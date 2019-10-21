FROM andreamaldonado/process_mining_mt:first_tag
RUN pip install pm4py
#TODO: Replace 'docker run -it -v $PWD/nfs/dockervolume/:/volume\
#andreamaldonado/process_mining_mt:first_tag bash'
CMD python test.py
