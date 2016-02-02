from elasticsearch import Elasticsearch
from datetime import datetime

es = Elasticsearch(
    [{'host':'172.99.73.160'}]
)

def put_event(event):
    es.index(index='my_index', doc_type='events', id=event['event']['id'], body=event)