PYTHON ?= python3
SPLAT := $(PYTHON) -m splat split
CONFIG_DIR := config
BUILD_DIR := build
TOOLS_DIR := tools
OBJDIFF_CLI := $(TOOLS_DIR)/objdiff-cli

.PHONY: all extract check setup report clean

all: extract

setup:
	$(PYTHON) -m pip install -U -r requirements.txt

extract:
	$(PYTHON) configure.py --link-disc
	$(SPLAT) $(CONFIG_DIR)/slps_006.18.yaml --disassemble-all --make-full-disasm-for-code
	$(SPLAT) $(CONFIG_DIR)/wizards.exe.yaml --disassemble-all --make-full-disasm-for-code

check:
	sha1sum --check $(CONFIG_DIR)/checksum.sha1

report:
	@test -x $(OBJDIFF_CLI) || $(PYTHON) $(TOOLS_DIR)/download_objdiff.py
	$(OBJDIFF_CLI) report generate -o $(BUILD_DIR)/report.json

clean:
	rm -rf asm assets build expected .splache
	rm -f $(CONFIG_DIR)/undefined_funcs_auto.*.txt $(CONFIG_DIR)/undefined_syms_auto.*.txt
	rm -f objdiff.json report.json

.SECONDARY:
SHELL := /bin/bash -e -o pipefail
