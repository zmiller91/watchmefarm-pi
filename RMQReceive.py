__author__ = 'zmiller'

import pika
import configuration
import os
import shared

def callback(ch, method, properties, body):

    # Create the configuration directory if it doesn't exist
    if not os.path.isdir(configuration.PATH):
        print "Creating directory..."
        os.makedirs(configuration.PATH)

    # Write message to the new configuration file
    filename = configuration.PATH + "/" + str(shared.curTime()) + ".txt"
    f = open(filename, 'w')
    f.write(body)
    f.close()

    print(" [x] Received %r" % body)

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='hello')
channel.basic_consume(callback, queue='hello', no_ack=True)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()