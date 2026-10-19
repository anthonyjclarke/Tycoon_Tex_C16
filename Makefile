PYTHON ?= python3

.PHONY: all run run-original test verify clean

all:
	$(PYTHON) scripts/restore_c16.py

run: all
	$(PYTHON) scripts/run_vice.py

run-original:
	$(PYTHON) scripts/run_vice.py --original

test:
	$(PYTHON) -m unittest discover -s test -p 'test_*.py' -v

verify: all
	$(PYTHON) scripts/verify_vice.py

clean:
	rm -rf build .pio
