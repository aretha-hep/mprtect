import click
import zmq
import es_put
import time

@click.command()
@click.argument('elastic_ip')
def eventcollector(elastic_ip):
    context = zmq.Context()
    pull_socket = context.socket(zmq.PULL)
    pull_socket.bind("tcp://*:3141")

    nevents = 0
    put_event = es_put.get_putter(elastic_ip)
    while True:
        zr,zw,zx = zmq.select([pull_socket], [],[], timeout = 0.0)
        if pull_socket in zr:
            message = pull_socket.recv_json()
            print "got event: {}".format(message)
            nevents = nevents+1
            put_event(message)
            if (nevents % 1000):
                print '{} events received'.format()
        time.sleep(0.001)


if __name__ == '__main__':
    eventcollector()