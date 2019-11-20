package storm.mqtt;


/**
 * Represents an MQTT Message consisting of a topic string (e.g. "/users/customer1")
 * and a byte array message/payload.
 *
 */
public class MqttMessage {
	private String topic;
    private byte[] message;


    public MqttMessage(String topic, byte[] payload) {
        this.topic = topic;
        this.message = payload;
    }

    public byte[] getMessage() {
        return this.message;
    }

    public String getTopic() {
        return this.topic;
    }
}
