#!/bin/bash
#

echo "Killing previous instance of xclisten"
ids=`ps -ef | grep xclisten | awk {' print $2 }'`  # head -1 | xargs kill
echo "xclisten ids: $ids"
while test $(echo $ids | wc -w) -gt 3; do
 ps -ef | grep xclisten | awk {' print $2 }' | head -1 | xargs kill
 ids=`ps -ef | grep xclisten | awk {' print $2 }'`  # head -1 | xargs kill
done

ids=`ps -ef | grep python3 | grep listen | awk {' print $2 }'`  # head -1 | xargs kill
echo "Python3 | listen ids: $ids"
while test $(echo $ids | wc -w) -gt 1; do
 ps -ef | grep python3 | grep listen | awk {' print $2 }' | head -1 | xargs kill
 ids=`ps -ef | grep python3 | grep listen | awk {' print $2 }'`  # head -1 | xargs kill
done

echo "Restarting xclisten"
nohup ~/.xclisten.sh &
