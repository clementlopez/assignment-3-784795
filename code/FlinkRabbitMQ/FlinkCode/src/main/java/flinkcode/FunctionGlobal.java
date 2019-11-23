package main.java.flinkcode;

import org.apache.flink.api.common.state.ValueState;
import org.apache.flink.api.common.state.ValueStateDescriptor;
import org.apache.flink.streaming.api.functions.KeyedProcessFunction;
import org.apache.flink.streaming.api.functions.KeyedProcessFunction.Context;
import org.apache.flink.util.Collector;
import org.apache.flink.configuration.Configuration;
import org.apache.flink.api.java.tuple.Tuple3;

public class FunctionGlobal extends KeyedProcessFunction<Tuple3<String, String, String>, BTSEvent, String> {
	
	/** The state that is maintained by this process function */
    private ValueState<GlobalKeyedVariables> state;

    @Override
    public void open(Configuration parameters) throws Exception {
        state = getRuntimeContext().getState(new ValueStateDescriptor<>("myState", GlobalKeyedVariables.class));
    }
    
	@Override
	public void processElement(BTSEvent value, Context ctx, Collector<String> out) throws Exception {
		GlobalKeyedVariables current = state.value();
        if (current == null) {
            current = new GlobalKeyedVariables();
        }
		// update the state
		if (value.well_deserialized) {
			if (current.count == 0) {
				current.max = value.value;
				current.min = value.value;
				current.sum = value.value;
			} else {
				if (value.value > current.max) {
					current.max = value.value;
				} else if (value.value < current.min) {
					current.min = value.value;
				}
				if (value.is_alarm_active) {
					current.number_alarms += 1;
				}
				current.sum += value.value;
				current.count++;
			}
		} else {
			current.data_conversion_errors++;
		}
		double mean = current.sum / current.count;
		out.collect("{\"type\":\"Global Analytic\"," +
				"\"key\":{\"station_id\":" + value.station_id +
					", \"datapoint_id\":" + value.datapoint_id +
					", \"alarm_id\":" + value.alarm_id +
				"}" +
				"\"data\":{ \"mean\":" + mean +
					", \"max\":" + current.max +
					", \"min\":" + current.min +
					", \"counter\":" + current.count +
					", \"alarms\":" + current.number_alarms +
				"}}");
		out.collect("{\"type\":\"Global Metric\","+
				"\"key\":{\"station_id\":" + value.station_id +
				", \"datapoint_id\":" + value.datapoint_id +
				", \"alarm_id\":" + value.alarm_id +
				"}" +
				" \"data\":{ \"data_conversion_errors\":"+current.data_conversion_errors+"}}");
		

        // write the state back
        state.update(current);
	}
}
