'''run this to find the recognized devices connected to the Pi, and their respective paths, if needed'''


import evdev

devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
for device in devices:
    print(device.path, device.name, device.phys)
