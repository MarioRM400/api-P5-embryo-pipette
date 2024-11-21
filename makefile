DATA_ENV_DIR := .

.SILENT:
.ONESHELL:

clean:
	@echo "## cleaning current project"
	find . -name '*.pyc' -delete

dvenv: clean $(DATA_ENV_DIR)/.venv/touchfile validation## 💻 Install all python libraries in requirements.txt

$(DATA_ENV_DIR)/.venv/touchfile: data-req.txt
	python -m venv $(DATA_ENV_DIR)/.venv
	. $(DATA_ENV_DIR)/.venv/bin/activate; pip install -Ur data-req.txt
	touch $(DATA_ENV_DIR)/.venv/touchfile

pull: dvenv
	@echo "## pulling data from bucket"
	. $(DATA_ENV_DIR)/.venv/bin/activate \
	&& dvc pull

push: dvenv
	@echo "## pushing data and weights to bucket"
	. $(DATA_ENV_DIR)/.venv/bin/activate \
	&& dvc add P5-raquet-blastocist-pipette/app/weights \
	&& git add P5-raquet-blastocist-pipette/app/weights.dvc \
	&& git commit -m "Weights added with dvc add command" \
	&& dvc push \
	&& git add P5-raquet-blastocist-pipette/app/weights.dvc \
	&& git commit -m "Weights pushed with dvc push command"

info:
	@echo "## executing dvc doctor command"
	. $(DATA_ENV_DIR)/.venv/bin/activate \
	&& dvc doctor

validation:
	@echo "## validating python version"
	. $(DATA_ENV_DIR)/.venv/bin/activate \
	&& python -V | grep 3.12.2 |if read remote; then echo "\t- .venv has $${remote} ";else echo "\tYou have not installed PYTHON VERSION 3.12.2 \n\t- Delete .venv and activate conda environment with python version 3.12.2 \n\t- pull again \n\t- validation failed ❌";exit 125 ;fi \
	&& echo "\t- validation success ✅"