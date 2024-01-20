from machine import Pin
import time

#GP15是LED
red_led = Pin(15,mode=Pin.OUT)

#0是關燈 1是開燈
#red_led.value(0)

#GP14是開關
btn = Pin(14,mode=Pin.PULL_DOWN)

#方法一
#while True:
#    btnValue=btn.value()
#    red_led.value(btnValue)    
#    print(btnValue)
#    time.sleep_ms(500)

#方法二
#while True:
#    if btn.value():
#        red_led.value(1)
#    else:
#        red_led.value(0)


#switch button
#解決彈跳
is_press = False
led_status = False

while True:
    if btn.value():
        time.sleep_ms(50)
        if btn.value():
            is_press = True
    elif is_press:
        time.sleep_ms(50)
        if btn.value() == False:
            print('release')
            led_status = not led_status        
            red_led.value(led_status)        
            is_press = False
            
    
