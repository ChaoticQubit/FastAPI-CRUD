import psycopg2 as pg
from psycopg2.extras import RealDictCursor
import time

class TableConstants:
    POSTSTABLE = "posts"
    POSTCOLS = ("title", "content", "published", "likes")

    def parseCols(self, cols):
        if cols == None:
            return "*"
        return f"""({", ".join(cols)})"""

    def parseWhereClause(self, whereClause):
        if whereClause == None:
            return ""
        return f" WHERE {whereClause} "
    
    def parseOrderByClause(self, orderByClause):
        if orderByClause == None:
            return ""
        return f" ORDER BY {orderByClause} "
    
    def parseLimitClause(self, limitClause):
        if limitClause == None:
            return ""
        return f" LIMIT {limitClause} "
    
    def parseOffsetClause(self, offsetClause):
        if offsetClause == None:
            return ""
        return f" OFFSET {offsetClause} "
    
    def parseLikeClause(self, likeClause):
        if likeClause == None:
            return ""
        return f" LIKE {likeClause} "

    def clauseParser(self, cols, where, limit, offset, orderby, like):
        cols = self.parseCols(cols)
        whereStmt = self.parseWhereClause(where)
        limitStmt = self.parseLimitClause(limit)
        offsetStmt = self.parseOffsetClause(offset)
        orderbyStmt = self.parseOrderByClause(orderby)
        likeStmt = self.parseLikeClause(like)
        return cols, whereStmt, limitStmt, offsetStmt, orderbyStmt, likeStmt

class Database:
    # Constructor - Establishing Database Connection
    def __init__(self):
        while True:
            try:
                self.connection = pg.connect(
                    host = "localhost",
                    port = '5433',
                    database = "fastapi",
                    user = "postgres",
                    password = "ARMANS123",
                    cursor_factory = RealDictCursor
                )
                self.connection.autocommit = True
                self.cursor = self.connection.cursor()
                print("Connection to Database was successfull.")
                break
            except Exception as error:
                print("Error while connecting to Database: ", error)
                time.sleep(2)
    
    def execute(self, query, params=None):
        res = self.cursor.execute(query, params)
        return self.cursor.fetchall()

    # def create_table(self, tableName):
    #     query = f"""CREATE TABLE IF NOT EXISTS {tableName} (
    #         id SERIAL PRIMARY KEY,
    #         title VARCHAR(255) NOT NULL,
    #         content TEXT NOT NULL,
    #         published BOOLEAN NOT NULL,
    #         rating FLOAT
    #     )"""
    #     self.execute(query)
    #     print("Table created.")
    
    def insert(self, tableName, cols, post):
        query = f"""INSERT INTO {tableName} ({", ".join(cols)}) VALUES (%s, {"%s, " * (len(cols) - 2)}%s) RETURNING *"""
        return self.execute(query, tuple([post[colName] for colName in cols]))
    
    def select(self, tableName, cols=None, where=None, limit=None, offset=None, orderby=None, like=None):
        tc = TableConstants()
        cols, whereStmt, limitStmt, offsetStmt, orderbyStmt, likeStmt = tc.clauseParser(cols, where, limit, offset, orderby, like)
        query = f"""SELECT {cols} FROM {tableName}""" + whereStmt + likeStmt + orderbyStmt + limitStmt + offsetStmt
        return self.execute(query)
    
    def update(self, tableName, cols, where, post):
        query = f"""UPDATE {tableName} SET title = %s, content = %s, published = %s, rating = %s WHERE {where} RETURNING *"""
        return self.execute(query, tuple([post[colName] for colName in cols]))
    
    def delete(self, tableName, post_id):
        query = f"DELETE FROM {tableName} WHERE id = %s RETURNING *"
        self.execute(query, (post_id,))
        return "Post deleted"
    
    def close(self):
        self.cursor.close()
        self.connection.close()
        print("Connection to Database was closed.")

    