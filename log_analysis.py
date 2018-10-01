import psycopg2

def first_query(dbname):
    """Queries the PostgreSQL database and answers the following question:
            'What are the most popular three articles of all time?'
     """
    first_query = """SELECT articles.title, count(*) as views
                     FROM articles, log
                     WHERE log.path = CONCAT('/article/', articles.slug)
                            AND log.status LIKE '%200%'
                     GROUP BY articles.title
                     ORDER BY views DESC
                     LIMIT 3;
                  """

    result = query_database(dbname=dbname, query=first_query)
    print_first_query(result=result)

def print_first_query(result):
    """Prints the rows of the first query result."""
    print_border()
    print("Most popular three articles of all time:\n")
    for (title, views) in result:
        print("\"" + str(title) + "\"" + " -- " + str(views) + " views")
    print_border()

def second_query(dbname):
    """Queries the PostgreSQL database and answers the following question:
            'Who are the most popular article authors of all time?'
    """
    second_query = """SELECT authors.name, count(*) as views
                      FROM authors, articles, log
                      WHERE authors.id = articles.author
                            AND log.path = CONCAT('/article/', articles.slug)
                            AND log.status LIKE '%200%'
                      GROUP BY authors.name
                      ORDER BY views DESC;
                   """
    result = query_database(dbname=dbname, query=second_query)
    print_second_query(result=result)

def print_second_query(result):
    """Prints the rows of the second query result."""
    print_border()
    print("Most popular article authors:\n")
    for (author, views) in result:
        print(str(author) + " -- " + str(views) + " views")
    print_border()

def third_query(dbname):
    """Queries the PostgreSQL database and answers the following question:
            On which days did more than 1% of requests lead to errors?
    """
    third_query = """WITH total_logs AS (
                     SELECT DATE(time) as date, count(*) as num_total_logs
                     FROM log
                     GROUP BY date
                  ),                
                 error_logs AS (
                     SELECT DATE(time) as date, count(*) as num_error_logs
                     FROM log
                     WHERE status LIKE'%4%' OR status LIKE'%5%'
                     GROUP BY date	
                 ),                
                 error_rates AS (
                     SELECT DATE(error_logs.date) as date ,
                     ROUND(((error_logs.num_error_logs::float / total_logs.num_total_logs::float)::numeric * 100), 2)
                           AS error_percentage
                     FROM total_logs, error_logs
                     WHERE total_logs.date = error_logs.date
                 )                
                 SELECT TO_CHAR(date, 'FMMonth DD YYYY'), error_percentage as percentage 
                 FROM error_rates
                 WHERE error_percentage > 1
                 ORDER BY error_percentage DESC;
                 """
    result = query_database(dbname=dbname, query=third_query)
    print_third_query(result=result)

def print_third_query(result):
    """Prints the rows of the third query result."""
    print_border()
    print("Days that had more than 1% of requests lead to errors:\n")
    for (date, percentage) in result:
        print(str(date) + " -- " + str(percentage) + "% errors")
    print_border()

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

def print_border():
    """Prints a border of 50 '-' characters for clearer output. """
    print("-" * 50)

if __name__ == "__main__":
    DBNAME = "news"
    first_query(dbname=DBNAME)
    second_query(dbname=DBNAME)
    third_query(dbname=DBNAME)