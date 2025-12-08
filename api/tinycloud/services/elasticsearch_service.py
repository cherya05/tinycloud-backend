from elasticsearch import Elasticsearch
import os

class ElasticsearchService:
    def __init__(self):
        self.es_host = os.getenv("ELASTICSEARCH_HOST", "elasticsearch-master")
        self.es_port = os.getenv("ELASTICSEARCH_PORT", 9200)
        self.es_url = f"http://{self.es_host}:{self.es_port}"
        self.client = Elasticsearch(self.es_url)
    
    def index_document(self, index_name, document):
        return self.client.index(index=index_name, body=document)

    def search(self, index_name, query):
        return self.client.search(index=index_name, body=query)