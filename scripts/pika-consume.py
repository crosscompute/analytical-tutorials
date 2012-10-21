from pika import SelectConnection, ConnectionParameters

CHANNEL = None
QUEUE = 'xxx'

def on_connection_open(connection):
    connection.channel(on_channel_open)

def on_channel_open(channel):
    global CHANNEL
    CHANNEL = channel
    CHANNEL.queue_declare(queue=QUEUE, callback=on_queue_declared)

def on_queue_declared(frame):
    CHANNEL.basic_consume(queue=QUEUE, consumer_callback=consume)

def consume(channel, method, header, body):
    CHANNEL.basic_ack(delivery_tag=method.delivery_tag)
    print 'Received %s' % body

parameters = ConnectionParameters()
connection = SelectConnection(parameters, on_open_callback=on_connection_open)
try:
    connection.ioloop.start()
except KeyboardInterrupt:
    connection.close()
    connection.ioloop.start()
