import click
import zmq
import es_put
import time

@click.command()
def eventcollector():
    context = zmq.Context()
    pull_socket = context.socket(zmq.PULL)
    pull_socket.bind("tcp://*:3141")
    while True:
        zr,zw,zx = zmq.select([pull_socket], [],[], timeout = 0.0)
        if pull_socket in zr:
            message = pull_socket.recv_json()
            print "got event: {}".format(message)
            es_put.put_event(message)
        time.sleep(0.001)


if __name__ == '__main__':
    eventcollector()