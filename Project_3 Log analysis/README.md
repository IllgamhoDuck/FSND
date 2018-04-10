# Log Analysis project

You've been hired onto a team working on a newspaper site. The user-facing newspaper site frontend itself, and the database behind it, are already built and running. You've been asked to built an internal reporting tool that will use information from the database to discover what kind of articles the site's reader like.

The database contains newspaper articles, as well as the web server log for the site. The log has a database row for each time a reader loaded a web page. Using that information, your code will answer questions about the site's user activity.

This project is to analyse the PostgreSQL with Python code to come up with an answers of 3 questions below.

1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

## The program you need
___

* Virtual Box
* Vagrant

This project will use virtual machine to run PostgreSQL.
And Vagrant will make you use this virtual machine much easier!
If you don't have each of them install it!

### When your finished installing both now follow the next step.

## What this project includes?
___

First You will see a vagrant folder alone.
Now follow this root.

### [vagrant]-[log_analysis]

At `[log_analysis]` folder you will see this files.

* log_analysis_db.py - **Python code to analysis the PostgreSQL DB!**
* newsdata.sql - **The SQL statement code that consist the PostgreSQL DB!**  But this file is deleted because the size is bigger than 100MB
* Project 3 log analysis output.txt - **The result of the Project!**
* README.md - **Its me! Hello!!!**

The Database and python file in the vagrant.

You can check the result of the python file by looking at the Project 3 log analysis output.txt file. Now lets start to look for what to install to activate this projects.

## How this project designed?
___

We use Vagrant to modify the files in virtual box and use PostgreSQL in virtual box.
We created the database inside the virtual box using **newsdata.sql** file inside
the **[log_analysis]** folder

The code to build the database.
```
psql -d news -f newsdata.sql
```

We could analysis the built PostgreSQL DB by using python code!
We use psycopg2 library! We could log in to the PostgreSQL DB and use SQL queries.
Also we could fetch the data from SQL!

Below is the example of the code.

```
import psycopg2

DBNAME = "news"


def question1():

    # What are the most popular three articles of all time?

    db = psycopg2.connect(database=DBNAME)  # log in to PostgreSQL DB using psycopg2!
    c = db.cursor()

    # postgresql query

    query = """
    (PostgreSQL query comes here)
    """
    c.execute(query)  # run the query!
    popular_articles = c.fetchall()  #get the data from sql to python

    # printing out the results

    db.close()  # close the DB
```

Now this is it! This is how the project was built!
And now let's try to run this project!

## How to run the application?
___
### 1. Go to vagrant folder and run the shell

Git bash works the same!

Enter 
```
vagrant up
```

And after is done enter

```
vagrant ssh
```

Now your ready to go! you just logged in the vagrant


### 2. Navigate to the folder [log_analysis]

Maybe this will help you!

```
cd / => cd vagrant/ => cd log_analysis/
```

Now your there! It's time to run the python code!

### 3. Run the [log_analysis_db.py]!

```
python log_analysis_db.py
```
It's all done! Now you will see the project result at the screen!
You can compare it with the **[log analysis output.txt]**!

If you wanna check the SQL itself type
```
psql news
```
in the vagrant! You will just log into the PostgreSQL DB!

Have Fun!


## lincense
___
MIT License

Copyright (c) 2017 illgamho_duck

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
