__author__ = 'zmiller'

import pika
import sys

if len(sys.argv) != 4:
    print "3 arguments must be provided: component, action, value"
    exit()

message = sys.argv[1] + ":" + sys.argv[2] + ":" + sys.argv[3]
connection = pika.BlockingConnection(pika.ConnectionParameters(
               'localhost'))
channel = connection.channel()
channel.queue_declare(queue='hello')
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body = message)

print(" [x] Sent '"+ message + "'")
connection.close()