#!/usr/bin/python3

import psycopg2

DBNAME = "news"

'''
Since these lines are repeating in different functions,
its better to implement a function and reuse that.

def connect(database_name="news"):
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("<error message>")

def yourFunc():
    db, cursor = connect()

    query = "SQL STATEMENT"
    cursor.execute(query)

    db.close()
'''


def question1():

    # What are the most popular three articles of all time?

    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()

    # postgresql query

    query = """
    SELECT articles.title, COUNT(articles.slug) AS num
    FROM log JOIN articles
    ON log.path LIKE CONCAT('%', '/', articles.slug)
    GROUP BY articles.title
    ORDER BY num DESC LIMIT 3;
    """

    c.execute(query)
    popular_articles = c.fetchall()

    # printing out the results

    print("\n")
    print("1. What are the most popular three articles of all time?")
    print("\n")

    for x in range(0, len(popular_articles)):
        print("\"{}\" - {} views".format(popular_articles[x][0],
              popular_articles[x][1]))

    print("\n")

    db.close()


def question2():

    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()

    # Who are the most popular article authors of all time?

    # postgresql query

    query = """
    SELECT authors.name, COUNT(author) AS num
    FROM authors

    JOIN

    (SELECT articles.author
    FROM log JOIN articles
    ON log.path LIKE CONCAT('%', '/', articles.slug))

    AS author

    ON authors.id = author.author
    GROUP BY authors.name
    ORDER BY num DESC;
    """

    c.execute(query)
    popular_authors = c.fetchall()

    # printing out the results

    print("2. Who are the most popular article authors of all time?")
    print("\n")

    for x in range(0, len(popular_authors)):
        print("{} - {} views".format(popular_authors[x][0],
              popular_authors[x][1]))

    print("\n")

    db.close()


def question3():

    # On which days did more than 1% of requests lead to errors?

    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()

    # postgresql query

    query = """
    SELECT TO_CHAR(date, 'FMMonth FMDD, YYYY') AS date, error_rate

    FROM

    (WITH

    total AS

    (SELECT DATE(time), COUNT(status) AS num
    FROM log
    GROUP BY DATE(time)),

    error AS

    (SELECT DATE(time), COUNT(status) AS num
    FROM log WHERE status NOT LIKE '%200%'
    GROUP BY DATE(time))

    SELECT total.date,
    ROUND(CAST(error.num/CAST(total.num AS float)*100 AS numeric),1)
    AS error_rate
    FROM total, error
    WHERE total.date = error.date)

    AS error_rate

    WHERE error_rate >= 1;
    """

    c.execute(query)
    error_rate = c.fetchall()

    # printing out the results

    print("3. On which days did more than 1% of requests lead to errors?")
    print("\n")
    print("{} - {}% errors".format(error_rate[0][0], error_rate[0][1]))
    print("\n")

    db.close()


'''
Here is a bit simpler version to retrieve the correct results for 3rd section.

select to_char(date, 'FMMonth FMDD, YYYY'), err/total as ratio
       from (select time::date as date,
                    count(*) as total,
                    sum((status != '200 OK')::int)::float as err
                    from log
                    group by date) as errors
       where err/total > 0.01;
'''

# Activating the PostgreSQL and achieving the results

if __name__ == "__main__":
    question1()
    question2()
    question3()

'''
The if __name__ == '__main__': section makes sure that the code in that section
is only run when this program is executed directly, and not when it is imported
as a module.

'''
