import pika
import json
from query_data import query_rag

def callback(ch, method, properties, body):
    # Extract query from the message
    query_data = json.loads(body)
    query = query_data['query']
    
    # Process query with IR_Search function
    context_response = query_rag(query)
    
    # Send response to Ollama
    # (Assuming `query_rag` integrates Ollama at the final step)
    response = {"response": context_response}

    # Publish the response to another queue to be sent back to the user
    ch.basic_publish(exchange='', routing_key='response_queue', body=json.dumps(response))
    print(" [x] Sent response back to RabbitMQ")

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    
    # Declare queues
    channel.queue_declare(queue='query_queue')
    channel.queue_declare(queue='response_queue')
    
    channel.basic_consume(queue='query_queue', on_message_callback=callback, auto_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == "__main__":
    main()
