FROM aaadur/padelselenium

#Pull python file into the location of the geckodriver for it to run 
COPY /robot.py /usr/local/bin
COPY /ReservationPadel.xml /usr/local/bin
WORKDIR /usr/local/bin

VOLUME test /usr/local/bin

ENV PYTHONPATH="/install"
RUN export PYTHONPATH=/install

ENTRYPOINT ["python3", "robot.py"]
