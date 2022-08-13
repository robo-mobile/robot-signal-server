import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(

    name='pwm_manage',

    version='1.0.0',

    packages=['pwm_manage'],

    author="Alexandr Liakhov",

    author_email="eleutherius69@gmail.com",

    description=" PWM for robot",

    long_description=long_description,

    long_description_content_type="text/markdown",

    # packages=setuptools.find_packages(),

    classifiers=[

        "Programming Language :: Python :: 3",

        "Operating System :: OS Independent",

    ],
    setup_requires=['wheel'],
    entry_points={
        'console_scripts': [
            'pwm = pwm_manage.pwm_manage:app'
        ]
    },

    install_requires=['typer', 'RPi.GPIO', 'asyncio', 'websockets', 'systemd',
                      'toml'],

    url='https://github.com/robo-mobile/pwm_manage'

)
