# Rex Control

## Wiring Rex

Connect the motor driver board to Raspberry Pi.

There are 6 pins on the motor driver: enable1, enable2, in1, in2, in3, and in4. They should be connected to the Raspberry Pi's digital pins (BCM notation) 4, 22, 2, 3, 17, 27, respectively.

<img src="https://www.elegoo.com/wp-content/uploads/2017/01/3-17.jpg" width="500">

From `rex_motor.py`, the pins are

```
class RabbitMotor:
    PIN_IN1 = 2
    PIN_IN2 = 3
    PIN_EN1 = 4
    PIN_IN3 = 17
    PIN_IN4 = 27
    PIN_EN2 = 22
```

![alt text](https://i.pinimg.com/originals/23/12/01/23120159f5e87a302de7d3ab88cf27f1.jpg "Raspberry pi pinout")

Figure 1: *Pinout of Raspberry Pi 2*
