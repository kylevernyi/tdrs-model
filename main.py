import time
import utime
import _thread
import network
import socket
import struct
from machine import Pin, Timer, PWM

STAT_GOT_IP = 3

# wifi
ssid = 'my_wifi_names'
password = 'my_wifi_password'
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
udp_dest_port = 5005
udp_ip="192.168.1.202"
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# LED
onboard_led = Pin("LED", Pin.OUT)
red_led = Pin(10, Pin.OUT)
green_led = Pin(0, Pin.OUT)
debug_led = Pin(7, Pin.OUT)

# timers
tim = Timer()
tim2 = Timer()
tim3 = Timer()
pwm_tim = Timer()
temp_tim = Timer()

#PWM
pwm = PWM(Pin(3))
pwm.freq(1000)
duty = 0
direction = 1

# temperature sensors
sensor_temp = machine.ADC(4)
temp_conversion_factor = 3.3 / (65535)

def failed_to_connect():
    global red_led
    red_led.toggle()
    

def toggle_onboard_led(timer):
    global onboard_led
    onboard_led.toggle()
    
def toggle_external_red_led(timer):
    global red_led
    red_led.toggle()
        
def toggle_external_green_led(timer):
    global green_led
    green_led.toggle()
    
def pwm_loop(timer):
    global duty, direction
    
    duty += direction
    
    if duty > 255:
        duty= 255
        direction = -1
    elif duty < 0:
        duty = 0
        direction = 1
    
    pwm.duty_u16(duty*duty)
        
def read_temperature(timer):
    global debug_led
    
    reading = sensor_temp.read_u16() * temp_conversion_factor
    # The temperature sensor measures the Vbe voltage of a biased bipolar diode, connected to the fifth ADC channel
    # Typically, Vbe = 0.706V at 27 degrees C, with a slope of -1.721mV (0.001721) per degree.
    temperature = 27 - (reading - 0.706)/0.001721
    debug_led.toggle()
    
    data_struct = struct.pack('!f', temperature)  
    sock.sendto(data_struct, (udp_ip, udp_dest_port))       

    
def main():
    # connect to wifi
    wlan.connect(ssid, password)
    max_wait = 60
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= STAT_GOT_IP:
            failed_to_connect()
        max_wait -= 1
        time.sleep(1)

    if (wlan.status() != STAT_GOT_IP):
        # red led shows could not connect to wifi
        tim2.init(freq=3.5, mode=Timer.PERIODIC, callback=toggle_external_red_led)
        return

    sock.connect((udp_ip, udp_dest_port))
    
    # init blinking of various LEDs
    tim.init(freq=2.5, mode=Timer.PERIODIC, callback=toggle_onboard_led)
    tim2.init(freq=3.5, mode=Timer.PERIODIC, callback=toggle_external_red_led)
    tim3.init(freq=1.5, mode=Timer.PERIODIC, callback=toggle_external_green_led)
    pwm_tim.init(freq=45, mode=Timer.PERIODIC, callback=pwm_loop)
    
    # start reading temperature
    temp_tim.init(freq=1, mode=Timer.PERIODIC, callback=read_temperature)
    

    
    
if __name__=="__main__":
    main()