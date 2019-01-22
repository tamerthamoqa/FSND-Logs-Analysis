#!/usr/bin/env python3
import psycopg2


def popular_articles(cursor):
    """Queries the PostgreSQL database and answers the following question:
            'What are the most popular three articles of all time?'
    """
    query = """SELECT articles.title, count(*) as views
                     FROM articles, log
                     WHERE log.path = CONCAT('/article/', articles.slug)
                            AND log.status = '200 OK'
                     GROUP BY articles.title
                     ORDER BY views DESC
                     LIMIT 3;"""
    first_line = "Most popular three articles of all time:\n"
    template = "\"{}\" -- {} views"

    result = query_database(cursor=cursor, query=query)
    print_query_results(result=result, template=template,
                        first_line=first_line)


def popular_authors(cursor):
    """Queries the PostgreSQL database and answers the following question:
            'Who are the most popular article authors of all time?'
    """
    query = """SELECT authors.name, count(*) as views
                      FROM authors, articles, log
                      WHERE authors.id = articles.author
                            AND log.path = CONCAT('/article/', articles.slug)
                            AND log.status = '200 OK'
                      GROUP BY authors.name
                      ORDER BY views DESC;"""
    template = "{} -- {} views"
    first_line = "Most popular article authors:\n"
    result = query_database(cursor=cursor, query=query)
    print_query_results(result=result, template=template,
                        first_line=first_line)


def error_days(cursor):
    """Queries the PostgreSQL database and answers the following question:
            'On which days did more than 1% of requests lead to errors?'
    """
    query = """WITH total_logs AS (
                     SELECT DATE(time) as date, count(*) as num_total_logs
                     FROM log
                     GROUP BY date
                  ),
                 error_logs AS (
                     SELECT DATE(time) as date, count(*) as num_error_logs
                     FROM log
                     WHERE status >= '400'
                     GROUP BY date
                 ),
                 error_rates AS (
                     SELECT DATE(error_logs.date) as date ,
                     ROUND(
                     ((error_logs.num_error_logs::float /
                     total_logs.num_total_logs::float)::numeric * 100), 2)
                           AS error_percentage
                     FROM total_logs, error_logs
                     WHERE total_logs.date = error_logs.date
                 )
                 SELECT TO_CHAR(date, 'FMMonth DD YYYY'), error_percentage
                 FROM error_rates
                 WHERE error_percentage > 1
                 ORDER BY error_percentage DESC;"""
    template = "{} -- {}% errors"
    first_line = "Days that had more than 1% of requests lead to errors:\n"
    result = query_database(cursor=cursor, query=query)
    print_query_results(result=result, template=template,
                        first_line=first_line)


def connect_database(dbname):
    """Opens a conncetion to a PostgreSQL database.

    Args:
        dbname(str): the name of the PostgreSQL database.

    Returns:
        connection object.
        cursor object.
    """
    try:
        connection = psycopg2.connect("dbname={}".format(dbname))
        cursor = connection.cursor()
        return connection, cursor
    except Exception as e:
        print("Connection to database failed!\n" + str(e))


def query_database(cursor, query):
    """Queries a PostgreSQL database and returns a query result.

    Args:
        cursor : cursor object of an open PostgreSQL database connection.
        query (str): the query to be sent to the PostgreSQL database.

    Returns:
        result: A list of tuples, each tuple is is a row of a query result.
        An empty list is returned if there are no more
        records to fetch.
    """
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(str(e))


def close_database(cursor, connection):
    """Closes an open connection to a PostgreSQL database.

    Args:
        cursor object.
        connection object.
    """
    try:
        cursor.close()
        connection.close()
    except Exception as e:
        print(str(e))


def print_query_results(result, template, first_line):
    """Prints the results of a query according to a specified str template.

    Args:
        result: list of tuples from the result of a query database.
        template (str): str template for result to printed as.
        first_line (str): first line that will be printed, used to differentiate
                          between different query outputs.
    """
    print_border()
    print(first_line)
    for row in result:
        print template.format(*row)
    print_border()


def print_border():
    """Prints a border of 50 '-' characters for clearer output. """
    print("-" * 50)


if __name__ == "__main__":
    DBNAME = "news"
    connection, cursor = connect_database(dbname=DBNAME)
    popular_articles(cursor)
    popular_authors(cursor)
    error_days(cursor)
    close_database(connection=connection, cursor=cursor)
