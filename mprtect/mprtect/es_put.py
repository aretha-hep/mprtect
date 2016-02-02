from elasticsearch import Elasticsearch
from datetime import datetime


def get_putter(elastic_ip):
    es = Elasticsearch(
        [{'host':elastic_ip}]
    )
    def put_event(event):
        es.index(index='my_index', doc_type='events', id=event['event']['id'], body=event)
    return put_event