import elasticsearch


mappings = {
    "temperatures": {
        "settings": {
            "number_of_shards": 1
        },
        "mappings": {
            "properties": {
                "client": {"type": "keyword"},
                "ip": {"type": "ip"},
                "temperatures": {"type": "object"},
                "datetime": {"type": "date"}
            }
        }
    },
    "memory": {
        "settings": {
            "number_of_shards": 1
        },
        "mappings": {
            "properties": {
                "client": {"type": "keyword"},
                "ip": {"type": "ip"},
                "total": {"type": "integer"},
                "free": {"type": "integer"},
                "used": {"type": "integer"},
                "cached": {"type": "integer"},
                "usage": {"type": "float"},
                "datetime": {"type": "date"}
            }
        }
    },
    "cpu": {
        "settings": {
            "number_of_shards": 1
        },
        "mappings": {
            "properties": {
                "client": {"type": "keyword"},
                "ip": {"type": "ip"},
                "user": {"type": "float"},
                "system": {"type": "float"},
                "nice": {"type": "float"},
                "idle": {"type": "float"},
                "wait": {"type": "float"},
                "hardware_interrupt": {"type": "float"},
                "software_interrupt": {"type": "float"},
                "steal": {"type": "float"},
                "usage": {"type": "float"},
                "datetime": {"type": "date"}
            }
        }
    },
    "storage": {
        "settings": {
            "number_of_shards": 1
        },
        "mappings": {
            "properties": {
                "client": {"type": "keyword"},
                "ip": {"type": "ip"},
                "storage": {"type": "object"},
                "total_storage": {"type": "integer"},
                "used_storage": {"type": "integer"},
                "free_storage": {"type": "integer"},
                "usage": {"type": "float"},
                "datetime": {"type": "date"}
            }
        }
    },
    "network": {
        "settings": {
            "number_of_shards": 1
        },
        "mappings": {
            "properties": {
                "client": {"type": "keyword"},
                "ip": {"type": "ip"},
                "in": {"type": "float"},
                "out": {"type": "float"},
                "datetime": {"type": "date"}
            }
        }
    }
}

database = elasticsearch.Elasticsearch()
for index in mappings:
    database.indices.create(index=index, body=mappings[index])
