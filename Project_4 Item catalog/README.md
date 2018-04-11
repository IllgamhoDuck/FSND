# Item Catalog project - AiLY

![Aily](https://github.com/IllgamhoDuck/FSND/blob/master/Project_5%20Neighborhood%20Map/full.png)

## Greeting Humans! I'm the duck from illgamho lake! QUARK!

Modern web applications perform a variety of functions and provide amazing features and utilities to their users. but deep down, it’s really all just creating, reading, updating and deleting data. In this project, we will combine your knowledge of building dynamic websites with persistent data storage to create a web application that provides a compelling service to your users. By using Python framework Flask we will develop a RESTful web application.

The main function we develop is

1. **CRUD(CREATE, READ, UPDATE, DELETE)** - Use database by SQLAlchemy
2. **SERVER REPONSE** - Use flask framework to make a server
3. **PROVIDE API** - Json endpoint
4. **OAUTH AUTHENTICATION** - Use third-party API
5. **LOGIN/LOGOUT** - Made by python code
6. **RESPONSIVE DESIGN** - Made by using HTML/CSS
7. **RATE LIMIT** - Made by python code

## The program you need
___

* Virtual Box
* Vagrant
* Python

This project is written by python and it will use virtual machine to run SQlite database. And Vagrant will make you use this virtual machine much easier! If you don't have each of them install it! Instructions on how to do so can be found on the websites as well as in [**HERE**](https://www.udacity.com/wiki/ud088/vagrant)..

### When your finished installing both now follow the next step.

## What this project includes?
___

First You will see a vagrant folder alone.
Now follow this root.

### [vagrant]-[catalog]

At `[catalog]` folder you will see this files.

* static - **Folder filled with image and CSS file!**
* templates - **Folder filled with HTML file!** 
* Ai.db - **The Website information will stored in this SQlite database!**
* Ai.py- **Server side code written by flask**
* Ai_ratelimit_test.py - **Testing the rate limit function works!**
* Aimodels.py - **Creating SQlite database using SQLAlchemy! PostgreSQL Code included!**
* Aimodels_populating.py - **Fill the database**
* client_secrets.json - **To use the GOOGLE OAUTH**
* fb_client_secrets.json - **To use the FACEBOOK OAUTH**

Now lets activate this project.

## How to run the application?
___
### 1. Go to vagrant folder and run the shell

Git bash works the same!

Enter 
```
vagrant up
```

And after it is done enter

```
vagrant ssh
```

Now your ready to go! you just logged in the vagrant


### 2. Navigate to the folder [catalog]

Maybe this will help you!

```
cd / => cd vagrant/ => cd catalog/
```

Now your there! It's time to run the python code!

### 3. Run the [Ai.py]!

```
python Ai.py
```
It's all done! Now the server is running!
### 4. See the Webpage!

Here is the link!
**[http://localhost:8000](http://localhost:8000)**!

Have Fun!

### Tip. Way to make database

Just impletement the below code by order. 
Then db file will be created! 
But in here it is already done!
So if you wanna try it delete Ai.db and try it!
```
python Aimodels.py
python Aimodels_populating.py
```


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
