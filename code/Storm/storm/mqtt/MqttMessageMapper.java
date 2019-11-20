package storm.mqtt;

import java.io.Serializable;
import org.apache.storm.tuple.Fields;
import org.apache.storm.tuple.Values;

/**
 * Represents an object that can be converted to a Storm Tuple from an AckableMessage,
 * given a MQTT Topic Name and a byte array payload.
 */
public interface MqttMessageMapper extends Serializable {
    /**
     * Convert a `MqttMessage` to a set of Values that can be emitted as a Storm Tuple.
     *
     * @param message An MQTT Message.
     * @return Values representing a Storm Tuple.
     */
    Values toValues(MqttMessage message);

    /**
     * Returns the list of output fields this Mapper produces.
     *
     * @return the list of output fields this mapper produces.
     */
    Fields outputFields();
}