//import org.apache.storm.mqtt.MqttMessageMapper;

/**
 * Given a topic name: "users/{user}"
 * and a payload of "{station_id},{datapoint_id},{alarm_id},{event_time},{value},{valueThreshold},{isActive}"
 * emits a tuple containing the payloads
 *
 */
public class Customer1MessageMapper implements MqttMessageMapper {
    private static final Logger LOG = LoggerFactory.getLogger(Customer1MessageMapper.class);


    public Values toValues(MqttMessage message) {
        String topic = message.getTopic();
        String[] topicElements = topic.split("/");
        String[] payloadElements = new String(message.getMessage()).split(",");

        return new Values(Integer.parseInt(payloadElements[0]), Integer.parseInt(payloadElements[1]),
        		Integer.parseInt(payloadElements[2]), payloadElements[3], Float.parseFloat(payloadElements[4]), 
                Float.parseFloat(payloadElements[5]), Boolean.parseBoolean(payloadElements[6]));
    }

    public Fields outputFields() {
        return new Fields("station_id", "datapoint_id", "alarm_id", "event_time", "value", "valueThreshold", "isActive");
    }
}