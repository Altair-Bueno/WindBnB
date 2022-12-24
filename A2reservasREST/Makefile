VENV_DIR     = venv
PYTHON       = python3.11
PORT         = 8000
HOST         = 0.0.0.0

REQUIREMENTS_FILES = requirements.txt dev-requirements.txt

dev:
	$(VENV_DIR)/bin/uvicorn src:app --host=$(HOST) --port=$(PORT)

install: $(VENV_DIR) $(REQUIREMENTS_FILES)
	$(VENV_DIR)/bin/pip-sync $(REQUIREMENTS_FILES)

lint:
	$(VENV_DIR)/bin/ruff src

fmt:
	$(VENV_DIR)/bin/black src

%.txt: %.in venv 
	$(VENV_DIR)/bin/pip-compile $<

$(VENV_DIR): 
	$(PYTHON) -m venv $@
	$(VENV_DIR)/bin/pip install pip-tools

.PHONY: install dev lint fmt