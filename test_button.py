from machine import Pin
import time

debounceTime = 20 #ms debouncing time to prevent flickering

DCwaiting = False #whether waiting for double click
DCregister = False #whether to register a double click
SCregister = False #whether to register a single click
ignoreRelease = False #whether to ignore the release as long press is triggered
longPressPast = False #whether the long press has already happened
buttonLast = 0 #button's previous state

downTime = -1 #time the button was pressed down
upTime = -1 #time the button was released

long_press_duration = 800
DC_gap = 800

event = 0

def check_botton(btn):
    global debounceTime
    global DCwaiting
    global DCregister
    global SCregister
    global ignoreRelease
    global longPressPast
    global buttonLast
    global downTime
    global upTime
    global event

    event = 0

    #read state of the button
    btnVal = btn.value()
    
    #button is pressed down
    if btnVal == 1 and buttonLast == 0 and (time.ticks_ms() - upTime) > debounceTime:
        downTime = time.ticks_ms()
        SCregister = True
        ignoreRelease = False
        longPressPast = False
        if (time.ticks_ms() - upTime) <= DC_gap and DCregister == False and DCwaiting == True:
            DCregister = True
        else:
            DCregister = False
        DCwaiting = False
       
    #button is released
    elif btnVal == 0 and buttonLast == 1 and (time.ticks_ms() - downTime) > debounceTime:
        if not ignoreRelease:
            upTime = time.ticks_ms()
            if DCregister == False:
                DCwaiting = True 
            #double click is tiggered
            else:
                event = 2
                DCregister = False
                DCwaiting = False
                SCregister = False
                
    #test for single click
    if btnVal == 0 and (time.ticks_ms() - upTime) > DC_gap and DCwaiting == True and DCregister == False and SCregister == True and longPressPast == False:
        event = 1
        DCwaiting = False
   
    #test for long press
    if btnVal == 1 and (time.ticks_ms() - downTime) > long_press_duration:
        #long press is tiggered
        if not longPressPast:
            event = 3
            waitForUp = True
            ignoreUp = True
            DCregister = False
            DCwaiting = False
            longPressPast = True

    buttonLast = btnVal    
  
while True:
    btn = Pin("PA_17", Pin.IN)
    led_pin = Pin("PA_9", Pin.OUT)
    #initiate led as OFF
    led_pin.value(0)
    check_botton(btn)
    if event == 1:
        #blink once
        print("Single click detected!")
        led_pin.value(1)
        time.sleep_ms(500)
        led_pin.value(0)
    elif event == 2:
        #blink twice
        print("Double click detected!")
        led_pin.value(1)
        time.sleep_ms(500)
        led_pin.value(0)
        time.sleep_ms(500)
        led_pin.value(1)
        time.sleep_ms(500)
        led_pin.value(0)
    elif event == 3:
        #blink for 3 sec
        print("Long press detected!")
        led_pin.value(1)
        time.sleep(3)
        led_pin.value(0)
