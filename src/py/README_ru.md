# pwm manage

pwm manage - это отдельный программный модуль необходимый для управления GPIO RPI

## Install

```shell script
pip install .
```
# Start driver

```shell script
pwm start
```
# Test run platform 

- ```engines``` количество двигателей: 4 (выберите 2 или 4)
- ```w-time``` кремя выполнения одной комманды (в секундах)
- ```power``` мощность двигателей (в процентах)

```shell
pwm test --engines 4 --w-time 1 --power 25
```