package storm.mqtt;

import java.io.Serializable;

import org.apache.storm.tuple.ITuple;

/**
 * Given a Tuple, converts it to an MQTT message.
 */
public interface MqttTupleMapper extends Serializable {

    /**
     * Converts a Tuple to a MqttMessage.
     * @param tuple the incoming tuple
     * @return the message to publish
     */
    MqttMessage toMessage(ITuple tuple);

}
