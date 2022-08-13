import RPi.GPIO as GPIO

"""
 RPI 3 B+ GPIO MAP 
 +-----+-----+---------+------+---+---Pi 3B--+---+------+---------+-----+-----+
 | BCM | wPi |   Name  | Mode | V | Physical | V | Mode | Name    | wPi | BCM |
 +-----+-----+---------+------+---+----++----+---+------+---------+-----+-----+
 |     |     |    3.3v |      |   |  1 || 2  |   |      | 5v      |     |     |
 |   2 |   8 |   SDA.1 |   IN | 1 |  3 || 4  |   |      | 5v      |     |     |
 |   3 |   9 |   SCL.1 |   IN | 1 |  5 || 6  |   |      | 0v      |     |     |
 |   4 |   7 | GPIO. 7 |   IN | 1 |  7 || 8  | 0 | IN   | TxD     | 15  | 14  |
 |     |     |      0v |      |   |  9 || 10 | 1 | IN   | RxD     | 16  | 15  |
 |  17 |   0 | GPIO. 0 |   IN | 0 | 11 || 12 | 0 | IN   | GPIO. 1 | 1   | 18  |
 |  27 |   2 | GPIO. 2 |   IN | 0 | 13 || 14 |   |      | 0v      |     |     |
 |  22 |   3 | GPIO. 3 |   IN | 0 | 15 || 16 | 0 | IN   | GPIO. 4 | 4   | 23  |
 |     |     |    3.3v |      |   | 17 || 18 | 0 | IN   | GPIO. 5 | 5   | 24  |
 |  10 |  12 |    MOSI |   IN | 0 | 19 || 20 |   |      | 0v      |     |     |
 |   9 |  13 |    MISO |   IN | 0 | 21 || 22 | 0 | IN   | GPIO. 6 | 6   | 25  |
 |  11 |  14 |    SCLK |   IN | 0 | 23 || 24 | 1 | IN   | CE0     | 10  | 8   |
 |     |     |      0v |      |   | 25 || 26 | 0 | OUT  | CE1     | 11  | 7   |
 |   0 |  30 |   SDA.0 |   IN | 1 | 27 || 28 | 1 | IN   | SCL.0   | 31  | 1   |
 |   5 |  21 | GPIO.21 |  OUT | 0 | 29 || 30 |   |      | 0v      |     |     |
 |   6 |  22 | GPIO.22 |  OUT | 0 | 31 || 32 | 0 | OUT  | GPIO.26 | 26  | 12  |
 |  13 |  23 | GPIO.23 |  OUT | 0 | 33 || 34 |   |      | 0v      |     |     |
 |  19 |  24 | GPIO.24 |  OUT | 0 | 35 || 36 | 0 | OUT  | GPIO.27 | 27  | 16  |
 |  26 |  25 | GPIO.25 |  OUT | 0 | 37 || 38 | 0 | OUT  | GPIO.28 | 28  | 20  |
 |     |     |      0v |      |   | 39 || 40 | 0 | OUT  | GPIO.29 | 29  | 21  |
 +-----+-----+---------+------+---+----++----+---+------+---------+-----+-----+
 | BCM | wPi |   Name  | Mode | V | Physical | V | Mode | Name    | wPi | BCM |
 +-----+-----+---------+------+---+---Pi 3B--+---+------+---------+-----+-----+
"""


class driver:
    logger: object
    channels: dict

    def __init__(self):
        for key, value in self.channels.items():
            setattr(self, key, value)


