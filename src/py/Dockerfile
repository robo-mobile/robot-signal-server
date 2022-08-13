FROM python:3.9-slim-buster

WORKDIR /app

RUN apt update && apt upgrade -y && apt install -y gcc
COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . .
ENV PYTHONPATH "${PYTHONPATH}:/app"
CMD  python3 -m pwm.pwm_manage.app start
#CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]