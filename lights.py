from pyHS100 import SmartPlug
import keys

plug = SmartPlug(keys.lightsip)
print("Current state: %s" % plug.state)


def on():
    plug.turn_on()
    return plug.state


def off():
    plug.turn_off()
    return plug.state


def invert():
    if plug.state.upper() == 'ON':
        plug.turn_off()
    elif plug.state.upper() == 'OFF':
        plug.turn_on()
    return plug.state
