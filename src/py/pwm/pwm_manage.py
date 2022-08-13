"""
It's a simple script to set up pwm engine
"""
import typer
import toml
import os
from .default_config import def_config
# from .motor_drives import *
from .websocketruner import *
from .test import *

app = typer.Typer(help="Awesome CLI IPMP universal tool.")

import logging
from systemd.journal import JournaldLogHandler

logger = logging.getLogger("pwm_manage")
journald_handler = JournaldLogHandler()

# set a formatter to include the level name
journald_handler.setFormatter(logging.Formatter(
    '[%(levelname)s] %(message)s'
))

# add the journald handler to the current logger
logger.addHandler(journald_handler)
logger.addHandler(logging.StreamHandler())

# optionally set the logging level
logger.setLevel(logging.DEBUG)


@app.command()
def init():
    """
    Create config.toml file

    Example of using:
    pwm init
    """
    if not os.path.isfile("config.toml"):
        print(f"Generate config.toml config file")
        with open("config.toml", 'w') as f:
            f.write(def_config)


@app.command()
def start(conf: str = typer.Option("/etc/pwm/config.toml", help="PWM config.", show_default=True)
          ):
    """
    Use for the start PWM manager 

    Example of using:
    pwm start --conf=/etc/pwm/config.toml
    """
    config: str

    if conf is None:
        if os.path.isfile("./config.toml"):
            config = "./config.toml"
        if not os.path.isfile("./config.toml"):
            print("Config file not exists!")
            exit(2)
    if conf is not None:
        config = conf

    config = toml.load(config)
    print("Awaiting control command...")
    if config['pwm_type'] == "L9110S":
        L9110S.logger = logger
        L9110S.channels = config['outputs']
        engine = L9110S
        runner = WebSoketRunner(logger=logger, engine=engine)
        runner.start()

    elif config['pwm_type'] == "L298N":
        L298N.logger = logger
        L298N.channels = config['outputs']
        engine = L298N
        runner = WebSoketRunner(logger=logger, engine=engine)
        runner.start()

    elif config['pwm_type'] == "DL298N":
        DL298N.logger = logger
        DL298N.channels = config['outputs']
        engine = DL298N
        runner = WebSoketRunner(logger=logger, engine=engine)
        runner.start()

    elif config['pwm_type'] == "DL298NU":
        DL298NU.logger = logger
        DL298NU.channels = config['outputs']
        engine = DL298NU
        runner = WebSoketRunner(logger=logger, engine=engine)
        runner.start()

    else:
        logger.error(f'Wrong config!')


@app.command()
def test(engines: int = typer.Option(2, help="Use 2 or 4 engines", show_default=True),
         w_time: int = typer.Option(2, help="Waiting time", show_default=True),
         power: int = typer.Option(50, help="Power %", show_default=True)
         ):
    """
    Use for the test engines

    Example of using:
    pwm test --engines 4 --w-time 1 --power 25
    """
    v_power = str(power/100)
    test_ws = Test_WS(engines, w_time, v_power)
    test_ws.run()


if __name__ == '__main__':
    app()
