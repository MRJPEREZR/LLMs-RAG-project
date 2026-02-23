# from pymilvus import connections, utility, Collection
# import logging

# class MilvusClient:
#     def __init__(self):
#         self.host = os.getenv("MILVUS_HOST", "localhost")
#         self.port = os.getenv("MILVUS_PORT", "19530")
#         self.collections = {}
    
#     async def connect(self):
#         """Connect to Milvus"""
#         connections.connect(
#             alias="default",
#             host=self.host,
#             port=self.port
#         )
#         logging.info("Connected to Milvus")
        
#     async def get_collection(self, name: str, schema=None):
#         """Get or create collection"""
#         if name in self.collections:
#             return self.collections[name]
            
#         if utility.has_collection(name):
#             collection = Collection(name)
#         else:
#             collection = Collection(name, schema=schema)
        
#         # Load collection into memory for search
#         collection.load()
#         self.collections[name] = collection
#         return collection