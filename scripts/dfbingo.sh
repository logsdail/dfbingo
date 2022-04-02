#!/bin/bash
#
export LD_LIBRARY_PATH=/home/andrew/Software/libxc-5.1.3/install/lib
export PYTHONPATH="/home/andrew/Software/libxc-5.1.3/:$PYTHONPATH"

python3 /home/andrew/Software/github/dfbingo/main.py --tweet 
