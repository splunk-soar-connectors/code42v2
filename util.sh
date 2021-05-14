#!/bin/bash

main() {
  case $1 in
  "")
    echo "Kindly supply a command" && exit 0
    ;;
  move)
    echo "Tarring the ball..."
    pushd .. && tar -cvf phcode42v2/phcode42v2.tgz -X phcode42v2/exclude_files.txt phcode42v2/* && popd
    echo "Moving to remote..."
    sshpass -p "phantom" scp phcode42v2.tgz "phantom@${PHANTOM_VM_IP_ADDR}":/home/phantom
    echo "Untarring on remote..."
    sshpass -p "phantom" ssh phantom@10.0.0.41 "rm -rf phcode42v2 && tar -xvf phcode42v2.tgz && cd phcode42v2 && phenv python /opt/phantom/bin/compile_app.pyc -i"
    ;;
  *)
    echo "Not a valid command" && exit 0
  esac
}

main "$@"