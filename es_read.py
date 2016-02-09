from elasticsearch import Elasticsearch
import elasticsearch.helpers
import click

@click.command()
@click.argument('eshost')
def hepmcreader(eshost):
    es = Elasticsearch([{'host':eshost}])
    scan = elasticsearch.helpers.scan(es,
        query = {
            "query": { "match_all": {} }
        },
        index = 'my_index',
        doc_type = 'events'
    )

    for x in scan:
        print x['_source']['event']['hepmcstring']
        
if __name__ == '__main__':
    hepmcreader()