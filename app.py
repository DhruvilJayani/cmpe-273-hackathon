from flask import Flask, request, jsonify, send_from_directory
from rabbitmq_send import send_query_to_rabbitmq
import pika
import json
import threading
import redis  # Import Redis library

app = Flask(__name__)

# Initialize Redis client
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# Shared variable to store the latest response
latest_response = None

def rabbitmq_listener():
    global latest_response
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    
    # Declare the response queue
    channel.queue_declare(queue='response_queue')

    def callback(ch, method, properties, body):
        global latest_response  # Declare as global to modify the variable
        # Process the incoming message and update the latest response
        latest_response = json.loads(body).get('response')
        print("Received response:", latest_response)

    channel.basic_consume(queue='response_queue', on_message_callback=callback, auto_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

@app.route("/")
def home():
    return send_from_directory('', 'index.html')  

@app.route('/submit_query', methods=['POST'])
def submit_query():
    global latest_response  
    data = request.get_json()
    query = data['query']

    # Check Redis cache for the query response
    cached_response = redis_client.get(query)
    if cached_response:
        return jsonify({"response": cached_response})

    # If not cached, send the query to RabbitMQ
    send_query_to_rabbitmq(query)

    while latest_response is None:
        pass  

    response = latest_response
    latest_response = None  

    # Cache the response in Redis with a timeout (e.g., 60 seconds)
    redis_client.setex(query, 60, response)
    
    return jsonify({"response": response})

if __name__ == "__main__":
    
    listener_thread = threading.Thread(target=rabbitmq_listener)
    listener_thread.daemon = True  
    listener_thread.start()

    app.run(port=5000)
