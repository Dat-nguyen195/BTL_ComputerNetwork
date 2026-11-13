.PHONY: help setup doctor check report
help:
	@./project --help
setup:
	@./project setup

doctor check report:
	@./project $@
