import psycopg2

"""Queries the news database and answers the following question:
        'What are the most popular three articles of all time?'
 """
first_query = ""

"""Queries the news database and answers the following question:
        'Who are the most popular article authors of all time?'
"""
second_query = ""

"""Queries the news database and answers the following question:
        On which days did more than 1% of requests lead to errors?
"""
third_query = ""

def query_database(dbname, query):
    """Queries a PostgreSQL database and returns a query result.
    
    Args:
        dbname (str): the name of the PostgreSQL database
        query (str): the query to be sent to the PostgreSQL database
    Returns:
          A list of tuples, each tuple is is a row of a query result. An empty list is returned if there is no more
          records to fetch.
    """
    try:
        conn = psycopg2.connect("dbname={}".format(dbname))
        cur = conn.cursor()
        cur.execute(query)
        result = cur.fetchall()
        cur.close()
        conn.close()
        return result
    except Exception as e:
        print("Connection to database failed!\n"+str(e))

if __name__ == "__main__":
    pass