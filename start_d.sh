
app=${1:-"app.py"} 
echo $app
ps -ef | grep $app | grep -v "grep" | awk '{print $2}' | xargs kill -9
sleep 2
nohup python $app  >> nohup.log  2>&1 &

