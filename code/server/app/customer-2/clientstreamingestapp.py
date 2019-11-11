#!/usr/bin/python3

import paho.mqtt.client as mqtt
import uuid
import time
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

avg_process_time = 0
total_messages = 0
time_of_last_report = 0
    

def insert_in_cassandra(message_mqtt):
    #Connect cluster
    auth_provider = PlainTextAuthProvider(username='cassandra', password='cassandra')
    cluster = Cluster(['cassan2'], auth_provider=auth_provider, port=9042)
    session = cluster.connect()

    #Enter in the keyspace
    session.execute("USE Customer2;")

    #Insert in Cassandra
    row = message_mqtt.split(",")
    rating = float(row[2])
    rev = int(row[3])
    fr = bool(row[6])
    price = float(row[7])
    ret = session.execute("""
                INSERT INTO Application (id, name, category, rating, reviews, size, installs, free, price_dollar, content_rating, genres, last_update, current_ver, android_ver)
                values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (uuid.uuid1(), row[0], row[1], rating, rev,
                row[4], row[5], fr, price, row[8],
                row[9], row[10], row[11], row[12])
                )
    
    #Close cluster
    cluster.shutdown()
    return ret

def report_data():
    global avg_process_time, total_messages, time_of_last_report
    if time.time() > (time_of_last_report + 10):
        client = mqtt.Client()
        client.connect("databroker")
        client.publish("reportStream", ["customer-2", avg_process_time])
        client.disconnect()
        #reinit global variables
        avg_process_time = 0
        total_messages = 0
        time_of_last_report = time.time()


def on_message(client, userdata, msg):
    global avg_process_time, total_messages
    start = time.time()
    result = insert_in_cassandra(str(msg.payload.decode()))
    end = time.time()
    if result == 0:
        avg_process_time = ((avg_process_time * total_messages)+(end-start))/(total_messages+1)
        total_messages = total_messages + 1
        report_data()
    return result


if __name__ == "__main__":
    client = mqtt.Client()
    client.connect("databroker")
    client.subscribe("customer-2")
    client.on_message = on_message
    client.loop_forever()