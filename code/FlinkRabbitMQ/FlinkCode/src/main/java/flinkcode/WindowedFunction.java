package main.java.flinkcode;

import org.apache.flink.util.Collector;
import org.apache.flink.streaming.api.functions.windowing.ProcessWindowFunction;
import org.apache.flink.api.java.tuple.Tuple3;
import org.apache.flink.streaming.api.windowing.windows.TimeWindow;

//Mean, max & min in timewindow
// a simple function to detect a sequence of alarms in a round
public class WindowedFunction
		extends ProcessWindowFunction<BTSEvent, String, Tuple3<String, String, String>, TimeWindow> {

	@Override
	public void process(Tuple3<String, String, String> station_sensor_alarm_ids, Context context,
			Iterable<BTSEvent> records, Collector<String> out) {
		// Analytics
		float max = 0;
		float min = 0;
		double sum = 0;
		long count = 0;
		long number_alarms = 0;

		// Metrics
		long data_conversion_errors = 0;
		for (BTSEvent btsrecord : records) {
			if(btsrecord.well_deserialized) {
				if (count == 0) {
					sum = btsrecord.value;
					max = btsrecord.value;
					min = btsrecord.value;
				} else {
					if (btsrecord.value > max) {
						max = btsrecord.value;
					} else if (btsrecord.value < min) {
						min = btsrecord.value;
					}
					sum += btsrecord.value;
				}
				if(btsrecord.is_alarm_active) {
					number_alarms += 1;
				}
				count++;
			}
			else {
				data_conversion_errors += 1;
			}
		}
		if (count > 0) {
			double mean = sum / count;
			out.collect("{\"type\":\"Windowed Analytic\"," +
						"\"key\":{\"station_id\":" + station_sensor_alarm_ids.f0 +
							", \"datapoint_id\":" + station_sensor_alarm_ids.f1 +
							", \"alarm_id\":" + station_sensor_alarm_ids.f2 +
						"}" +
						"\"data\":{ \"mean\":" + mean +
							", \"max\":" + max +
							", \"min\":" + min +
							", \"counter\":" + count +
							", \"alarms\":" + number_alarms +
						"}}");
		}
		out.collect("{\"type\":\"Windowed Metric\","+
					"\"key\":{\"station_id\":" + station_sensor_alarm_ids.f0 +
						", \"datapoint_id\":" + station_sensor_alarm_ids.f1 +
						", \"alarm_id\":" + station_sensor_alarm_ids.f2 +
					"}" +
					" \"data\":{ \"data_conversion_errors\":"+data_conversion_errors+"}}");
	}
}
