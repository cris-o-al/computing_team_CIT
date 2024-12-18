from confluent_kafka import Consumer, KafkaError
import base64
from transcript_audio import intento

# Kafka consumer configuration
kafka_config = {
    'bootstrap.servers': '192.168.29.52:9092',  # Replace with your Kafka broker
    'group.id': 'python-consumer-group',    # Consumer group ID
    'auto.offset.reset': 'earliest'         # Start reading from the earliest message
}
output_path = "C:/Users/Crist/Desktop/Carpeta/hola.wav"
# Kafka topic
kafka_topic = 'topic-m4'  # Replace with your topic name

def consume_messages():
    # Create a Kafka consumer instance
    consumer = Consumer(kafka_config)
    
    # Subscribe to the Kafka topic
    consumer.subscribe([kafka_topic])
    
    print(f"Subscribed to topic: {kafka_topic}")
    
    try:
        while True:
            # Poll for messages
            message = consumer.poll(timeout=1.0)  # Wait 1 second for a message
            
            if message is None:
                # No new message
                continue
            if message.error():
                # Handle errors
                if message.error().code() == KafkaError._PARTITION_EOF:
                    print(f"End of partition reached {message.topic()} [{message.partition()}] at offset {message.offset()}")
                else:
                    print(f"Error: {message.error()}")
            else:
                # Successfully received a message
                try:
                    with open(output_path, 'wb') as wav_file:
                        wav_file.write(base64.b64decode(message.value()))
                        intento(output_path)
                       # wav_file.write(message.value())
                        print(f"WAV file successfully written to {output_path}")
                except Exception as e:
                    print(f"Error writing WAV file: {e}")
                    print(f"Received message: {message.value().decode('utf-8')} (from topic: {message.topic()}, partition: {message.partition()})")
    except KeyboardInterrupt:
        print("Consumer interrupted.")
    finally:
        # Close the consumer to free up resources
        consumer.close()

if __name__ == "__main__":
    consume_messages()
