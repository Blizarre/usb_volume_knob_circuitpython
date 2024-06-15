import rotaryio
from microcontroller import pin 
import digitalio
import usb_hid
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_debouncer import Button

from time import time

def debounce_button(gpio_pin):
    button = digitalio.DigitalInOut(gpio_pin)
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP
    return Button(button)

previous_button = debounce_button(pin.GPIO26)
next_button = debounce_button(pin.GPIO20)

playpause_button = debounce_button(pin.GPIO4)

encoder = rotaryio.IncrementalEncoder(pin.GPIO2, pin.GPIO3)

usb_consumer = ConsumerControl(usb_hid.devices)


last_position = encoder.position
while True:
    playpause_button.update()
    previous_button.update()
    next_button.update()
    
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

    if playpause_button.short_count >= 1:
        print("Button short-pressed")
        usb_consumer.send(ConsumerControlCode.PLAY_PAUSE)

    if next_button.short_count >= 1:
            print("Next Button short-pressed")
            usb_consumer.send(ConsumerControlCode.SCAN_NEXT_TRACK)

    if previous_button.short_count >= 1:
            print("Previous Button short-pressed")
            # Yes, I REALLY want to go to the previous track, not just go to the
            # beginning of the current track
            usb_consumer.send(ConsumerControlCode.SCAN_PREVIOUS_TRACK)
            usb_consumer.send(ConsumerControlCode.SCAN_PREVIOUS_TRACK)
