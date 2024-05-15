from kafka import KafkaProducer
import pandas as pd
import json

# Kafka Producer configuration
producer = KafkaProducer(
    bootstrap_servers='ample-bulldog-14625-eu1-kafka.upstash.io:9092',
    sasl_mechanism='SCRAM-SHA-256',
    security_protocol='SASL_SSL',
    sasl_plain_username='YW1wbGUtYnVsbGRvZy0xNDYyNSRNj_2vbSptJffUSEZmuA_2z9oWGrTvwFplI_U',
    sasl_plain_password='MmRlMzA2ODEtMzNlYS00OWRlLWE0MmEtNzJjNDY2ODFhOTQ4',
    batch_size=32*1024,  # 32 KB
    linger_ms=10,        # 10 milliseconds
    buffer_memory=33554432,  # 32 MB
    compression_type='gzip'
)

# Load data
print("Loading data...")
tracks = pd.read_csv('albums.csv')
print("Data loaded. Handling missing values...")
tracks.fillna("Unknown", inplace=True)

# Define batch size
batch_size = 100

# Process and send messages in batches
for i in range(0, len(tracks), batch_size):
    batch = tracks.iloc[i:i+batch_size]
    record_dicts = batch.to_dict(orient='records')
    print(f"Processing batch {i//batch_size + 1}...")
    for record in record_dicts:
        data = json.dumps(record).encode('utf-8')
        producer.send('albums', data)
    producer.flush()  # Ensure all messages are sent
    print(f"Batch {i//batch_size + 1} produced successfully.")

# Close producer
producer.close()
print("All messages produced and producer closed.")
