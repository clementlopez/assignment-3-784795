public class Customer1TupleMapper implements MqttTupleMapper {
    public MqttMessage toMessage(ITuple tuple) {
        String topic = "users/" + tuple.getStringByField("userId");
        byte[] payload = tuple.getStringByField("message").getBytes();
        return new MqttMessage(topic, payload);
    }
}