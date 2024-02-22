import evdev

device = evdev.InputDevice('/dev/input/event12')
print(device)


for event in device.read_loop():
    if event.type == evdev.ecodes.EV_KEY or evdev.ecodes.EV_ABS:
        print(evdev.categorize(event))
