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

# Every database the task list creates. They are removed before and after a run
# so that a half finished run does not break the next one. "demodb" is not in
# here on purpose, the tests only read it.
TEST_DBS = ("alatestdb", "compactdbtest", "destinationdb", "anotherdb",
            "copydb", "destinationdb1")


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


def record(name, casefile, task, status, note, expected):
    """Log one result.

    Several cases share the same task name (renamedb, renamedb_adoff, ... all
    run the "renamedb" task), so the case file is what identifies a test. It
    leads every line, with the task it runs in brackets.
    """
    ok = (status == expected)
    results.append({"name": name, "file": casefile, "ok": ok, "note": note})
    label = "%s [%s]" % (name, task)
    if ok:
        print(label + " : " + '\033[32m{0}\033[0m'.format(status))
    else:
        print(label + " : " + '\033[31mexpected {0}, got {1} ({2})\033[0m'.format(
            expected, status, note))
        print("    case file: %s" % casefile)
    return ok


def send_one(name, req, token, expected="success", casefile=""):
    req["token"] = token
    task = req.get("task", name)
    response = exec_task(cmsip, port, url, json.dumps(req))
    try:
        data = json.loads(response.decode())
    except ValueError:
        record(name, casefile, task, "invalid",
               "non JSON response: %s" % response[:200], expected)
        return {"task": task, "status": "failure"}
    record(name, casefile, task, data.get("status"), data.get("note", ""),
           expected)
    return data


def do_one_job(name, taskfile, token, expected="success"):
    request = load_task(taskfile)
    if isinstance(request, list):
        for index, req in enumerate(request):
            data = send_one("%s[%d]" % (name, index), req, token, expected,
                            taskfile)
    else:
        data = send_one(name, request, token, expected, taskfile)
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


def dump_one(name, token):
    """Run a single task case with the real token and print its raw response.

    Used to capture actual response values, e.g. to verify or update the API
    documentation. The stale token in the case file is replaced with `token`.
    """
    request = load_task(TEST_CASE_DIR + name + ".txt")
    reqs = request if isinstance(request, list) else [request]
    for req in reqs:
        req["token"] = token
        response = exec_task(cmsip, port, url, json.dumps(req))
        try:
            data = json.loads(response.decode())
            print(json.dumps(data, indent=3, sort_keys=True, ensure_ascii=False))
        except ValueError:
            print(response.decode(errors="replace"))


def reset_test_dbs():
    """Drop whatever a previous run left behind.

    A run that dies half way through leaves database directories and
    databases.txt entries around, and the next run then fails on names that are
    already taken. Only the databases the suite creates itself are touched.
    """
    for name in TEST_DBS:
        shutil.rmtree(os.path.join(CUBRID_DATABASES, name), ignore_errors=True)

    dblist = os.path.join(CUBRID_DATABASES, "databases.txt")
    try:
        with open(dblist, "r") as f:
            lines = f.readlines()
    except IOError:
        return
    def is_test_db(line):
        fields = line.split()
        return not line.startswith("#") and fields and fields[0] in TEST_DBS

    kept = [l for l in lines if not is_test_db(l)]
    if len(kept) != len(lines):
        with open(dblist, "w") as f:
            f.writelines(kept)


def build_env():
    """Create what the test cases expect to find on the host."""
    reset_test_dbs()
    # copydb_advance copies a database into this directory.
    dest = os.path.join(CUBRID_DATABASES, "destinationdb1")
    if not os.path.isdir(dest):
        os.makedirs(dest)
    # getcaslogtopresult and removecasrunnertmpfile read these files.
    tmpdir = os.path.join(CUBRID, "tmp")
    srcdir = os.path.join(TEST_CONFIG_DIR, "tmp_file_for_test")
    for name in os.listdir(srcdir):
        shutil.copy(os.path.join(srcdir, name), tmpdir)
    # removelog deletes the file it is given, so give it a disposable one.
    with open(os.path.join(tmpdir, "test_removelog.log"), "w") as f:
        f.write("dummy log line for removelog test\n")
    # runscript only accepts a path under $CUBRID or $CUBRID_DATABASES, so the
    # script it runs has to be created there.
    script = os.path.join(tmpdir, "test_runscript.sh")
    with open(script, "w") as f:
        f.write("#!/bin/sh\necho runscript test\n")
    os.chmod(script, 0o755)


def clean_env():
    reset_test_dbs()


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
            out.write('<testcase name="%s" file="%s" status="run" time="0" '
                      'classname="CMSERVER_TEST">\n'
                      % (escape(item["name"]), escape(item["file"])))
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
# The calls above only set up the session, the report covers the task list.
results = []

# `--dump <case> [<case> ...]` logs in and prints the raw response of each case
# with the real token, instead of running the whole task list.
if len(sys.argv) > 1 and sys.argv[1] == "--dump":
    for name in sys.argv[2:]:
        print("===== %s =====" % name)
        dump_one(name, token)
    sys.exit(0)

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
    for item in results:
        if not item["ok"]:
            print("  \033[31m%s\033[0m (%s): %s"
                  % (item["name"], item["file"], item["note"]))
    sys.exit(1)

print("\n\033[32mall %d tasks succeeded.\033[0m" % len(results))
