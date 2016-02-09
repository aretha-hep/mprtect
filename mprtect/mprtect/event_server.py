import zmq
import click
import hepmcanalysis
import hepmc
from hepmcanalysis.streamproxy import ifstream_proxy
from hepmcanalysis.events import events, dumps
import os
import time
import math
import uuid
import socket

@click.command()
@click.argument('hepmcfile')
@click.argument('collectordns')
def eventserver(hepmcfile,collectordns):
    context = zmq.Context()
    push_socket = context.socket(zmq.PUSH)
    push_socket.connect("tcp://{}:3141".format(socket.gethostbyname_ex(collectordns)[-1][0]))

    proxy = ifstream_proxy(str(os.path.abspath(hepmcfile)))
    g = hepmc.IO_GenEvent(proxy.stream())
    for i,e in enumerate(events(g)):
        particles_json = []
        for x in e.particles():
            particles_json += [{
                'px':x.momentum().px(),
                'py':x.momentum().py(),
                'pz':x.momentum().pz(),
                'pT':math.sqrt(x.momentum().px()**2 + x.momentum().py()**2)
            }]
        hepmc_json_event = {
            'id': str(uuid.uuid4()),
            'hepmcstring':dumps([e]),
            'nparticles':len(e.particles()),
            'particles': particles_json
        }

        push_socket.send_json({'event':hepmc_json_event})
        time.sleep(0.001)

if __name__ == '__main__':
    eventserver()

