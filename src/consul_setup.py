import consul
if __name__ == "__main__":
    c = consul.Consul()
    c.kv.put("hazel-ports", "127.0.0.1:5701 127.0.0.1:5702 127.0.0.1:5703")
    c.kv.put("map", "log-map")
    c.kv.put("queue", "messages-queue")