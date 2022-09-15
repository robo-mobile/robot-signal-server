# pwm manage

pwm manage - this is a separate software module needed to control GPIO RPI ([RU](./README_ru.md))

## Install

```shell script
pip install .
```
# Start driver

```shell script
pwm start
```
# Test run platform 
- ``engines`` number of engines: 4 (choose 2 or 4)
- ``w-time``, time of execution of one command (in seconds)
- ``power``, the power of the motors (in percent)

```shell
pwm test --engines 4 --w-time 1 --power 25
```
