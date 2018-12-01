import gc
import ujson
import network
from utime import sleep
from utime import sleep_ms
from machine import Pin, reset
from neopixel import NeoPixel
from umqtt.robust import MQTTClient


with open("./config.json") as fp:
    config = ujson.load(fp)

pin = Pin(config["neopixel_pin"], Pin.OUT) 
np = NeoPixel(pin, 24)

heartbeat = Pin(2, Pin.OUT)  # Pin 2 is connected to the blue LED on Wemos board

client = MQTTClient(config["mqtt_client"], config["mqtt_server"])

############## Here we go then #################

def goLamp():
    client.set_callback(do_callback)

    if not client.connect(clean_session=True):
        print("New session being set up")
        client.subscribe(config["mqtt_topic"])

    while 1:
        try:
            client.wait_msg() 
        finally:
            client.disconnect()
        gc.collect()


def do_callback(topic, msg):
    value = str(msg, "utf-8")
    print("value: " + value)
    splitval = value.split(",")
    red = int(splitval[0])
    green = int(splitval[0])
    blue = int(splitval[0])
    lampcolour = (red, green, blue)
    np.fill(lampcolour)
    np.write


# If we are being imported as a module then do nothing
# If we are being run as a script then run
if __name__ == '__main__':
    gc.enable()
    
    sta_if = network.WLAN(network.STA_IF)

    while not sta_if.isconnected():
        print("Not connected to WiFi")
        sleep(5)
    
    try:
        goLamp()
    except Exception as e:
        print("Something has gone horribly wrong")
        print(e)
        sleep(10)
        reset()