class L9110S(driver):

    def __init__(self):

        super().__init__()
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        GPIO.setup(self.channel1, GPIO.OUT)
        GPIO.setup(self.channel2, GPIO.OUT)
        GPIO.setup(self.channel3, GPIO.OUT)
        GPIO.setup(self.channel4, GPIO.OUT)

        self.pwm_channel1 = GPIO.PWM(self.channel1, 1000)
        self.pwm_channel2 = GPIO.PWM(self.channel2, 1000)
        self.pwm_channel3 = GPIO.PWM(self.channel3, 1000)
        self.pwm_channel4 = GPIO.PWM(self.channel4, 1000)

        self.pwm_channel1.stop()
        self.pwm_channel2.stop()
        self.pwm_channel3.stop()
        self.pwm_channel4.stop()

    def pwm_controller(self, manage_list):
        left, right = manage_list
        left = int(left * 100)
        right = int(right * 100)
        self.logger.debug(f'left : {left}, right : {right}')

        if left >= 0 and right >= 0:
            self.pwm_channel1.start(abs(left))
            self.pwm_channel2.stop()
            self.pwm_channel3.start(abs(right))
            self.pwm_channel4.stop()

        elif left < 0 and right < 0:

            self.pwm_channel1.stop()
            self.pwm_channel2.start(abs(left))
            self.pwm_channel3.stop()
            self.pwm_channel4.start(abs(right))

        elif left >= 0 and right < 0:

            self.pwm_channel1.start(abs(left))
            self.pwm_channel2.stop()
            self.pwm_channel3.stop()
            self.pwm_channel4.start(abs(right))

        elif left < 0 and right >= 0:

            self.pwm_channel1.stop()
            self.pwm_channel2.start(abs(left))
            self.pwm_channel3.start(abs(right))
            self.pwm_channel4.stop()

        elif left == 0 and right == 0:

            self.pwm_channel1.stop()
            self.pwm_channel2.stop()
            self.pwm_channel3.stop()
            self.pwm_channel4.stop()


class L298N(driver):

    def __init__(self):

        super().__init__()
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        GPIO.setup(self.enA, GPIO.OUT)
        GPIO.setup(self.enB, GPIO.OUT)
        GPIO.setup(self.channel1, GPIO.OUT)
        GPIO.setup(self.channel2, GPIO.OUT)
        GPIO.setup(self.channel3, GPIO.OUT)
        GPIO.setup(self.channel4, GPIO.OUT)

        GPIO.output(self.channel1, GPIO.LOW)
        GPIO.output(self.channel2, GPIO.LOW)
        GPIO.output(self.channel3, GPIO.LOW)
        GPIO.output(self.channel4, GPIO.LOW)

        self.pwm_enA = GPIO.PWM(self.enA, 1000)
        self.pwm_enB = GPIO.PWM(self.enB, 1000)

        self.pwm_enA.stop()
        self.pwm_enB.stop()

    def pwm_controller(self, manage_list: list):
        left, right = manage_list
        left = int(left * 100)
        right = int(right * 100)
        self.logger.debug(f'left : {left} right : {right}')

        if left >= 0 and right >= 0:

            self.pwm_enA.start(abs(left))
            GPIO.output(self.channel1, GPIO.HIGH)
            GPIO.output(self.channel2, GPIO.LOW)

            self.pwm_enB.start(abs(right))
            GPIO.output(self.channel3, GPIO.HIGH)
            GPIO.output(self.channel4, GPIO.LOW)


        elif left < 0 and right < 0:

            self.pwm_enA.start(abs(left))
            GPIO.output(self.channel1, GPIO.LOW)
            GPIO.output(self.channel2, GPIO.HIGH)

            self.pwm_enB.start(abs(right))
            GPIO.output(self.channel3, GPIO.LOW)
            GPIO.output(self.channel4, GPIO.HIGH)

        elif left >= 0 and right < 0:

            self.pwm_enA.start(abs(left))
            GPIO.output(self.channel1, GPIO.HIGH)
            GPIO.output(self.channel2, GPIO.LOW)

            self.pwm_enB.start(abs(right))
            GPIO.output(self.channel3, GPIO.LOW)
            GPIO.output(self.channel4, GPIO.HIGH)

        elif left < 0 and right >= 0:

            self.pwm_enA.start(abs(left))
            GPIO.output(self.channel1, GPIO.LOW)
            GPIO.output(self.channel2, GPIO.HIGH)

            self.pwm_enB.start(abs(right))
            GPIO.output(self.channel3, GPIO.HIGH)
            GPIO.output(self.channel4, GPIO.LOW)

        elif left == 0 and right == 0:

            self.pwm_enA.stop()
            GPIO.output(self.channel1, GPIO.LOW)
            GPIO.output(self.channel2, GPIO.LOW)

            self.pwm_enB.stop()
            GPIO.output(self.channel3, GPIO.LOW)
            GPIO.output(self.channel4, GPIO.LOW)


