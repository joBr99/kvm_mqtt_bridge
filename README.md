# Homeassistant MQTT Bridge for Ali NoName KVM Switch (XH-HK4401)

![image](https://user-images.githubusercontent.com/29555657/170509924-150d5e63-e66b-427a-8ce5-b1deb907a3dd.png)

https://www.aliexpress.com/item/4000006937156.html?spm=a2g0o.order_list.0.0.21ef18027XWq0n

The control micro-usb port on the kvm switch isn't really usb it is rs232 at 5V. However the logic levels of the RX/TX signals are inverted. The easiest solution for this is to get a serial adater that supports this rare feature like the FTDI FT232.

# Program FTDI FT232 on Windows

In order to invert the RX/TX signals, you can use ft_prog and set the following settings:

![image](https://user-images.githubusercontent.com/29555657/170510654-262dde34-40ab-4ab1-8c3b-1caa402c2940.png)


# Conntect FTDI to KVM Switch

| Signal | Color  | FT232 Pin |
|--------|--------|-----------|
| VCC    | red    | -         |
| D-     | white  | RX        |
| D+     | green  | Tx        |
| GND    | black  | GND       |
