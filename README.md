# software_architecture_labs
## Prerequisite
Consul
The same as in previous labs
## Instructions
Launch 3 Hazelcast Nodes  
Launch Consul using 
```
sudo ./scripts/start_consul.sh
```
Launch Services
```
sudo python3 ./src/facade.py 8080
sudo python3 ./src/messages.py 8081
sudo python3 ./src/messages.py 8082
sudo python3 ./src/logger.py 8083
sudo python3 ./src/logger.py 8084
sudo python3 ./src/logger.py 8085
```
Send POST/GET requests
```
curl -X POST http://localhost:8080 -H 'Content-Type: application/json' -d '{"msg":"hello1"}'
curl -X GET http://localhost:8080
```
