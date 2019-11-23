#!/usr/bin/env python
import logging
import argparse
import os
import time
import pika

logging.basicConfig(filename='../../data/streamdata_receiver_logs.log',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

def parse_arguments():
    parser = argparse.ArgumentParser(description='Init authentication')
    #queue
    parser.add_argument('-queue', type=str, help='You must provide the name of the queue')
    return parser.parse_args()

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    time.sleep(0.5) #simulate some processing work
    logging.info("Receive data : %r" % body)
    ch.basic_ack(delivery_tag = method.delivery_tag)

if __name__ == "__main__":
    args = parse_arguments()
    if args.queue is None:
        logging.debug("Queue unspecified when launching client_receiver")
        exit(0)
    logging.info("Receive data : Starting connection to RabbitMQ")
    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters('localhost', 5672, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    logging.info("Receive data : Creation of the topic if not exists")
    channel.queue_declare(queue=args.queue)
    channel.basic_consume(queue=args.queue, on_message_callback=callback)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
    