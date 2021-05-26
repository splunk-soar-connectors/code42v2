PYTHONPATH=$(pwd)/build-scripts/

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
	scp ../phcode42v2.tgz "phantom@${PHANTOM_VM_IP_ADDR}":/home/phantom
	ssh "phantom@${PHANTOM_VM_IP_ADDR}"\
		"rm -rf phcode42v2 && tar -xvf phcode42v2.tgz && cd phcode42v2 && phenv python /opt/phantom/bin/compile_app.pyc -i"

deploy-bypass:: tar
	sshpass -p "${PHANTOM_VM_PASSWORD}" scp ../phcode42v2.tgz "phantom@${PHANTOM_VM_IP_ADDR}":/home/phantom
	sshpass -p "${PHANTOM_VM_PASSWORD}" ssh phantom@${PHANTOM_VM_IP_ADDR} \
		"rm -rf phcode42v2 && tar -xvf phcode42v2.tgz && cd phcode42v2 && phenv python /opt/phantom/bin/compile_app.pyc -i"

ssh::
	sshpass -p "${PHANTOM_VM_PASSWORD}" ssh phantom@${PHANTOM_VM_IP_ADDR}

open-web::
	open https://${PHANTOM_VM_IP_ADDR}:9999
