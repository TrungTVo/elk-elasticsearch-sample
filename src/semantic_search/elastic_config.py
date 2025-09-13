from elasticsearch import Elasticsearch, helpers

class MyElasticsearch:
    es: Elasticsearch

    def __init__(self, host: str = "http://localhost:9200"):
        self.es = Elasticsearch(host)

    def get_client(self) -> Elasticsearch:
        return self.es
    
    def create_index(self, index_name: str, mapping: dict):
        if not self.es.indices.exists(index=index_name):
            self.es.indices.create(index=index_name, body=mapping)

    def delete_index(self, index_name: str):
        if self.es.indices.exists(index=index_name):
            self.es.indices.delete(index=index_name)

    def insert_document(self, index_name: str, document: dict):
        self.es.index(index=index_name, document=document)

    def bulk_insert_documents(self, index_name: str, documents: list):
        helpers.bulk(self.es, documents, index=index_name)

    # Perform semantic search (kNN search)
    def semantic_search(self, index_name: str, knn: dict, source: list = None):
        response = self.es.search(
            index=index_name,
            knn=knn,
            source=source
        )
        return response
