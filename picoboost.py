import machine
import time

# set up analog input pin
pot_pin = machine.ADC(26)

# set up digital input pin for button
button_pin = machine.Pin(10, machine.Pin.IN, machine.Pin.PULL_UP)

# set up digital output pin for LED
red_led_pin = machine.Pin(19, machine.Pin.OUT)
green_led_pin = machine.Pin(20, machine.Pin.OUT)
blue_led_pin = machine.Pin(21, machine.Pin.OUT)


# set hysteresis value
hysteresis = 2

# check if potentiometer is at 0% before initializing main loop
while True:
    # read voltage from analog input pin
    voltage = pot_pin.read_u16() / 65535 * 3.3

    # convert voltage to percentage and round to nearest multiple of 10
    percentage = round((3.3 - voltage) / 3.3 * 100 / 10) * 10

    if percentage == 0:
        break

    # print warning message if potentiometer is not at 0%
    print("Warning! Boost not idle!")

    time.sleep(0.1)

# initialize percentage, prev_percentage, and flash_speed to None
percentage = None
prev_percentage = None
flash_speed = None

# initialize button state and prev_button_state to False
button_state = False
prev_button_state = False

while True:
    # read voltage from analog input pin
    voltage = pot_pin.read_u16() / 65535 * 3.3

    # convert voltage to percentage and round to nearest multiple of 10
    percentage = round((3.3 - voltage) / 3.3 * 100 / 10) * 10

    # read state of button
    button_state = button_pin.value()

    # convert button state to "Active" or "off"
    button_text = "-" if button_state else "Active"

    # check if percentage has changed by more than hysteresis since the last reading
    # or if the button state has changed since the last reading
    if (
        prev_percentage is None
        or abs(percentage - prev_percentage) >= hysteresis
        or button_state != prev_button_state
    ):
        # calculate flash speed based on percentage (0% = 0.1 seconds, 100% = 0.01 seconds)
        flash_speed = 0.2 - (percentage / 1000)

        # print percentage and button state to serial console
        print("Boost: {:.0f}%, Rolling Anti-lag: {}".format(percentage, button_text))

        # update prev_percentage and prev_button_state to the current values
        prev_percentage = percentage
        prev_button_state = button_state

    # toggle LED state every flash_speed seconds
    blue_led_pin.toggle()
    time.sleep(flash_speed)
