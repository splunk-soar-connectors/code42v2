#!/bin/bash
# Usage:
#  ./util.sh <cmd>
#
# Commands:
#   tar: Bundles up required files for the Python app.
#   clean: Remove local app bundle (tar file).
#   deploy: Bundles up required files for the Python app, deploys to Phantom VM, and invokes the Phantom app compilation script.
#   deploy-bypass: Bypass the password prompts using the PHANTOM_VM_PASSWORD environment variable.
#   ssh: SSH into your Phantom VM.
#   open-web: Open your default web browser at `https://<phantom-vm-ip:9999>`.

set -eo pipefail

make_tar() {
  echo "Tarring the ball..."
  tar -cvf phcode42v2.tgz -X ./exclude_files.txt .
}

clean() {
  rm -f phcode42v2.tgz
}

deploy_bypass() {
  echo "Moving to remote..."
  sshpass -p "${PHANTOM_VM_PASSWORD}" scp phcode42v2.tgz "phantom@${PHANTOM_VM_IP_ADDR}":/home/phantom
  echo "Untarring on remote..."
  sshpass -p "${PHANTOM_VM_PASSWORD}" ssh phantom@${PHANTOM_VM_IP_ADDR} \
		"rm -rf phcode42v2deploy && mkdir phcode42v2deploy && tar -xvf phcode42v2.tgz -C phcode42v2deploy && cd phcode42v2deploy && phenv python /opt/phantom/bin/compile_app.pyc -i"
}

deploy() {
  scp phcode42v2.tgz "phantom@${PHANTOM_VM_IP_ADDR}":/home/phantom
  echo "Untarring on remote..."
  ssh "phantom@${PHANTOM_VM_IP_ADDR}" \
    "rm -rf phcode42v2deploy && mkdir phcode42v2deploy && tar -xvf phcode42v2.tgz -C phcode42v2deploy && cd phcode42v2deploy && phenv python /opt/phantom/bin/compile_app.pyc -i"
}

print_usage() {
  echo "./util.sh <tar, clean, deploy, deploy-bypass, ssh, open-web>"
}

main() {
  case $1 in
  "")
    echo "Kindly supply a command" && print_usage && exit 0
    ;;
  tar)
    clean
    make_tar
    ;;
  clean)
    clean
    ;;
  deploy)
    make_tar
    deploy
    ;;
  deploy-bypass)
    make_tar
    deploy_bypass
    ;;
  ssh)
    sshpass -p "${PHANTOM_VM_PASSWORD}" ssh phantom@${PHANTOM_VM_IP_ADDR}
    ;;
  open-web)
    open https://${PHANTOM_VM_IP_ADDR}:9999
    ;;
  *)
    echo "Not a valid command" && print_usage && exit 0
  esac
}

main "$@"
