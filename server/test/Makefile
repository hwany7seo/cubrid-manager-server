CUR_PATH=$(shell /bin/pwd)
COVERAGE_PATH=../cmserver/
LOG_PATH=$(CUR_PATH)/log
PYTHON?=python3

# test_tasks.py drives the JSON API over HTTPS, which is the interface the
# manager server exposes on cm_port.
test: $(LOG_PATH)
	$(PYTHON) test_tasks.py

$(LOG_PATH):
	mkdir -p $(LOG_PATH)

# Tests of the interface that preceded the HTTP one. test_tasks.php speaks the
# line based socket protocol of cub_auto (cm_port) and cub_js (cm_port + 1), and
# sendfile uploads a job file to the transfer port 21000. Neither those two
# processes nor that port exist in the current server, so this target only runs
# against a manager server older than the HTTP interface.
legacy: sendfile $(LOG_PATH)
	/usr/bin/php -q test_tasks.php $(LOG_PATH)/test_cmserver.xml
	./sendfile task_test_case/jobfile task_test_case/jobfile.zip

sendfile: sendfile.cpp
	$(CXX) -o $@ $<

lcov: $(LOG_PATH)
	rm -f $(LOG_PATH)/CM_SERVER.CoverageResult.info
	lcov -q -d $(COVERAGE_PATH) --no-recursion -b . -c -t CM_SERVER -o $(LOG_PATH)/tmp.CM_SERVER.CoverageResult.info --ignore-errors source
	lcov --remove $(LOG_PATH)/tmp.CM_SERVER.CoverageResult.info stat.h sysmacros.h '*.h' -o $(LOG_PATH)/CM_SERVER.CoverageResult.info
	rm $(LOG_PATH)/tmp.CM_SERVER.CoverageResult.info

clean:
	rm -rf $(LOG_PATH) sendfile

.PHONY: test legacy lcov clean
