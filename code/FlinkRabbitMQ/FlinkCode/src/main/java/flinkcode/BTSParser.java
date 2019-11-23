package main.java.flinkcode;

import java.io.StringReader;
import java.text.SimpleDateFormat;
import java.util.Date;
import org.apache.flink.api.common.functions.FlatMapFunction;
import org.apache.flink.util.Collector;
import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVRecord;

//we write a simple way to parsing the text as csv record.
// You can do it more simple by parsing the text with ","
public class BTSParser implements FlatMapFunction<String, BTSEvent> {

	@Override
	public void flatMap(String line, Collector<BTSEvent> out) throws Exception {
		CSVRecord record = CSVFormat.RFC4180.withIgnoreHeaderCase().parse(new StringReader(line)).getRecords().get(0);
		try {
			SimpleDateFormat format = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss z");
			Date date = format.parse(record.get(3));
			BTSEvent event = new BTSEvent(record.get(0), record.get(1), record.get(2), date,
					Float.valueOf(record.get(4)), Float.valueOf(record.get(5)), Boolean.valueOf(record.get(6)), true);
			out.collect(event);
		} catch (Exception e) {
			BTSEvent event = new BTSEvent(record.get(0), record.get(1), record.get(2), new Date(), 0f, 0f, true,
					false);
			out.collect(event);
		}
	}
}
