FROM andreamaldonado/process_mining_mt:first_tag
RUN pip install pm4py
WORKDIR /code
