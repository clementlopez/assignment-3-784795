package main.java.flinkcode;

import org.apache.flink.api.java.functions.KeySelector;
import org.apache.flink.api.java.tuple.Tuple3;

//keyed by station_sensor_alarm_ids
public class StationSensorAlarmKeySelector implements KeySelector<BTSEvent, Tuple3<String, String, String>> {

	@Override
	public Tuple3<String, String, String> getKey(BTSEvent value) throws Exception {
		return new Tuple3(value.station_id, value.datapoint_id, value.alarm_id);
	}
}
