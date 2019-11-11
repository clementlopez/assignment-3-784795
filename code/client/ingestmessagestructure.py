import paho.mqtt.client as mqtt
import logging
import argparse
import os
import time


def parse_arguments():
    parser = argparse.ArgumentParser(description='Init authentication')
    #customer-X
    parser.add_argument('-u', type=str, help='You must provide a userId')
    #message
    parser.add_argument('-file', type=str, help='You must provide the path to the file to stream')
    return parser.parse_args()

def stream_data(message, topic):
    logging.info("Stream data : creating new client instance")
    client = mqtt.Client(args.u)
    logging.info("Stream data : connecting to broker")
    client.connect("localhost")
    logging.info("Stream data : publishing into broker")
    client.publish(topic,message)
    logging.info("Stream data : message %s streamed, now disconnect" %(message))
    client.disconnect()
    logging.info("Stream data : disconnected")


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

