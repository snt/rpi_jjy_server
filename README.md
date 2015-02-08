40khz JJY server for Raspberry Pi
=================================

JJY server is time synchronization server in Japan, [emitting 40khz or 60khz signals](http://jjy.nict.go.jp/jjy/trans/).

We use [RPIO](https://pythonhosted.org/RPIO/pwm_py.html) to use PWM.

setup
=====

software
--------

```sh
sudo pip install RPIO
```

hardware
--------

We use almost same configuration as [an article of Nikke Computer](http://itpro.nikkeibp.co.jp/atcl/column/14/093000080/093000002/?ST=oss&P=6).

* a 30k ohm resistor
* a LED
* a 2SC1815
* long wire (as an antenna). 

```
GPIO4 (pin7) -> 30k ohm resistor -> base of 2SC1815

GND   (pin6) -> emitter of 2SC1815

VCC   (pin2) -> LED -> collector of 2SC1815
                    -> long wire
```

run
===

```sh
sudo python jjy.py
```

This transmits JJY signals from the 0 second of next minute.  Put your JJY compatible clock near to the antenna, push sync button or so, and wait for it.


