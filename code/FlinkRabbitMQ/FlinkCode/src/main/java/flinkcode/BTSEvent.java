/*
* CS-E4640
 * Linh Truong
 * Edited by Clement Lopez
 */
package main.java.flinkcode;

import java.util.Date;

public class BTSEvent {
	public String station_id;
	public String datapoint_id;
	public String alarm_id;
	public Date event_time;
	public float value;
	public float valueThreshold;
	public boolean is_alarm_active;
	public boolean well_deserialized; // if the input event could be deserialized
	

	BTSEvent() {

	}

	BTSEvent(String station_id, String datapoint_id, String alarm_id, Date event_time, Float value,
			Float valueThreshold, boolean alarm_active, boolean deserialized) {
		this.station_id = station_id;
		this.datapoint_id = datapoint_id;
		this.alarm_id = alarm_id;
		this.event_time = event_time;
		this.value = value;
		this.valueThreshold = valueThreshold;
		this.is_alarm_active = alarm_active;
		this.well_deserialized = deserialized;
	}

	public String toString() {
		return "station_id=" + station_id + " for datapoint_id=" + datapoint_id + " at " + event_time.toString()
				+ " alarm_id=" + alarm_id + " with value =" + value;
	}
}
