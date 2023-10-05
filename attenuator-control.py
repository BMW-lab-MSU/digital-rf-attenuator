from machine import Pin, Timer
import utime

#Controls Digital Step Attenuator: ZX76-31R5A-SPS+
#Using a Rhasberry Pi Pico 
#must be saved as main.py to run on power up            <----!!!
clock_pin = Pin(0, Pin.OUT)
data_pin  = Pin(1, Pin.OUT)
latch_pin = Pin(2, Pin.OUT)
clock_pin.value(0)
data_pin.value(0)
latch_pin.value(0)
latch = False

#adding ones to the values stored in data turns on different attenuation states.
#you must combine attenuation states to achieve your desired attenuation
# data = [0,0,0,0,0,0] #reference
# data = [0,0,0,0,0,1] #.5dB
# data = [0,0,0,0,1,0] #1dB
# data = [0,0,0,1,0,0] #2dB
# data = [0,0,1,0,0,0] #4dB
# data = [0,1,0,0,0,0] #8dB
# data = [1,0,0,0,0,0] #16dB
# data = [1,1,1,1,1,1] #31.5dB

#eg. setting data = [0,1,0,0,1,1] would yeild an attenuation of 8dB + 1dB + .5dB= 9dB 

data_index = 0

timer = Timer()

#sends data, latches data. If the attenuator stops being 
#sent control commands, it will return to reference mode (0dB)
def clockGen(timer):
    global data_index, latch, data
    data_pin.value(data[data_index])
    utime.sleep_ms(10)
    latch_pin.value(0)
    
    if(clock_pin.value() == 1):
        data_index = data_index + 1        
        
    if(latch):
        latch_pin.toggle()
        latch = False

    if(data_index >= 6):
        data_index = 0
        latch = True

    clock_pin.toggle()

#you should probably lower the amount of time it waits before it starts to controll the attenuator, but i didn't test lower times so this is what it is for now
#the maximum frequency the attenuator wants is 10MHz. This is obviously well below that. Like the sleep time, I haven't had time to test faster frequencies. 
utime.sleep(1)
timer.init(freq=2, mode=Timer.PERIODIC, callback=clockGen)


