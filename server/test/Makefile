CUR_PATH=$(shell /bin/pwd)
COVERAGE_PATH=../cmserver/
LOG_PATH=$(CUR_PATH)/log
PYTHON?=python3

# test_tasks.py drives the JSON API over HTTPS, which is the interface the
# manager server exposes on cm_port.
test: $(LOG_PATH)
	TEST_XML=$(LOG_PATH)/test_cmserver.xml $(PYTHON) test_tasks.py

$(LOG_PATH):
	mkdir -p $(LOG_PATH)

lcov: $(LOG_PATH)
	rm -f $(LOG_PATH)/CM_SERVER.CoverageResult.info
	lcov -q -d $(COVERAGE_PATH) --no-recursion -b . -c -t CM_SERVER -o $(LOG_PATH)/tmp.CM_SERVER.CoverageResult.info --ignore-errors source
	lcov --remove $(LOG_PATH)/tmp.CM_SERVER.CoverageResult.info stat.h sysmacros.h '*.h' -o $(LOG_PATH)/CM_SERVER.CoverageResult.info
	rm $(LOG_PATH)/tmp.CM_SERVER.CoverageResult.info

clean:
	rm -rf $(LOG_PATH)

.PHONY: test lcov clean
