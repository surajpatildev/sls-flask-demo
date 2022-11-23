python3.9_env:
	pyenv local `cat python_local_version`
python3.9_venv :
	python3.9_env
	python -m venv venv
venv_activate :
	python3.9_venv
    ( \
        source venv/bin/activate; \
        pip install --upgrade pip; \
        pip install -r requirements.txt; \
    )

serverless_install: venv_activate
    ( \
        node_version=`which node`; \
        if [ -z "$node_version" ]; then brew install node     ; fi ;\
        npm install -g serverless; \
        sls plugin install -n serverless-python-requirements ; \
        npm install serverless-offline --save-dev ; \
    )
waypoint_setup:serverless_install
waypoint_start:
    ( \
        source venv/bin/activate; \
        sls wsgi serve; \
    )