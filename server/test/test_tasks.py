#! /usr/bin/env python3
import http.client
import json
import os
import ssl
import sys
from getpass import getpass

DEFAULT_PORT = 8001


def findport():
    """Read cm_port from the manager server configuration.

    The port used to be taken from cm_httpd.conf, which does not exist any
    more; cm.conf is the current configuration file.
    """
    cubrid = os.environ.get("CUBRID")
    if not cubrid:
        print("CUBRID environment variable is not set.")
        sys.exit(1)

    conf = os.path.join(cubrid, "conf", "cm.conf")
    try:
        with open(conf, "r") as cf:
            for line in cf:
                line = line.split("#", 1)[0].strip()
                if line.startswith("cm_port"):
                    _, _, value = line.partition("=")
                    if value.strip().isdigit():
                        return int(value.strip())
    except IOError:
        pass

    print("cm_port not found in %s, falling back to %d." % (conf, DEFAULT_PORT))
    return DEFAULT_PORT


cmsip = "localhost"
port = findport()
url = "/cm_api"
testdir = "task_test_case_json/"

token = ""
CUBRID = ""
CUBRID_DATABASES = ""

nfailed = 0

# The manager server serves cm_port over TLS with a self signed certificate,
# so the certificate of the host under test is not verified here.
ssl_context = ssl._create_unverified_context()


def exec_task(ip, port, url, body):
    conn = http.client.HTTPSConnection(ip, port, context=ssl_context)
    try:
        conn.request("POST", url, body)
        return conn.getresponse().read()
    finally:
        conn.close()


def load_task(taskfile):
    with open(taskfile, "r") as task:
        filebuf = task.read()
    filebuf = filebuf.replace("$CUBRID_DATABASES", str(CUBRID_DATABASES))
    filebuf = filebuf.replace("$CUBRID", str(CUBRID))
    return json.loads(filebuf)


def report(data):
    global nfailed
    if data.get("status") == "failure":
        nfailed += 1
        print(data.get("task", "?") + " : " +
              '\033[31m{0}\033[0m'.format(data.get("note", "")))
    else:
        print(data.get("task", "?") + " : " +
              '\033[32m{0}\033[0m'.format(data.get("status")))


def send_one(req, token):
    global nfailed
    req["token"] = token
    response = exec_task(cmsip, port, url, json.dumps(req))
    try:
        data = json.loads(response.decode())
    except ValueError:
        nfailed += 1
        print(req.get("task", "?") + " : " +
              '\033[31mnon JSON response: {0}\033[0m'.format(response[:200]))
        return {"task": req.get("task", "?"), "status": "failure"}
    report(data)
    return data


def do_one_job(taskfile, token):
    request = load_task(taskfile)
    if isinstance(request, list):
        for req in request:
            data = send_one(req, token)
    else:
        data = send_one(request, token)
    return data


def do_all_jobs(token):
    if len(sys.argv) == 1:
        listfile = "task_list.txt"
    else:
        listfile = sys.argv[1]
    with open(listfile, "r") as tasks:
        for data in tasks:
            data = data.rstrip()
            if data == "":
                continue
            if data[0] == '/':
                print('\n\033[33m{0}\033[0m'.format(data))
                continue
            do_one_job(testdir + data + ".txt", token)


def init_env():
    response = do_one_job(testdir + "/login.txt", "")
    if response["status"] == "failure":
        request = load_task(testdir + "/login.txt")
        request["password"] = getpass(
            "Please input the passwd for %s: " % (request["id"]))
        response = send_one(request, "")
        if response["status"] == "failure":
            print("login failed, cannot run the tests.")
            sys.exit(1)
    token = response["token"]
    response = do_one_job(testdir + "/getenv.txt", token)
    bindir = response["CUBRID"]
    datadir = response["CUBRID_DATABASES"]
    return token, bindir, datadir


token, CUBRID, CUBRID_DATABASES = init_env()
# The login and the getenv calls above are the ones that set up the session,
# their failures are counted from the task list only.
nfailed = 0
do_all_jobs(token)

if nfailed:
    print("\n\033[31m%d task(s) failed.\033[0m" % nfailed)
    sys.exit(1)

print("\n\033[32mall tasks succeeded.\033[0m")
