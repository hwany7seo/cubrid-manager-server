#! /usr/bin/env python3
import datetime
import json
import os
import re
import shutil
import ssl
import sys
from getpass import getpass

DEFAULT_PORT = 8001
TEST_CASE_DIR = "task_test_case_json/"
TEST_CONFIG_DIR = "task_test_config/"


def findport():
    """Read cm_port from the manager server configuration.

    The port used to be taken from cm_httpd.conf, which does not exist any
    more; cm.conf is the current configuration file.
    """
    cubrid = os.environ.get("CUBRID")
    if not cubrid:
        print("CUBRID environment variable is not set.")
        sys.exit(1)

    # cm.conf writes an entry either as "cm_port 8001" or as "cm_port=8001".
    conf = os.path.join(cubrid, "conf", "cm.conf")
    try:
        with open(conf, "r") as cf:
            for line in cf:
                line = line.split("#", 1)[0].strip()
                match = re.match(r"cm_port\s*=?\s*(\d+)$", line)
                if match:
                    return int(match.group(1))
    except IOError:
        pass

    print("cm_port not found in %s, falling back to %d." % (conf, DEFAULT_PORT))
    return DEFAULT_PORT


cmsip = "localhost"
port = findport()
url = "/cm_api"

token = ""
CUBRID = ""
CUBRID_DATABASES = ""

results = []

# The manager server serves cm_port over TLS with a self signed certificate,
# so the certificate of the host under test is not verified here.
ssl_context = ssl._create_unverified_context()


def exec_task(ip, port, url, body):
    import http.client
    conn = http.client.HTTPSConnection(ip, port, context=ssl_context)
    try:
        conn.request("POST", url, body)
        return conn.getresponse().read()
    finally:
        conn.close()


def replace_env_vars(contents):
    """Substitute the placeholders a test case may use.

    The $AUTO_* ones are set to the next minute so that a scheduled job created
    by the test is due right after the request.
    """
    next_minute = datetime.datetime.now() + datetime.timedelta(minutes=1)
    contents = contents.replace("$AUTO_DATE", next_minute.strftime("%Y-%m-%d"))
    contents = contents.replace("$AUTO_TIME", next_minute.strftime("%H%M"))
    contents = contents.replace("$AUTO_QUERY_TIME",
                                next_minute.strftime("%Y/%m/%d %H:%M"))
    contents = contents.replace("$CUBRID_DATABASES", str(CUBRID_DATABASES))
    contents = contents.replace("$CUBRID", str(CUBRID))
    return contents


def load_task(taskfile):
    with open(taskfile, "r") as task:
        return json.loads(replace_env_vars(task.read()))


def record(name, task, status, note, expected):
    ok = (status == expected)
    results.append({"name": name, "ok": ok, "note": note})
    if ok:
        print(task + " : " + '\033[32m{0}\033[0m'.format(status))
    else:
        print(task + " : " + '\033[31mexpected {0}, got {1} ({2})\033[0m'.format(
            expected, status, note))
    return ok


def send_one(name, req, token, expected="success"):
    req["token"] = token
    task = req.get("task", name)
    response = exec_task(cmsip, port, url, json.dumps(req))
    try:
        data = json.loads(response.decode())
    except ValueError:
        record(name, task, "invalid", "non JSON response: %s" % response[:200],
               expected)
        return {"task": task, "status": "failure"}
    record(name, task, data.get("status"), data.get("note", ""), expected)
    return data


def do_one_job(name, taskfile, token, expected="success"):
    request = load_task(taskfile)
    if isinstance(request, list):
        for index, req in enumerate(request):
            data = send_one("%s[%d]" % (name, index), req, token, expected)
    else:
        data = send_one(name, request, token, expected)
    return data


def do_all_jobs(token):
    listfile = sys.argv[1] if len(sys.argv) > 1 else "task_list.txt"
    with open(listfile, "r") as tasks:
        for line in tasks:
            line = line.rstrip()
            if line == "":
                continue
            if line[0] == '/':
                print('\n\033[33m{0}\033[0m'.format(line))
                continue
            # "<test case>" runs a test that must succeed, "<test case>,failure"
            # one that must be rejected by the server.
            name, _, expected = line.partition(",")
            expected = expected.strip() or "success"
            do_one_job(name.strip(), TEST_CASE_DIR + name.strip() + ".txt",
                       token, expected)


def build_env():
    """Create what the test cases expect to find on the host."""
    # copydb_advance copies a database into this directory.
    dest = os.path.join(CUBRID_DATABASES, "destinationdb1")
    if not os.path.isdir(dest):
        os.makedirs(dest)
    # getcaslogtopresult and removecasrunnertmpfile read these files.
    tmpdir = os.path.join(CUBRID, "tmp")
    srcdir = os.path.join(TEST_CONFIG_DIR, "tmp_file_for_test")
    for name in os.listdir(srcdir):
        shutil.copy(os.path.join(srcdir, name), tmpdir)


def clean_env():
    for name in ("destinationdb1", "destinationdb", "copydb"):
        shutil.rmtree(os.path.join(CUBRID_DATABASES, name), ignore_errors=True)


def write_junit_xml(path):
    """Write the report the CI job collects."""
    failures = sum(1 for r in results if not r["ok"])
    directory = os.path.dirname(path)
    if directory and not os.path.isdir(directory):
        os.makedirs(directory)

    def escape(text):
        return (str(text).replace("&", "&amp;").replace("<", "&lt;")
                .replace(">", "&gt;").replace('"', "&quot;"))

    with open(path, "w") as out:
        out.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        out.write('<testsuites tests="%d" failures="%d" disabled="0" '
                  'errors="0" time="0" name="AllTests">\n'
                  % (len(results), failures))
        out.write('<testsuite name="CMSERVER_TEST" tests="%d" failures="%d" '
                  'disabled="0" errors="0" time="0">\n'
                  % (len(results), failures))
        for item in results:
            out.write('<testcase name="%s" status="run" time="0" '
                      'classname="CMSERVER_TEST">\n' % escape(item["name"]))
            if not item["ok"]:
                out.write('<failure message="%s" type=""></failure>\n'
                          % escape(item["note"]))
            out.write('</testcase>\n')
        out.write('</testsuite>\n</testsuites>\n')


def init_env():
    response = do_one_job("login", TEST_CASE_DIR + "login.txt", "")
    if response["status"] == "failure":
        request = load_task(TEST_CASE_DIR + "login.txt")
        request["password"] = getpass(
            "Please input the passwd for %s: " % (request["id"]))
        response = send_one("login", request, "")
        if response["status"] == "failure":
            print("login failed, cannot run the tests.")
            sys.exit(1)
    token = response["token"]
    response = do_one_job("getenv", TEST_CASE_DIR + "getenv.txt", token)
    return token, response["CUBRID"], response["CUBRID_DATABASES"]


token, CUBRID, CUBRID_DATABASES = init_env()
# The two calls above only set up the session, the report covers the task list.
results = []

build_env()
try:
    do_all_jobs(token)
finally:
    clean_env()

xmlfile = os.environ.get("TEST_XML")
if xmlfile:
    write_junit_xml(xmlfile)

nfailed = sum(1 for r in results if not r["ok"])
if nfailed:
    print("\n\033[31m%d of %d task(s) failed.\033[0m" % (nfailed, len(results)))
    sys.exit(1)

print("\n\033[32mall %d tasks succeeded.\033[0m" % len(results))
