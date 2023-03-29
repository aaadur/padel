FROM alpine

RUN mkdir /install
WORKDIR /install

COPY requirements.txt /requirements.txt

RUN apk --update add --no-cache g++ \
    gcc musl-dev python3-dev libffi-dev openssl-dev cargo py3-pip

RUN pip install -U pip

RUN pip install --target=/install -r /requirements.txt
#RUN pip install --install-option="--prefix='/install'" -r /requirements.txt
#RUN pip install -r /requirements.txt

RUN apk del g++ gcc musl-dev python3-dev libffi-dev openssl-dev cargo

RUN apk add --no-cache python3

#Update packages and add the following programs for selenium to work
RUN apk --update add --no-cache g++
RUN apk add wget unzip dbus-x11 ttf-freefont firefox-esr@102.4.0 xvfb tar

#Pull geckodriver from the github respository 
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz

#unzip it and move to a directory.
RUN tar -zxvf geckodriver-v0.30.0-linux64.tar.gz
RUN mv ./geckodriver /usr/local/bin

# then make it executable to everyone
RUN chmod a+x /usr/local/bin/geckodriver

#Pull python file into the location of the geckodriver for it to run 
COPY /robot.py /usr/local/bin
COPY /RéservationPadel.xml /usr/local/bin
WORKDIR /usr/local/bin

VOLUME test /usr/local/bin

ENV PYTHONPATH="/install"
RUN export PYTHONPATH=/install

CMD python3 robot.py
#CMD [ "python", ma ]
