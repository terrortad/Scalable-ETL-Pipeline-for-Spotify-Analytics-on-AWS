from kafka import KafkaProducer
import pandas as pd
import json

producer = KafkaProducer(
    bootstrap_servers='ample-bulldog-14625-eu1-kafka.upstash.io:9092',
    sasl_mechanism='SCRAM-SHA-256',
    security_protocol='SASL_SSL',
    sasl_plain_username='YW1wbGUtYnVsbGRvZy0xNDYyNSRNj_2vbSptJffUSEZmuA_2z9oWGrTvwFplI_U',
    sasl_plain_password='MmRlMzA2ODEtMzNlYS00OWRlLWE0MmEtNzJjNDY2ODFhOTQ4'
)

tracks = pd.read_csv('tracks.csv')


for dt in tracks.to_dict(orient='records'):
    data = json.dumps(dt).encode('utf-8')

    try:
        result = producer.send('tracks', data).get(timeout = 60)
        print("Message produced: result")
    except Exception as e:
        print(f"Error producing message: {e}")
producer.close()