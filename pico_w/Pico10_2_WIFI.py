import network
import time

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.disconnect()
#wlan.connect('Robert_iPhone','0926656')
wlan.connect('LondonChu','78787878')

#等待連線或失敗
#status = 0,1,2 正在連線
#status = 3 連線成功
#<0,>3失敗的連線

max_wait = 40
while max_wait>0:
    status = wlan.status()
    if status < 0 or status >=3:
        break
    max_wait-=1
    print("等待連線...")
    time.sleep(1)
    
print(wlan.ifconfig())
print(status)
print(wlan.isconnected())