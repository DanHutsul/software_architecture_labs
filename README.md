# Lab 1: Microservices basics

## Requirements:
- httpserver
- requests
- uuid
## Usage:
Run the services:
```
python src/facade.py
python src/logger.py
python src/messages.py
```

Send POST/GET requests:

```
curl -X POST http://localhost:8080 -d "Test message"

curl -X GET http://localhost:8080
```

## Results:
Task1Output.pdf