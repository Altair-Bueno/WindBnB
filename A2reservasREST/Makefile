VENV_DIR     = .venv
PYTHON       = python3.11
PORT         = 8000
HOST         = 0.0.0.0

REQUIREMENTS_FILES = requirements.txt dev-requirements.txt

# Goals
dev:
	$(VENV_DIR)/bin/uvicorn src:app --host=$(HOST) --port=$(PORT) --reload

install: $(VENV_DIR) $(REQUIREMENTS_FILES)
	$(VENV_DIR)/bin/pip-sync $(REQUIREMENTS_FILES)

lint:
	$(VENV_DIR)/bin/ruff --ignore=F403,F405 src

fmt:
	$(VENV_DIR)/bin/black src

clean:
	rm -fr $(VENV_DIR)

# Artifacts
%.txt: %.in $(VENV_DIR)
	$(VENV_DIR)/bin/pip-compile $<

$(VENV_DIR): 
	$(PYTHON) -m venv $@
	$(VENV_DIR)/bin/pip install pip-tools

.PHONY: dev install lint fmt