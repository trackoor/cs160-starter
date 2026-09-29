# Targets for testing, formatting and submitting your compiler. Run `make` for the list.

PYTHON ?= python3
RUFF ?= $(firstword $(wildcard build_support/.venv/bin/ruff) $(shell command -v ruff 2>/dev/null))
LINT_DIRS := $(wildcard compiler tools release build_support starter logo)

# The files you do not write. Every other module in compiler/ is yours and is submitted.
PROVIDED := compiler/__init__.py compiler/__main__.py compiler/config.py compiler/emit.py \
            compiler/errors.py compiler/ir.py compiler/subset.py
STUDENT_MODULES := $(filter-out $(PROVIDED),$(wildcard compiler/*.py))

# What each submission contains, besides your modules: your design documents and your tests.
PA1_FILES := docs/pa1-design.md test/mine/pa1
PA2_FILES := docs/pa2-design.md test/mine/pa2 $(PA1_FILES)
PA3_FILES := docs/pa3-design.md test/mine/pa3 $(PA2_FILES)
PA4_FILES := docs/pa4-design.md test/mine/pa4 $(PA3_FILES)
PA5_FILES := docs/pa5-design.md test/mine/pa5 $(PA4_FILES)
PA6_FILES := docs/pa6-design.md test/mine/pa6 $(PA5_FILES)

.PHONY: help check-tests check-public-ci-tests format check-format check-lint require-ruff

help:
	@echo "make check-tests           run the tests of every released assignment, and your own"
	@echo "make test-pa1              run the tests of one assignment (test-pa1 ... test-pa6)"
	@echo "make format                format your Python files in place"
	@echo "make check-format          check the formatting without changing anything"
	@echo "make check-lint            check your Python files for common mistakes"
	@echo "make submit-pa1            a zip for staff; you hand in with oneworld assessment submit"

check-tests:
	$(PYTHON) tools/check.py

test-pa%:
	$(PYTHON) tools/check.py pa$*

# The checks that pass on the starter as released: the toolchain and the provided code.
check-public-ci-tests:
	$(PYTHON) tools/doctor.py

format: require-ruff
	$(RUFF) format $(LINT_DIRS)

check-format: require-ruff
	$(RUFF) format --check $(LINT_DIRS)

check-lint: require-ruff
	$(RUFF) check $(LINT_DIRS)

require-ruff:
	@test -n "$(RUFF)" || { echo "ruff was not found; run build_support/packages.sh"; exit 1; }

submit-pa%:
	@test -f docs/pa$*-design.md || { echo "docs/pa$*-design.md is missing; is PA$* released?"; exit 1; }
	@rm -f pa$*-submission.zip
	zip -r pa$*-submission.zip $(sort $(STUDENT_MODULES) $(PA$*_FILES)) -x '*__pycache__*' '*.DS_Store'
	@echo "Created pa$*-submission.zip"
