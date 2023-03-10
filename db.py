import mysql.connector
import logging as logger
import os
from dotenv import load_dotenv
load_dotenv(os.path.abspath(".") + "/config.env")
class Database:
    __instance = None
    def __init__(self):
        if self.__instance is None or self.__instance.is_connected() == False:

            self.__instance = mysql.connector.connect(
                user=os.getenv("USER"),
                password=os.getenv("PASSWORD"),
                host=os.getenv("HOST"),
                database=os.getenv("DATABASE"),
            )
            self.__instance.autocommit = False
    def query(self, query, autoCommit=None, fetch="ALL"):
        try:
            cursor = self.__instance.cursor()
            result = cursor.execute(query)
            if autoCommit is not None:
                self.__instance.commit()
                operation = True if cursor.lastrowid == 0 else {"id": cursor.lastrowid}
                return {"result": operation}
            fields = [field_md[0] for field_md in cursor.description]
            if fetch != "SINGLE":
                result = [dict(zip(fields, row)) for row in cursor.fetchall()]
                return {"result": result}
            else:
                result = [dict(zip(fields, row)) for row in cursor.fetchone()]
                return {"result": result}
        except Exception as e:
            return {"result": None, "error": e, "query": query}
            logger.error(e)
        finally:
            if self.__instance.is_connected():
                logger.info("Connected.")

