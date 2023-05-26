FROM aaadur/padelselenium

#Pull python file into the location of the geckodriver for it to run 
COPY /robot.py /usr/local/bin
COPY /RéservationPadel.xml /usr/local/bin
WORKDIR /usr/local/bin

VOLUME test /usr/local/bin

ENV PYTHONPATH="/install"
RUN export PYTHONPATH=/install

CMD python3 robot.py
