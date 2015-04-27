from pika import SelectConnection, ConnectionParameters
from time import sleep

CHANNEL = None
QUEUE = 'xxx'

def on_connection_open(connection):
    connection.channel(on_channel_open)

def on_channel_open(channel):
    global CHANNEL
    CHANNEL = channel
    CHANNEL.queue_declare(queue=QUEUE, callback=on_queue_declared)

def on_queue_declared(frame):
    count = 0
    while True:
        body = str(count)
        CHANNEL.basic_publish(exchange='', routing_key=QUEUE, body=body)
        print 'Sent %s' % body
        sleep(3)
        count += 1

parameters = ConnectionParameters()
connection = SelectConnection(parameters, on_open_callback=on_connection_open)
try:
    connection.ioloop.start()
except KeyboardInterrupt:
    connection.close()
    connection.ioloop.start()
