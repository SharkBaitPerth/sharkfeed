"""Test for publisher that remains connected."""
import time
import paho.mqtt.client as mqtt
from random import randint

mqttc=mqtt.Client()
mqttc.connect("52.62.201.125", 1883, 60)
mqttc.loop_start()

def test_publish():
    return randint(1, 10)

while True:
    value = test_publish()
    (result,mid) = mqttc.publish("$test", value, 2)
    print(value, result, mid)
    time.sleep(1)

mqttc.loop_stop()
mqttc.disconnect()
