PYTHONPATH=$(pwd)/build-scripts/
SERVER_ADDRESS=${PHANTOM_VM_IP_ADDR}
SERVER_PASSWORD=${PHANTOM_VM_PASSWORD}

.PHONY: all clean test validate style tar deploy deploy-bypass ssh open-web

all: clean test validate style tar

clean::
	rm -f ../phcode42v2.tgz

test::
	pytest -vv

validate::
	python ./build-scripts/compile_app.pyc -c

style::
	pre-commit run --all-files --show-diff-on-failure

tar:: clean
	python ./build-scripts/compile_app.pyc -t

deploy:: tar
	scp ../phcode42v2.tgz "phantom@$(SERVER_ADDRESS)":/home/phantom
	ssh "phantom@$(SERVER_ADDRESS)"\
		"rm -rf phcode42v2 && tar -xvf phcode42v2.tgz && cd phcode42v2 && phenv python /opt/phantom/bin/compile_app.pyc -i"

deploy-bypass:: tar
	sshpass -p "$(SERVER_PASSWORD)" scp ../phcode42v2.tgz "phantom@$(SERVER_ADDRESS)":/home/phantom
	sshpass -p "$(SERVER_PASSWORD)" ssh phantom@$(SERVER_ADDRESS) \
		"rm -rf phcode42v2 && tar -xvf phcode42v2.tgz && cd phcode42v2 && phenv python /opt/phantom/bin/compile_app.pyc -i"

ssh::
	sshpass -p "$(SERVER_PASSWORD)" ssh phantom@$(SERVER_ADDRESS)

open-web::
	open https://$(SERVER_ADDRESS):9999
