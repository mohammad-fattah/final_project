import schedule 
import time 
import os

def run_python_code(): 
    os.system("python query.py")
   
schedule.every(30).minutes.do(run_python_code)
while True: 
  
    schedule.run_pending() 
    time.sleep(1) 
