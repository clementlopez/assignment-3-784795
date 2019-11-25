# This your assignment deployment report

it is a free form. you can add:

* how to deploy your system 

## Important

All subsequent instructions must be from the ```code``` folder

## Prerequisites

You need Python installed in your machine,
then run ```pip install -r requirements.txt```

## Run Docker

Run ```make install``` in order to deploy all the docker servers.

## Build java project and inject it into Flink server

Run ```cd FlinkRabbitMQ/FlinkCode```
Then run ```./script_install_jar_on_flink.sh``` the script will build the Java maven project and copy the jar file into the Flink server docker.

## Send/Receive data

Run ```cd ../../client```

### To start the analytics on Flink

Run ```./start_analytics.sh```

### To receive analytics

Run in another terminal ```./receive.sh```

### To send data for analytics

Run in another terminal ```./send.sh``` or if you want to test with a very small dataset which include some data conversion error (explained in Assignment-3-Design.md) you can run ```test_metric_sender.sh```

### Results

The results of the Analytics are printed in the terminal where the receiver script runs. You can also have a look at them in the file ```streamdata_receiver_logs.log``` and you can have a look at the sender script logs in the file ```streamdata_logs.log```, this 2 files are in the ```logs``` directory. This 2 files only appear in the structure after your first run of the code (I delete all previous logs in order to make them more readable)




