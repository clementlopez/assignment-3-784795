#!/usr/bin/env python
import paho.mqtt.client as mqtt
import logging
import argparse
import os
import time
import pika

def parse_arguments():
    parser = argparse.ArgumentParser(description='Init authentication')
    #customer-X
    parser.add_argument('-u', type=str, help='You must provide a userId')
    #message
    parser.add_argument('-file', type=str, help='You must provide the path to the file to stream')
    return parser.parse_args()

def stream_data(message, topic):
    logging.info("Stream data : Starting connection to RabbitMQ")
    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters('localhost', 5672, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    logging.info("Stream data : Creation of the topic if not exists")
    channel.queue_declare(queue=topic)
    logging.info("Stream data : Sending message")
    channel.basic_publish(exchange='',
                        routing_key=topic,
                        body='Hello World!')
    logging.info("Stream data : Closing connection")
    connection.close()


if __name__ == "__main__":
    logging.basicConfig(filename='../../data/streamdata_logs.log',
                        level=logging.DEBUG,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    args = parse_arguments()
    if args.u is None:
        logging.debug("User unspecified when launching ingestmessagestructure")
        exit(0)
    if args.file is None or os.path.exists(args.file):
        logging.debug("No file to stream when launching ingestmessagestructure")
        exit(0)
    with open(args.file) as csv_file:
        data = csv_file.read()
        data_lines = data.splitlines()
        for lineToStream in data_lines:
            time.sleep(0.05) #to remove
            stream_data(lineToStream, args.u)

