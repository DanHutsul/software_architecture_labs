import uuid
from flask import Flask, request
from requests import get, post
import sys
import uuid
import hazelcast
import consul
import random


session = consul.Consul(host='localhost', port=8500)
session.agent.service.register('facade-service', port=int(sys.argv[1]), service_id=f"f{str(uuid.uuid4())}")
services = session.agent.services()

app = Flask(__name__)

log_clients = []
msg_clients = []

for key in services:
    if key[0] == 'l':
        log_clients.append('http://localhost:' + str(services[key]['Port']) + '/logging')
    elif key[0] == 'm':
        msg_clients.append('http://localhost:' + str(services[key]['Port']) + '/messages')
        
client = hazelcast.HazelcastClient(cluster_members=session.kv.get('hazel-ports')[1]['Value'].decode("utf-8").split())
msg_q = client.get_queue(session.kv.get('queue')[1]['Value'].decode("utf-8")).blocking()

@app.route('/', methods=['GET', 'POST'])
def requests():
    if request.method == 'GET':
        response_log = get(random.choice(log_clients)).text
        response_msg = get(random.choice(msg_clients)).text
        return 'Messages-service reply: ' + response_msg + '\nLogging-service reply: ' + response_log + '\n'
    elif request.method == 'POST':
        message = request.get_json()
        msg_q.put(str(message["msg"]))
        msg_uuid = str(uuid.uuid4())

        return post(random.choice(log_clients), data={"id": msg_uuid, "msg": message["msg"]}).text

if __name__ == '__main__':
    from sys import argv
    if len(argv) != 2:
    	sys.exit(0)
    app.run(port=int(sys.argv[1]))
