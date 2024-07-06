.PHONY: run-init boot as_root deploy

as_root:
	@if [ `id -u` -ne 0 ]; then \
		echo "Please run this command as root"; \
		exit 1; \
	fi

boot:
	@if [ ! -d ".venv" ]; then \
		python3 -m venv .venv; \
		source .venv/bin/activate && \
			pip install --upgrade pip && \
			.venv/bin/pip install -r requirements.txt; \
	fi

run-init: boot
	PYTHONPATH=./:${PYTHONPATH}
	source .venv/bin/activate && python3 -m init config.yaml

deploy:
	ansible-playbook -v -i ansible/inventory -e target=paterica -e conf_file_src_path=../config.yaml ansible/playbook.yaml
