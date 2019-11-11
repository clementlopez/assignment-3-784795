import csv
import os
import uuid
from datetime import datetime
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Init authentication')
    parser.add_argument('-file', type=str, help='define the file to ingest', default=None)
    parser.add_argument('--id', type=str, help='You must fill in a Int',  default=0)
    return parser.parse_args()

def fill_database(session, file):
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count > 0:
                rating = float(row[2])
                rev = int(row[3])
                fr = bool(row[6])
                price = float(row[7])
                session.execute("""
                INSERT INTO Application (id, name, category, rating, reviews, size, installs, free, price_dollar, content_rating, genres, last_update, current_ver, android_ver)
                values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (uuid.uuid1(), row[0], row[1], rating, rev,
                row[4], row[5], fr, price, row[8],
                row[9], row[10], row[11], row[12])
                )
            line_count += 1
    return

if __name__ == "__main__":
    args = parse_arguments()
    if args.file is None or not os.path.exists(args.file):
        exit(0)
    #Connect cluster
    auth_provider = PlainTextAuthProvider(username='cassandra', password='cassandra')
    cluster = Cluster(['cassan2'], auth_provider=auth_provider, port=9042)
    session = cluster.connect()

    #Enter in the keyspace
    session.execute("USE Customer1;")

    fill_database(session, args.file)

    #Close cluster
    cluster.shutdown()