/*
* CS-E4640
* Linh Truong
* Edited by Clement Lopez
*/

package main.java.flinkcode;

import java.io.StringReader;
import java.util.Date;
import java.text.SimpleDateFormat;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.CheckpointingMode;
import org.apache.flink.streaming.api.TimeCharacteristic;
import org.apache.flink.api.java.utils.ParameterTool;
import org.apache.flink.types.Row;
import org.apache.flink.api.common.typeinfo.TypeInformation;
import org.apache.flink.streaming.connectors.rabbitmq.common.RMQConnectionConfig;
import org.apache.flink.streaming.connectors.rabbitmq.RMQSource;
import org.apache.flink.streaming.connectors.rabbitmq.RMQSink;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.api.common.serialization.SimpleStringSchema;
import org.apache.flink.streaming.api.windowing.windows.Window;
import org.apache.flink.api.java.tuple.Tuple;
import org.apache.flink.streaming.api.windowing.time.Time;
import org.apache.flink.streaming.api.windowing.windows.TimeWindow;
import org.apache.flink.streaming.api.windowing.assigners.SlidingTimeWindows;
import org.apache.flink.streaming.api.windowing.assigners.SlidingProcessingTimeWindows;
import org.apache.flink.streaming.api.windowing.assigners.SlidingEventTimeWindows;
import org.apache.flink.streaming.api.functions.windowing.WindowFunction;
import org.apache.flink.api.common.functions.FlatMapFunction;
import org.apache.flink.util.Collector;
import org.apache.flink.streaming.api.functions.windowing.ProcessWindowFunction;
import org.apache.flink.api.java.functions.KeySelector;
import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVRecord;

import org.apache.flink.configuration.Configuration;
import org.apache.flink.api.java.tuple.Tuple;
import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.api.java.tuple.Tuple3;
import org.apache.flink.api.common.state.ValueState;
import org.apache.flink.api.common.state.ValueStateDescriptor;
import org.apache.flink.streaming.api.functions.KeyedProcessFunction;
import org.apache.flink.streaming.api.functions.KeyedProcessFunction.Context;
import org.apache.flink.streaming.api.functions.KeyedProcessFunction.OnTimerContext;

public class SimpleAlarmAnalysis {

	public static void main(String[] args) throws Exception {
		// using flink ParameterTool to parse input parameters
		final String input_rabbitMQ;
		final String inputQueue;
		final String outputQueue;
		final int parallelismDegree;
		try {
			final ParameterTool params = ParameterTool.fromArgs(args);
			input_rabbitMQ = params.get("amqpurl");
			inputQueue = params.get("iqueue");
			outputQueue = params.get("oqueue");
			parallelismDegree = params.getInt("parallelism");
		} catch (Exception e) {
			System.err.println(
					"'LowSpeedDetection --amqpurl <rabbitmq url>  --iqueue <input data queue> --oqueue <output data queue> --parallelism <degree of parallelism>'");
			return;
		}

		// the following is for setting up the execution getExecutionEnvironment
		final StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

		// checkpoint can be used for different levels of message guarantees
		// select one of the following modes
		final CheckpointingMode checkpointingMode = CheckpointingMode.EXACTLY_ONCE;
		env.enableCheckpointing(1000 * 60, checkpointingMode);
		// define the event time
		env.setStreamTimeCharacteristic(TimeCharacteristic.ProcessingTime);
//		env.setStreamTimeCharacteristic(TimeCharacteristic.EventTime);
		// now start with the source of data
		final RMQConnectionConfig connectionConfig = new RMQConnectionConfig.Builder().setHost(input_rabbitMQ)
				.setVirtualHost("/").setUserName("guest").setPassword("guest").setPort(5672).build();

		// build schema for the input DataStream
		// simple text schema
		SimpleStringSchema inputSchema = new SimpleStringSchema();
		// declare rabbit mq as a source of data and set parallelism degree
		RMQSource<String> btsdatasource = new RMQSource(connectionConfig, // config for the RabbitMQ connection
				inputQueue, // name of the RabbitMQ queue to consume
				false, // no correlation between event
				inputSchema);

		final DataStream<String> btsdatastream = env.addSource(btsdatasource) // deserialization schema for input
				.setParallelism(parallelismDegree);

		/************* Analytics **********************/
		/* Analytic without Window */
		DataStream<String> non_windowed = btsdatastream
				.flatMap(new BTSParser()).keyBy(new StationSensorAlarmKeySelector())
			    .process(new FunctionGlobal());
		
		/* Analytic with Window */
		DataStream<String> windowed = btsdatastream.flatMap(new BTSParser()).keyBy(new StationSensorAlarmKeySelector())
				.window(SlidingProcessingTimeWindows.of(Time.minutes(1), Time.seconds(5)))
				.process(new WindowedFunction());

		// send the alerts to another channel
		RMQSink<String> sink = new RMQSink<String>(connectionConfig, outputQueue, new SimpleStringSchema());		

		
		windowed.addSink(sink);
		non_windowed.addSink(sink);

		// Send out the result
		windowed.print().setParallelism(parallelismDegree);
		non_windowed.print().setParallelism(parallelismDegree);

		env.execute("Assignment 3 Analysis");
	}
	

	// Reliability : chaleur augmente proche du pic, lancer alerte
	// Noise detect : coherence avec valeur avant/apres
	// Number of returned analytics ?
	// Nombre de rows recues
	

}
