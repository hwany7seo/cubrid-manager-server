#! /usr/bin/env python3
import atexit
import datetime
import json
import os
import re
import shutil
import signal
import ssl
import subprocess
import sys
import time
from getpass import getpass

DEFAULT_PORT = 8001
TEST_CASE_DIR = "task_test_case_json/"
TEST_CONFIG_DIR = "task_test_config/"
# Where start_kill_targets() records the processes it spawned, so that a run
# killed before clean_env() can be cleaned up by the next one.
HELPER_PID_FILE = "log/helper_pids"

# Every database the task list creates. They are removed before and after a run
# so that a half finished run does not break the next one. "demodb" is not in
# here on purpose, the tests only read it.
TEST_DBS = ("alatestdb", "compactdbtest", "destinationdb", "anotherdb",
            "copydb", "destinationdb1", "renameadvdb", "renamedadvdb",
            "optionaldb")


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

# Placeholders whose value is only known once the run has started, see
# start_kill_targets().
runtime_vars = {}
helper_procs = []

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
    for name, value in runtime_vars.items():
        contents = contents.replace(name, value)
    contents = contents.replace("$CUBRID_DATABASES", str(CUBRID_DATABASES))
    contents = contents.replace("$CUBRID", str(CUBRID))
    return contents


def load_task(taskfile):
    with open(taskfile, "r") as task:
        return json.loads(replace_env_vars(task.read()))


def record(name, casefile, task, status, note, expected, response=None):
    """Log one result.

    Several cases share the same task name (renamedb, renamedb_adoff, ... all
    run the "renamedb" task), so the case file is what identifies a test. It
    leads every line, with the task it runs in brackets.

    `response` is kept for the detailed report only; the console output and the
    plain XML stay short.
    """
    ok = (status == expected)
    results.append({"name": name, "file": casefile, "task": task, "ok": ok,
                    "note": note, "response": response})
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
    # Tasks that echo a log file back (loadaccesslog) can carry bytes that are
    # not valid UTF-8, because the server writes error messages with an
    # uninitialized buffer into the log. That is a server defect, but it must
    # not turn into a failure of whatever case happens to read the log.
    body = response.decode(errors="replace")
    try:
        data = json.loads(body)
    except ValueError:
        record(name, casefile, task, "invalid",
               "non JSON response: %s" % response[:200], expected, body)
        return {"task": task, "status": "failure"}
    # The raw body is kept verbatim: docs/api/*.md quote the server's own
    # formatting, so a re-serialized copy would not be comparable.
    record(name, casefile, task, data.get("status"), data.get("note", ""),
           expected, body)
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
            data = json.loads(response.decode(errors="replace"))
            print(json.dumps(data, indent=3, sort_keys=True, ensure_ascii=False))
        except ValueError:
            print(response.decode(errors="replace"))


