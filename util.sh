#!/bin/bash

# Bundles up required files for the Python app, deploys to Phantom VM, and invokes the Phantom app compilation script.
# Use `deploy-bypass` to bypass the password prompts.

set -e

main() {
  if [[ -z "$PHANTOM_VM_IP_ADDR" ]]; then
    echo "Must provide PHANTOM_VM_IP_ADDR in environment" 1>&2
    exit 1
  fi

  command="${1:?Missing subcommand \"deploy\" or \"deploy-bypass\".}"
  case $command in
  "")
    echo "Kindly supply a command" && exit 1
    ;;
  deploy)
    echo "Tarring the ball..."
    pushd .. && tar -cvf phcode42v2/phcode42v2.tgz -X phcode42v2/exclude_files.txt phcode42v2/* && popd
    echo "Moving to remote..."
    scp phcode42v2.tgz "phantom@${PHANTOM_VM_IP_ADDR}":/home/phantom
    echo "Untarring on remote..."
    ssh "phantom@${PHANTOM_VM_IP_ADDR}" "rm -rf phcode42v2 && tar -xvf phcode42v2.tgz && cd phcode42v2 && phenv python /opt/phantom/bin/compile_app.pyc -i"
    ;;
  deploy-bypass)
    if [[ -z "$PHANTOM_PWD" ]]; then
      echo "Must provide PHANTOM_PWD in environment" 1>&2
      exit 1
    fi

    echo "Tarring the ball..."
    pushd .. && tar -cvf phcode42v2/phcode42v2.tgz -X phcode42v2/exclude_files.txt phcode42v2/* && popd
    echo "Moving to remote..."
    sshpass -p "${PHANTOM_PWD}" scp phcode42v2.tgz "phantom@${PHANTOM_VM_IP_ADDR}":/home/phantom
    echo "Untarring on remote..."
    sshpass -p "${PHANTOM_PWD}" ssh "phantom@${PHANTOM_VM_IP_ADDR}" "rm -rf phcode42v2 && tar -xvf phcode42v2.tgz && cd phcode42v2 && phenv python /opt/phantom/bin/compile_app.pyc -i"
    ;;
  *)
    echo "Not a valid command" && exit 1
  esac
}

main "$@"