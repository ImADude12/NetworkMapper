import json
from neo4j import GraphDatabase


class Neo4jConnection:

    def __init__(self, uri, user, pwd):
        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__driver = None
        try:
            self.__driver = GraphDatabase.driver(
                self.__uri, auth=(self.__user, self.__pwd))
        except Exception as e:
            print("Failed to create the driver:", e)

    def close(self):
        if self.__driver is not None:
            self.__driver.close()

    def query(self, query, parameters=None, db=None):
        assert self.__driver is not None, "Driver not initialized!"
        session = None
        response = None
        try:
            session = self.__driver.session(
                database=db) if db is not None else self.__driver.session()
            response = list(session.run(query, parameters))
        except Exception as e:
            print("Query failed:", e)
        finally:
            if session is not None:
                session.close()
        return response


# Read creds from local json - avoid having them on git!
with open('neo4j_creds.json', 'r') as f:
    neo4j_creds = json.load(f)

print(neo4j_creds['uri'], neo4j_creds['username'])


conn = Neo4jConnection(uri=neo4j_creds['uri'],
                       user=neo4j_creds['username'],
                       pwd=neo4j_creds['password'])
print(conn.query('MATCH (n1)-[*]->(n2) RETURN * LIMIT 25'))
