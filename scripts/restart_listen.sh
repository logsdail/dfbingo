#!/bin/bash
#

ids=`ps -ef | grep bash | grep dflisten | awk {' print $2 }'`  # head -1 | xargs kill
echo "listen ids: $ids"
while test $(echo $ids | wc -w) -gt 0; do
 ps -ef | grep bash | grep dflisten | awk {' print $2 }' | head -1 | xargs kill
 ids=`ps -ef | grep bash | grep dflisten | awk {' print $2 }'`  # head -1 | xargs kill
done

ids=`ps -ef | grep python3 | grep main | grep listen |awk {' print $2 }'`  # head -1 | xargs kill
echo "listen ids: $ids"
while test $(echo $ids | wc -w) -gt 0; do
 ps -ef | grep python3 | grep main | grep listen | awk {' print $2 }' | head -1 | xargs kill
 ids=`ps -ef | grep python3 | grep main | grep listen | awk {' print $2 }'`  # head -1 | xargs kill
done

echo "Restarting dflisten"
nohup ./dflisten.sh &
