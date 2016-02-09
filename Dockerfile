FROM lukasheinrich/python27sherpa220rivet230
COPY HepMC-2.06.09 /code/HepMC-2.06.09
WORKDIR /code/HepMC-2.06.09
RUN ./configure --with-momentum=GEV --with-length=MM
RUN make -j2
RUN make -j2 install

COPY swig-3.0.8.tar.gz /code
WORKDIR /code
RUN tar -xzvf swig-3.0.8.tar.gz
WORKDIR /code/swig-3.0.8
RUN ./configure && make &&  make install
WORKDIR /code
ENV HEPMCPATH /usr/local
ENV HEPMC_VERSION 2.06.09
ADD pyhepmc pyhepmc_src
WORKDIR pyhepmc_src
RUN python setup.py build_ext
RUN python setup.py install
ENV LD_LIBRARY_PATH /usr/local/lib:/usr/local/lib:

WORKDIR /code
RUN pip install click zmq
RUN git clone https://github.com/lukasheinrich/hepmcanalysis.git hepmcanalysis_src
WORKDIR hepmcanalysis_src
RUN python setup.py build_ext
RUN python setup.py install
WORKDIR /code

RUN apt-get update && apt-get install --yes nano

RUN echo 'rebuild'
ADD mprtect mprtect
WORKDIR mprtect
RUN pip install -e .
WORKDIR /code
RUN pip install elasticsearch
ADD input.hepmc test.hepmc
