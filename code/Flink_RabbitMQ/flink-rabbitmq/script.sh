docker cp target/flink-rabbitmq-1.0-SNAPSHOT.jar code_jobmanager_1:/job.jar
docker exec -it code_jobmanager_1 flink run /job.jar --amqpurl localhost --iqueue aa --oqueue bb --parallelism 1
