import pika
import json

def send_query_to_rabbitmq(query):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare a queue
    channel.queue_declare(queue='query_queue')

    # Publish query to the queue
    channel.basic_publish(exchange='', routing_key='query_queue', body=json.dumps({'query': query}))
    print(" [x] Sent query to RabbitMQ")
    connection.close()
