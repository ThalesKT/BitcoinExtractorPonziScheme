from neo4j import GraphDatabase
from Src.Config import *


class Database:
    _instance = None

    def __init__(self):
        self.driver = GraphDatabase.driver(URI, auth=NEO4J_AUTH)
        self.session = self.driver.session()

    def close(self):
        self.driver.close()

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = Database()
        return cls._instance

    #Tx is the session
    def query(self, query):
        return self.session.run(query)

