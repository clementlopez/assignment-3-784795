docker exec -it code_jobmanager_1 flink run /job.jar --amqpurl rabbitmq1 --iqueue customer1 --oqueue receiver1 --parallelism 1
