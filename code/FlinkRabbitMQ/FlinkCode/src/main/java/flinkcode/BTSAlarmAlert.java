/*
 * CS-E4640
 * Linh Truong
 * Edited by Clement Lopez
 */
package main.java.flinkcode;

public class BTSAlarmAlert {
	public boolean warning = false;
	public String station_id;

	public BTSAlarmAlert() {
	}

	public BTSAlarmAlert(String station_id, boolean warning) {
		this.station_id = station_id;
		this.warning = warning;
	}

	public String toString() {
		return "Station with " + station_id + " has too many alarms";
	}

	public String toJSON() {
		return "{\"btsalarmalert\":{\"station_id\":" + station_id + ", \"active\":true}}";
	}

}