def stop_test_servers():
    """Shut down any server still running for a database the suite creates.

    A stopdb that does not finish leaves "cub_server <db>" behind. Deleting the
    directory underneath it does not kill it, and the next run then fails on
    "database is active" or on volumes it cannot mount, so the damage carries
    over from run to run until someone kills the process by hand.
    """
    cubrid_bin = os.path.join(CUBRID, "bin", "cubrid")
    for name in TEST_DBS:
        if subprocess.call(["pgrep", "-f", "^cub_server %s$" % name],
                           stdout=subprocess.DEVNULL) != 0:
            continue
        subprocess.call([cubrid_bin, "server", "stop", name],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.call(["pkill", "-9", "-f", "^cub_server %s$" % name],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def reset_test_dbs():
    """Drop whatever a previous run left behind.

    A run that dies half way through leaves database directories and
    databases.txt entries around, and the next run then fails on names that are
    already taken. Only the databases the suite creates itself are touched.
    """
    stop_test_servers()
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


def probe(request):
    """Run a task without recording it, for the setup code below."""
    request["token"] = token
    try:
        return json.loads(exec_task(cmsip, port, url, json.dumps(request)).decode())
    except ValueError:
        return {}


def find_tranindex(pid, timeout=15):
    """Return the transaction index demodb gave the client running as `pid`.

    The index is reported as "1(ACTIVE)" but killtran wants a bare number.
    """
    deadline = time.time() + timeout
    while time.time() < deadline:
        data = probe({"task": "gettransactioninfo", "dbname": "demodb"})
        for entry in data.get("transactioninfo", []):
            for tran in entry.get("transaction", []):
                if tran.get("pid") == str(pid):
                    match = re.match(r"\d+", tran.get("tranindex", ""))
                    if match:
                        return match.group(0)
        time.sleep(0.5)
    return ""


def record_helper_pid(proc):
    """Remember a helper process so a killed run can be cleaned up later.

    clean_env() is skipped when the run dies on SIGKILL, and the sleep would
    then sit there for an hour while the csql session keeps a transaction open
    on demodb. The pid is written together with the command line so the next
    run only kills a pid that is still the process we started.
    """
    helper_procs.append(proc)
    directory = os.path.dirname(HELPER_PID_FILE)
    if directory and not os.path.isdir(directory):
        os.makedirs(directory)
    with open(HELPER_PID_FILE, "a") as f:
        f.write("%d %s\n" % (proc.pid, " ".join(proc.args)))


def sweep_stale_helpers():
    """Kill helpers a previous run left behind, and only those."""
    try:
        with open(HELPER_PID_FILE) as f:
            entries = [line.split(None, 1) for line in f if line.strip()]
    except IOError:
        return
    for pid, cmdline in entries:
        try:
            with open("/proc/%s/cmdline" % pid, "rb") as f:
                running = f.read().replace(b"\0", b" ").decode().strip()
        except IOError:
            continue        # already gone, or not ours any more
        if running == cmdline.strip():
            print("killing helper left over from an earlier run: %s %s"
                  % (pid, running))
            try:
                os.kill(int(pid), signal.SIGKILL)
            except OSError:
                pass
    os.remove(HELPER_PID_FILE)


def open_transaction():
    """Open a transaction on demodb and leave it open.

    With autocommit off the transaction lives until the process exits, and the
    process exits on its own when the runner dies, because stdin is a pipe.
    """
    csql = subprocess.Popen(
        [os.path.join(CUBRID, "bin", "csql"), "--CS-mode", "-u", "dba", "demodb"],
        stdin=subprocess.PIPE, stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL, universal_newlines=True)
    record_helper_pid(csql)
    csql.stdin.write(";autocommit off\nselect count(*) from db_class;\n")
    csql.stdin.flush()
    return csql


def start_kill_targets():
    """Give killprocess and killtransaction something that really exists.

    Both cases used to carry a hardcoded id (pid 99999, tranindex "2(+)"), so
    they failed on every host. The suite now creates its own victims and passes
    their real ids in through $TEST_KILL_PID / $TEST_TRANINDEX.
    """
    sweep_stale_helpers()

    dummy = subprocess.Popen(["sleep", "3600"], stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL)
    record_helper_pid(dummy)
    runtime_vars["$TEST_KILL_PID"] = str(dummy.pid)

    # Two transactions, not one: killtransaction reports the transactions that
    # are still there after the kill, so with a single victim it can only ever
    # answer "transactioninfo": null. The second one is the bystander.
    victim, bystander = (open_transaction(), open_transaction())

    tranindex = find_tranindex(victim.pid)
    if not tranindex:
        print("\033[33mno transaction found on demodb, killtransaction will "
              "fail.\033[0m")
    runtime_vars["$TEST_TRANINDEX"] = tranindex
    if not find_tranindex(bystander.pid):
        print("\033[33monly one transaction on demodb, killtransaction will "
              "report an empty list.\033[0m")


def stop_kill_targets():
    for proc in helper_procs:
        try:
            if proc.stdin:
                proc.stdin.close()
            proc.kill()
            proc.wait(timeout=5)
        except Exception:
            pass
    del helper_procs[:]
    try:
        os.remove(HELPER_PID_FILE)
    except OSError:
        pass


def make_loaddb_input(tmpdir):
    """Unload demodb into a throwaway schema/objects pair for the loaddb case.

    loaddb runs with delete_orignal_files=y, so it consumes whatever it is
    pointed at. It used to be pointed at demodb's own dump, which the unloaddb
    case (much later in the list) regenerates -- meaning loaddb was really
    reading the *previous* run's output, and a run that died in between broke
    the next one with "file does not exists". Its input is now produced here.
    """
    for suffix in ("schema", "objects", "indexes", "trigger"):
        try:
            os.remove(os.path.join(tmpdir, "test_loaddb_%s" % suffix))
        except OSError:
            pass
    subprocess.call([os.path.join(CUBRID, "bin", "cubrid"), "unloaddb",
                     "--CS-mode", "-u", "dba", "-O", tmpdir,
                     "--output-prefix", "test_loaddb", "demodb"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def wait_for_mon_data(timeout=120):
    """Wait until the first monitoring sample has been collected.

    set_mon_interval resizes vol_mon, and that file is only created once a
    gather run has registered the volumes of a database. Called straight after
    a restart it would find no file and fail, and the failed reset_meta leaves
    the meta inconsistent for good, so the run has to wait for the first sample
    before it touches any of the monitoring cases.
    """
    meta = os.path.join(CUBRID, "var", "manager", "mon_data", "meta.json")
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with open(meta) as f:
                if json.load(f).get("k_total_vol_num", 0) > 0:
                    return True
        except (IOError, ValueError):
            pass
        time.sleep(2)
    print("\033[33mno monitoring data collected within %d s; the "
          "set_mon_interval and get_mon_statistic cases will fail. Check "
          "support_mon_statistic in cm.conf.\033[0m" % timeout)
    return False


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
    # analyzecaslog runs broker_log_top over a broker SQL log. Pointed at a live
    # CAS log it answers "resultlist": null, because nothing in this suite sends
    # SQL through a broker and broker_log_top then writes an empty report. This
    # fixture carries two executed queries so the parsing is actually covered.
    shutil.copy(os.path.join(TEST_CONFIG_DIR, "test_analyzecaslog.sql.log"), tmpdir)
    # getfolderswithkeyword searches for directories whose name contains the
    # keyword ("res"). Without one it answers "folders": null.
    folder = os.path.join(tmpdir, "test_result_folder")
    if not os.path.isdir(folder):
        os.makedirs(folder)
    make_loaddb_input(tmpdir)
    # adddbmtuser creates "yifan" and deletedbmtuser drops it again. A run that
    # died between the two leaves the user behind, and the next adddbmtuser
    # then fails with "already exist"; this is a no-op when it is not there.
    probe({"task": "deletedbmtuser", "targetid": "yifan"})
    wait_for_mon_data()
    start_kill_targets()


def clean_env():
    stop_kill_targets()
    reset_test_dbs()


def xml_escape(text):
    return (str(text).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def detail_xml_path(path):
    """`log/result.xml` -> `log/result_detail.xml`."""
    root, ext = os.path.splitext(path)
    return root + "_detail" + ext


def write_junit_xml(path, with_response=False):
    """Write the report the CI job collects.

    Two files are produced: the plain one stays small enough to skim, and the
    "_detail" one carries the full response of every case in <system-out>, so
    that the documented samples in docs/api/*.md can be checked against what
    the server really answers without re-running anything.
    """
    failures = sum(1 for r in results if not r["ok"])
    directory = os.path.dirname(path)
    if directory and not os.path.isdir(directory):
        os.makedirs(directory)

    with open(path, "w") as out:
        out.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        out.write('<testsuites tests="%d" failures="%d" disabled="0" '
                  'errors="0" time="0" name="AllTests">\n'
                  % (len(results), failures))
        out.write('<testsuite name="CMSERVER_TEST" tests="%d" failures="%d" '
                  'disabled="0" errors="0" time="0">\n'
                  % (len(results), failures))
        for item in results:
            out.write('<testcase name="%s" file="%s" task="%s" status="run" '
                      'time="0" classname="CMSERVER_TEST">\n'
                      % (xml_escape(item["name"]), xml_escape(item["file"]),
                         xml_escape(item.get("task", ""))))
            if not item["ok"]:
                out.write('<failure message="%s" type=""></failure>\n'
                          % xml_escape(item["note"]))
            if with_response and item.get("response") is not None:
                # A "]]>" inside the payload would close the section early.
                body = item["response"].replace("]]>", "]]]]><![CDATA[>")
                out.write('<system-out><![CDATA[\n%s\n]]></system-out>\n' % body)
            out.write('</testcase>\n')
        out.write('</testsuite>\n</testsuites>\n')


def wait_for_manager(timeout=90):
    """Block until the manager server answers on cm_port again."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            exec_task(cmsip, port, url, json.dumps({"task": "keepalive"}))
            return True
        except Exception:
            time.sleep(1)
    print("\033[31mthe manager server did not come back up within %d s.\033[0m"
          % timeout)
    return False


def reset_mon_data(cubrid_home):
    """Throw away the monitoring statistics files.

    They have to go while the service is down. cub_manager rebuilds them on the
    way up, and only a rebuilt set is guaranteed to be consistent: reset_meta()
    resizes broker/db/volume/os files one by one and updates k_interval last, so
    a failure in the middle (a missing vol_mon, for instance) leaves the files
    sized for the new interval and the meta claiming the old one. Once that
    happens set_mon_interval fails on every later call and the yearly
    get_mon_statistic reads past the end of the file.
    """
    mon_dir = os.path.join(cubrid_home, "var", "manager", "mon_data")
    if not os.path.isdir(mon_dir):
        return
    for name in os.listdir(mon_dir):
        try:
            os.remove(os.path.join(mon_dir, name))
        except OSError:
            pass


def restart_services():
    """Start the run from a known state.

    A run that was killed can leave a csql session holding a transaction on
    demodb, a cub_server that stopdb never managed to stop, or monitoring files
    that no longer match their meta. None of that is repaired by deleting
    directories, so the suite bounces the whole service first.
    """
    cubrid_home = os.environ["CUBRID"]
    cubrid_bin = os.path.join(cubrid_home, "bin", "cubrid")
    print("restarting the CUBRID service to start from a known state ...")
    sweep_stale_helpers()
    subprocess.call([cubrid_bin, "service", "stop"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    reset_mon_data(cubrid_home)
    subprocess.call([cubrid_bin, "service", "start"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # demodb is what most of the cases run against; "service start" only starts
    # it when cubrid.conf lists it, so ask for it explicitly.
    subprocess.call([cubrid_bin, "server", "start", "demodb"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    wait_for_manager()


def stop_services():
    """Leave the host with the service down, the way the run found it.

    restart_services() brings the whole service up at the start, so a finished
    run would otherwise leave cub_manager, the brokers and cub_server demodb
    behind on a machine that was idle before. Runs from the finally block, so a
    failed or interrupted run stops them too.
    """
    cubrid_bin = os.path.join(os.environ["CUBRID"], "bin", "cubrid")
    print("stopping the CUBRID service ...")
    subprocess.call([cubrid_bin, "service", "stop"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


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


# `--dump <case> [<case> ...]` logs in and prints the raw response of each case
# with the real token, instead of running the whole task list. It is a probe, so
# it uses the server as it finds it and never restarts anything.
dump_mode = len(sys.argv) > 1 and sys.argv[1] == "--dump"

if not dump_mode:
    restart_services()

token, CUBRID, CUBRID_DATABASES = init_env()
# The calls above only set up the session, the report covers the task list.
results = []

if dump_mode:
    for name in sys.argv[2:]:
        print("===== %s =====" % name)
        dump_one(name, token)
    sys.exit(0)

# A plain "kill" skips the finally below, so make the helper processes go away
# on the usual termination signals as well.
atexit.register(stop_kill_targets)
for _signum in (signal.SIGTERM, signal.SIGHUP):
    signal.signal(_signum, lambda signum, frame: sys.exit(128 + signum))

try:
    build_env()
    do_all_jobs(token)
finally:
    clean_env()
    stop_services()

xmlfile = os.environ.get("TEST_XML")
if xmlfile:
    write_junit_xml(xmlfile)
    write_junit_xml(detail_xml_path(xmlfile), with_response=True)

nfailed = sum(1 for r in results if not r["ok"])
if nfailed:
    print("\n\033[31m%d of %d task(s) failed.\033[0m" % (nfailed, len(results)))
    for item in results:
        if not item["ok"]:
            print("  \033[31m%s\033[0m (%s): %s"
                  % (item["name"], item["file"], item["note"]))
    sys.exit(1)

print("\n\033[32mall %d tasks succeeded.\033[0m" % len(results))
