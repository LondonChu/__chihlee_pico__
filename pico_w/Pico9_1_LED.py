#from datetime import datetime,timedelta
#now=datetime.now()
#nowNext=now+timedelta(seconds=1)

#count=0
#while datetime.now()<nowNext:
#      count+=1
   
#print(f"{now}")
#print(f"{nowNext}")
#print(f"{count}")

import time
from machine import Pin

led = Pin("LED",Pin.OUT)

while True:
    led.high()
    time.sleep(1)
    led.low()
    time.sleep(1)
    