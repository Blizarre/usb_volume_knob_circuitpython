import digitalio

import storage, usb_cdc, usb_midi
import usb_hid

import pins

# disable all the extra USB peripherals UNLESS the playpause button is pressed at boot time
button = digitalio.DigitalInOut(pins.PLAYPAUSE)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

# Disable devices only if button is not pressed (default UP).
if button.value:
    storage.disable_usb_drive()
    usb_cdc.disable()
    usb_midi.disable()

    usb_hid.enable(
        (usb_hid.Device.CONSUMER_CONTROL,)
    )  # Do not enable any of the other hid
