import rotaryio
from microcontroller import pin 
import digitalio
import usb_hid
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_debouncer import Button

from time import time

io_button = digitalio.DigitalInOut(pin.GPIO4)
io_button.direction = digitalio.Direction.INPUT
io_button.pull = digitalio.Pull.UP

button = Button(io_button)

encoder = rotaryio.IncrementalEncoder(pin.GPIO2, pin.GPIO3)

usb_consumer = ConsumerControl(usb_hid.devices)


last_position = encoder.position
while True:
    button.update()
    current_position = encoder.position
    encoder_change = current_position - last_position
    if encoder_change > 0:
        for _ in range(encoder_change):
            usb_consumer.send(ConsumerControlCode.VOLUME_INCREMENT)
        print(current_position)
    elif encoder_change < 0:
        for _ in range(-encoder_change):
            usb_consumer.send(ConsumerControlCode.VOLUME_DECREMENT)
        print(current_position)
    
    last_position = current_position

    if button.long_press:
        print("Button long-pressed")
        usb_consumer.send(ConsumerControlCode.SCAN_NEXT_TRACK)
    if button.short_count >= 1:
        print("Button short-pressed")
        usb_consumer.send(ConsumerControlCode.PLAY_PAUSE)


