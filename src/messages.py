import uuid
from flask import Flask, request
import requests
import sys
import uuid
import hazelcast
import consul
import random
app = Flask(__name__)

session = consul.Consul('localhost')
session.agent.service.register('messages-service', port=int(sys.argv[1]), service_id='m'+str(uuid.uuid4()))
msg_data = []

@app.route('/messages', methods=['GET', 'POST'])
def messages_requests():
    client = hazelcast.HazelcastClient()
    msg_q = client.get_queue(session.kv.get('queue')[1]['Value'].decode("utf-8")).blocking()
    while not msg_q.is_empty():
        msg_data.append(msg_q.take())
        print('Message = ' + msg_data[-1])
    response = ','.join(msg_data)
    client.shutdown()
    return response

if __name__ == '__main__':
    from sys import argv
    if len(argv) != 2:
    	sys.exit(0)
    app.run(port=int(sys.argv[1]))
