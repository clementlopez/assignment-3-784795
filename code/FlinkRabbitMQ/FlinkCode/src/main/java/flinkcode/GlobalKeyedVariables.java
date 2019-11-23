package main.java.flinkcode;

public class GlobalKeyedVariables {
	// Analytics
	public long count;
    public float max;
    public float min;
    public double sum;
    public long number_alarms;
    
    // Metrics
    public long data_conversion_errors;

	public GlobalKeyedVariables() {
		this.count = 0;
		this.max = 0;
		this.min = 0;
		this.sum = 0;
		this.number_alarms = 0;
		this.data_conversion_errors = 0;
	}
}