class DL298N(driver):
    """Колеса Илона"""

    def __init__(self, *args, **kwargs):
        super().__init__()

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        GPIO.setup(self.enA1, GPIO.OUT)
        GPIO.setup(self.enB1, GPIO.OUT)
        GPIO.setup(self.channel11, GPIO.OUT)
        GPIO.setup(self.channel12, GPIO.OUT)
        GPIO.setup(self.channel13, GPIO.OUT)
        GPIO.setup(self.channel14, GPIO.OUT)

        GPIO.setup(self.enA2, GPIO.OUT)
        GPIO.setup(self.enB2, GPIO.OUT)
        GPIO.setup(self.channel21, GPIO.OUT)
        GPIO.setup(self.channel22, GPIO.OUT)
        GPIO.setup(self.channel23, GPIO.OUT)
        GPIO.setup(self.channel24, GPIO.OUT)

        GPIO.output(self.channel11, GPIO.LOW)
        GPIO.output(self.channel12, GPIO.LOW)
        GPIO.output(self.channel13, GPIO.LOW)
        GPIO.output(self.channel14, GPIO.LOW)

        GPIO.output(self.channel21, GPIO.LOW)
        GPIO.output(self.channel22, GPIO.LOW)
        GPIO.output(self.channel23, GPIO.LOW)
        GPIO.output(self.channel24, GPIO.LOW)

        self.pwm_enA1 = GPIO.PWM(self.enA1, 1000)
        self.pwm_enB1 = GPIO.PWM(self.enB1, 1000)

        self.pwm_enA2 = GPIO.PWM(self.enA2, 1000)
        self.pwm_enB2 = GPIO.PWM(self.enB2, 1000)

        self.pwm_enA1.stop()
        self.pwm_enB1.stop()
        self.pwm_enA2.stop()
        self.pwm_enB2.stop()

    def pwm_controller(self, manage_list: list):
        a_left, a_right, b_left, b_right = manage_list
        a_left = int(a_left * 100)
        a_right = int(a_right * 100)
        b_left = int(b_left * 100)
        b_right = int(b_right * 100)
        self.logger.debug(f'a_left : {a_left}, a_right : {a_right}, b_left : {b_left}, b_right : {b_right}')

        if a_left >= 0 and a_right >= 0 and b_left >= 0 and b_right >= 0:
            """
            Прямо вперед 
            """

            self.pwm_enA1.start(abs(a_left))
            GPIO.output(self.channel11, GPIO.HIGH)
            GPIO.output(self.channel12, GPIO.LOW)

            self.pwm_enA2.start(abs(b_left))
            GPIO.output(self.channel21, GPIO.HIGH)
            GPIO.output(self.channel22, GPIO.LOW)

            self.pwm_enB1.start(abs(a_right))
            GPIO.output(self.channel13, GPIO.HIGH)
            GPIO.output(self.channel14, GPIO.LOW)

            self.pwm_enB2.start(abs(b_right))
            GPIO.output(self.channel23, GPIO.HIGH)
            GPIO.output(self.channel24, GPIO.LOW)



        elif a_left < 0 and a_right < 0 and b_left < 0 and b_right < 0:
            """
            Прямо назад
            """

            self.pwm_enA1.start(abs(a_left))
            GPIO.output(self.channel11, GPIO.LOW)
            GPIO.output(self.channel12, GPIO.HIGH)

            self.pwm_enB1.start(abs(a_right))
            GPIO.output(self.channel13, GPIO.LOW)
            GPIO.output(self.channel14, GPIO.HIGH)

            self.pwm_enA2.start(abs(b_left))
            GPIO.output(self.channel21, GPIO.LOW)
            GPIO.output(self.channel22, GPIO.HIGH)

            self.pwm_enB2.start(abs(b_right))
            GPIO.output(self.channel23, GPIO.LOW)
            GPIO.output(self.channel24, GPIO.HIGH)

        elif a_left > 0 and a_right < 0 and b_left > 0 and b_right < 0:
            """
            По кругу вправо
            """

            self.pwm_enA1.start(abs(a_left))
            GPIO.output(self.channel11, GPIO.HIGH)
            GPIO.output(self.channel12, GPIO.LOW)

            self.pwm_enB1.start(abs(a_right))
            GPIO.output(self.channel13, GPIO.LOW)
            GPIO.output(self.channel14, GPIO.HIGH)

            self.pwm_enA2.start(abs(b_left))
            GPIO.output(self.channel21, GPIO.HIGH)
            GPIO.output(self.channel22, GPIO.LOW)

            self.pwm_enB2.start(abs(b_right))
            GPIO.output(self.channel23, GPIO.LOW)
            GPIO.output(self.channel24, GPIO.HIGH)

        elif a_left < 0 and a_right > 0 and b_left < 0 and b_right > 0:
            """
            По кругу налево
            """

            self.pwm_enA1.start(abs(a_right))
            GPIO.output(self.channel13, GPIO.HIGH)
            GPIO.output(self.channel14, GPIO.LOW)

            self.pwm_enB1.start(abs(a_left))
            GPIO.output(self.channel11, GPIO.LOW)
            GPIO.output(self.channel12, GPIO.HIGH)

            self.pwm_enA2.start(abs(b_right))
            GPIO.output(self.channel23, GPIO.HIGH)
            GPIO.output(self.channel24, GPIO.LOW)

            self.pwm_enB2.start(abs(b_left))
            GPIO.output(self.channel21, GPIO.LOW)
            GPIO.output(self.channel22, GPIO.HIGH)

        elif a_left > 0 and a_right == 0 and b_left == 0 and b_right > 0:
            """
            Наискось вперед направо
            """
            self.pwm_enA1.start(abs(a_left))
            GPIO.output(self.channel11, GPIO.HIGH)
            GPIO.output(self.channel12, GPIO.LOW)

            self.pwm_enB1.start(abs(a_right))
            GPIO.output(self.channel13, GPIO.LOW)
            GPIO.output(self.channel14, GPIO.LOW)

            self.pwm_enA2.start(abs(b_left))
            GPIO.output(self.channel21, GPIO.LOW)
            GPIO.output(self.channel22, GPIO.LOW)

            self.pwm_enB2.start(abs(b_right))
            GPIO.output(self.channel23, GPIO.HIGH)
            GPIO.output(self.channel24, GPIO.LOW)


        elif a_left == 0 and a_right < 0 and b_left < 0 and b_right == 0:
            """ 
            Наискось назад направо
            """
            self.pwm_enA1.start(abs(a_left))
            GPIO.output(self.channel11, GPIO.LOW)
            GPIO.output(self.channel12, GPIO.LOW)

            self.pwm_enB1.start(abs(a_right))
            GPIO.output(self.channel13, GPIO.LOW)
            GPIO.output(self.channel14, GPIO.HIGH)

            self.pwm_enA2.start(abs(b_left))
            GPIO.output(self.channel21, GPIO.LOW)
            GPIO.output(self.channel22, GPIO.HIGH)

            self.pwm_enB2.start(abs(b_right))
            GPIO.output(self.channel23, GPIO.LOW)
            GPIO.output(self.channel24, GPIO.LOW)

        elif a_left == 0 and a_right > 0 and b_left > 0 and b_right == 0:
            """
            Наискось вперед направо
            """
            self.pwm_enA1.start(abs(a_left))
            GPIO.output(self.channel11, GPIO.LOW)
            GPIO.output(self.channel12, GPIO.LOW)

            self.pwm_enB1.start(abs(a_right))
            GPIO.output(self.channel13, GPIO.HIGH)
            GPIO.output(self.channel14, GPIO.LOW)

            self.pwm_enA2.start(abs(b_left))
            GPIO.output(self.channel21, GPIO.HIGH)
            GPIO.output(self.channel22, GPIO.LOW)

            self.pwm_enB2.start(abs(b_right))
            GPIO.output(self.channel23, GPIO.LOW)
            GPIO.output(self.channel24, GPIO.LOW)

        elif a_left < 0 and a_right == 0 and b_left == 0 and b_right < 0:
            """
            Наискось назад направо
            """
            self.pwm_enA1.start(abs(a_left))
            GPIO.output(self.channel11, GPIO.LOW)
            GPIO.output(self.channel12, GPIO.HIGH)

            self.pwm_enB1.start(abs(a_right))
            GPIO.output(self.channel13, GPIO.LOW)
            GPIO.output(self.channel14, GPIO.LOW)

            self.pwm_enA2.start(abs(b_left))
            GPIO.output(self.channel21, GPIO.LOW)
            GPIO.output(self.channel22, GPIO.LOW)

            self.pwm_enB2.start(abs(b_right))
            GPIO.output(self.channel23, GPIO.LOW)
            GPIO.output(self.channel24, GPIO.HIGH)

        elif a_left > 0 and a_right < 0 and b_left < 0 and b_right > 0:
            """
            В бок направо
            """
            self.pwm_enA1.start(abs(a_left))
            GPIO.output(self.channel11, GPIO.HIGH)
            GPIO.output(self.channel12, GPIO.LOW)

            self.pwm_enB1.start(abs(a_right))
            GPIO.output(self.channel13, GPIO.LOW)
            GPIO.output(self.channel14, GPIO.HIGH)

            self.pwm_enA2.start(abs(b_left))
            GPIO.output(self.channel21, GPIO.LOW)
            GPIO.output(self.channel22, GPIO.HIGH)

            self.pwm_enB2.start(abs(b_right))
            GPIO.output(self.channel23, GPIO.HIGH)
            GPIO.output(self.channel24, GPIO.LOW)

        elif a_left < 0 and a_right > 0 and b_left > 0 and b_right < 0:
            """
            В бок налево
            """
            self.pwm_enA1.start(abs(a_left))
            GPIO.output(self.channel11, GPIO.LOW)
            GPIO.output(self.channel12, GPIO.HIGH)

            self.pwm_enB1.start(abs(a_right))
            GPIO.output(self.channel13, GPIO.HIGH)
            GPIO.output(self.channel14, GPIO.LOW)

            self.pwm_enA2.start(abs(b_left))
            GPIO.output(self.channel21, GPIO.HIGH)
            GPIO.output(self.channel22, GPIO.LOW)

            self.pwm_enB2.start(abs(b_right))
            GPIO.output(self.channel23, GPIO.LOW)
            GPIO.output(self.channel24, GPIO.HIGH)

        elif a_left == 0 and a_right == 0 and b_left == 0 and b_right == 0:
            """
            STOP
            """

            self.pwm_enA1.stop()
            GPIO.output(self.channel11, GPIO.LOW)
            GPIO.output(self.channel12, GPIO.LOW)

            self.pwm_enB1.stop()
            GPIO.output(self.channel13, GPIO.LOW)
            GPIO.output(self.channel14, GPIO.LOW)

            self.pwm_enA2.stop()
            GPIO.output(self.channel21, GPIO.LOW)
            GPIO.output(self.channel22, GPIO.LOW)

            self.pwm_enB2.stop()
            GPIO.output(self.channel23, GPIO.LOW)
            GPIO.output(self.channel24, GPIO.LOW)

        else:
            self.logger.error(f'Wrong data...')
            self.pwm_enA1.stop()
            GPIO.output(self.channel11, GPIO.LOW)
            GPIO.output(self.channel12, GPIO.LOW)

            self.pwm_enB1.stop()
            GPIO.output(self.channel13, GPIO.LOW)
            GPIO.output(self.channel14, GPIO.LOW)

            self.pwm_enA2.stop()
            GPIO.output(self.channel21, GPIO.LOW)
            GPIO.output(self.channel22, GPIO.LOW)

            self.pwm_enB2.stop()
            GPIO.output(self.channel23, GPIO.LOW)
            GPIO.output(self.channel24, GPIO.LOW)


