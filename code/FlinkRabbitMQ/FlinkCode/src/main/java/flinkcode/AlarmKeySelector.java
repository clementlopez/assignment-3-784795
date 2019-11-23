package main.java.flinkcode;

import org.apache.flink.api.java.functions.KeySelector;

//keyed by alarm_id
public class AlarmKeySelector implements KeySelector<BTSEvent, String> {

	@Override
	public String getKey(BTSEvent value) throws Exception {
		return value.alarm_id;
	}
}
