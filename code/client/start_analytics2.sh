docker exec -it code_jobmanager_1 flink run /job.jar --amqpurl rabbitmq1 --iqueue customer2 --oqueue receiver2 --parallelism 1
