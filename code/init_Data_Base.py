from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Init authentication')
    parser.add_argument('--user', type=str, help='You must fill in a String', default='cassandra')
    parser.add_argument('--password', type=str, help='You must fill in a String',  default='cassandra')
    parser.add_argument('--port', type=int, help='You must fill in a Int',  default=9042)
    parser.add_argument('--adress', type=str, help='You must fill in a Int',  default='0.0.0.0')
    return parser.parse_args()



if __name__ == "__main__":
    args = parse_arguments()
    #Connect cluster
    auth_provider = PlainTextAuthProvider(username=args.user, password=args.password)
    cluster = Cluster([args.adress], auth_provider=auth_provider, port=args.port)
    session = cluster.connect()

    #Create Keyspace Customer-1
    session.execute("""CREATE KEYSPACE IF NOT EXISTS Customer1
        WITH REPLICATION = {
            'class' : 'SimpleStrategy',
            'replication_factor' : 1
        };
    """)

    #Create Keyspace Customer-1
    session.execute("""CREATE KEYSPACE IF NOT EXISTS Customer2
        WITH REPLICATION = {
            'class' : 'SimpleStrategy',
            'replication_factor' : 1
        };
    """)

    #Enter in the keyspace Customer-1
    session.execute("USE Customer1;")

    #Create Table
    session.execute("""
    CREATE TABLE Bts
    (
        id UUID PRIMARY KEY,
        station_id text,
        datapoint_id text,
        alarm_id text,
        event_time timestamp,
        value float,
        valueThreshold float,
        isActive Boolean,
        storedtime timestamp
    );
    """)
    
    #Enter in the keyspace Customer-2
    session.execute("USE Customer2;")

    #Create Table
    session.execute("""
    CREATE TABLE Bts
    (
        id UUID PRIMARY KEY,
        station_id text,
        datapoint_id text,
        alarm_id text,
        event_time timestamp,
        value float,
        valueThreshold float,
        isActive Boolean,
        storedtime timestamp
    );
    """)

    #Close cluster
    cluster.shutdown()