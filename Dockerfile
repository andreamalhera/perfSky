FROM andreamaldonado/process_mining_mt:latest
COPY /setup.py setup.py
RUN python setup.py install
WORKDIR /code