class DL298NU(driver):
    """Колеса Илона"""

    def __init__(self, *args, **kwargs):
        super().__init__()

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        GPIO.setup(self.enA1, GPIO.OUT)
        GPIO.setup(self.enB1, GPIO.OUT)
        GPIO.setup(self.channel11, GPIO.OUT)
        GPIO.setup(self.channel12, GPIO.OUT)
        GPIO.setup(self.channel13, GPIO.OUT)
        GPIO.setup(self.channel14, GPIO.OUT)

        GPIO.setup(self.enA2, GPIO.OUT)
        GPIO.setup(self.enB2, GPIO.OUT)
        GPIO.setup(self.channel21, GPIO.OUT)
        GPIO.setup(self.channel22, GPIO.OUT)
        GPIO.setup(self.channel23, GPIO.OUT)
        GPIO.setup(self.channel24, GPIO.OUT)

        GPIO.output(self.channel11, GPIO.LOW)
        GPIO.output(self.channel12, GPIO.LOW)
        GPIO.output(self.channel13, GPIO.LOW)
        GPIO.output(self.channel14, GPIO.LOW)

        GPIO.output(self.channel21, GPIO.LOW)
        GPIO.output(self.channel22, GPIO.LOW)
        GPIO.output(self.channel23, GPIO.LOW)
        GPIO.output(self.channel24, GPIO.LOW)

        self.pwm_enA1 = GPIO.PWM(self.enA1, 1000)
        self.pwm_enB1 = GPIO.PWM(self.enB1, 1000)

        self.pwm_enA2 = GPIO.PWM(self.enA2, 1000)
        self.pwm_enB2 = GPIO.PWM(self.enB2, 1000)

        self.pwm_enA1.stop()
        self.pwm_enB1.stop()
        self.pwm_enA2.stop()
        self.pwm_enB2.stop()


    def pwm_controller(self, manage_list: list):
        left, right = manage_list
        left = int(left * 100)
        right = int(right * 100)
        self.logger.debug(f'left : {left} right : {right}')

        if left >= 0 and right >= 0:

            self.pwm_enA1.start(abs(left))
            GPIO.output(self.channel11, GPIO.HIGH)
            GPIO.output(self.channel12, GPIO.LOW)

            self.pwm_enB1.start(abs(right))
            GPIO.output(self.channel13, GPIO.HIGH)
            GPIO.output(self.channel14, GPIO.LOW)

            self.pwm_enA2.start(abs(left))
            GPIO.output(self.channel21, GPIO.HIGH)
            GPIO.output(self.channel22, GPIO.LOW)

            self.pwm_enB2.start(abs(right))
            GPIO.output(self.channel23, GPIO.HIGH)
            GPIO.output(self.channel24, GPIO.LOW)


        elif left < 0 and right < 0:

            self.pwm_enA1.start(abs(left))
            GPIO.output(self.channel11, GPIO.LOW)
            GPIO.output(self.channel12, GPIO.HIGH)

            self.pwm_enB1.start(abs(right))
            GPIO.output(self.channel13, GPIO.LOW)
            GPIO.output(self.channel14, GPIO.HIGH)

            self.pwm_enA2.start(abs(left))
            GPIO.output(self.channel21, GPIO.LOW)
            GPIO.output(self.channel22, GPIO.HIGH)

            self.pwm_enB2.start(abs(right))
            GPIO.output(self.channel23, GPIO.LOW)
            GPIO.output(self.channel24, GPIO.HIGH)

        elif left >= 0 and right < 0:

            self.pwm_enA1.start(abs(left))
            GPIO.output(self.channel11, GPIO.HIGH)
            GPIO.output(self.channel12, GPIO.LOW)

            self.pwm_enB1.start(abs(right))
            GPIO.output(self.channel13, GPIO.LOW)
            GPIO.output(self.channel14, GPIO.HIGH)

            self.pwm_enA2.start(abs(left))
            GPIO.output(self.channel21, GPIO.HIGH)
            GPIO.output(self.channel22, GPIO.LOW)

            self.pwm_enB2.start(abs(right))
            GPIO.output(self.channel23, GPIO.LOW)
            GPIO.output(self.channel24, GPIO.HIGH)

        elif left < 0 and right >= 0:

            self.pwm_enA1.start(abs(left))
            GPIO.output(self.channel11, GPIO.LOW)
            GPIO.output(self.channel12, GPIO.HIGH)

            self.pwm_enB1.start(abs(right))
            GPIO.output(self.channel13, GPIO.HIGH)
            GPIO.output(self.channel14, GPIO.LOW)

            self.pwm_enA2.start(abs(left))
            GPIO.output(self.channel21, GPIO.LOW)
            GPIO.output(self.channel22, GPIO.HIGH)

            self.pwm_enB2.start(abs(right))
            GPIO.output(self.channel23, GPIO.HIGH)
            GPIO.output(self.channel24, GPIO.LOW)

        elif left == 0 and right == 0:

            self.pwm_enA1.stop()
            GPIO.output(self.channel11, GPIO.LOW)
            GPIO.output(self.channel12, GPIO.LOW)

            self.pwm_enB1.stop()
            GPIO.output(self.channel13, GPIO.LOW)
            GPIO.output(self.channel14, GPIO.LOW)

            self.pwm_enA2.stop()
            GPIO.output(self.channel21, GPIO.LOW)
            GPIO.output(self.channel22, GPIO.LOW)

            self.pwm_enB2.stop()
            GPIO.output(self.channel23, GPIO.LOW)
            GPIO.output(self.channel24, GPIO.LOW)