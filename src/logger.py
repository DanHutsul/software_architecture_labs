import uuid
from flask import Flask, request
import requests
import sys
import uuid
import hazelcast
import consul
import random
app = Flask(__name__)

session = consul.Consul('localhost', 8500)
session.agent.service.register('logging-service', port=int(sys.argv[1]), service_id='l'+str(uuid.uuid4()))



@app.route('/logging', methods=['GET', 'POST'])
def logging_requests():
    if request.method == 'GET':
        client = hazelcast.HazelcastClient(cluster_members=['127.0.0.1:5701', '127.0.0.1:5702', '127.0.0.1:5703'])
        my_map = client.get_map(session.kv.get('map')[1]['Value'].decode("utf-8")).blocking()
        response = ', '.join(my_map.values())
        client.shutdown()
        return response
        
    if request.method == 'POST':
        
        uuid = request.form['id']
        msg = request.form['msg']
        
        print("msg = ", msg, " UUID = ", uuid, "\n")
        client = hazelcast.HazelcastClient(cluster_members=['127.0.0.1:5701', '127.0.0.1:5702', '127.0.0.1:5703'])
        my_map = client.get_map(session.kv.get('map')[1]['Value'].decode("utf-8")).blocking()
        my_map.put(uuid, msg)
        client.shutdown()
        return 'returned str'

if __name__ == '__main__':
    from sys import argv
    if len(argv) != 2:
    	sys.exit(0)
    app.run(port=int(sys.argv[1]))
