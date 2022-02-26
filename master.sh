

while :
do
  python3 main.py
  sleep 8*60*60
  ps -ef | grep -v grep | grep python3 | awk '{print $2}' | xargs kill -9
done


