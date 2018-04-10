# The fresh_tomatoes.py

fresh_tomatoes.py is a python file that will help you make your movie introducing website very easy!!! Everything is made and all you need to do Is just put the information about the movies you like! And it will turn it to a awesome website!

## What python file do i have to open?
___

You can see there are 3 python file are included

* `fresh_tomatoes.py`
* `entertainment_center.py`
* `media.py`

You don't need to touch the `fresh_tomatoes.py` or `media.py`
All you need to open is `entertainment_center.py`

## How to modify? Follow this steps!
___
### 1. You need to make instance(object) about your favorite movie! 

This instance will have 3 information about the movie! 
`Title`, `movie poster image url`, and `movie youtube trailer url`! 
To do this make some instance like this!
```
[instance_name] = media.Movie("self.title",
                              "self.poster_image_url",
                              "self.trailer_youtube_url")
```
Once instance, one movie! So make as much as you want!

### 2. Choose your html file's title! 
```
choose_html_title = "[the title you want]"
```
Just add what you want inside the parenthesis! 
`file name`, `html title`, and the `title inside the webpage` 
will change as what you choosed!

### 3. Merge all instance about movies!

It's almost there! You put all your informations and its ready to activate! 
You need to merge your instance of movies to array! Like this!
```
movies = [(movie instance),(movie instance),(movie instance)]
```
You could check the sample code when you open `entertainment_center.py`

## How to run the application?
___

Everything is done! Its time to see your website!

The file run the application is `entertainment_center.py`!
So you just open it with your python IDLE and
 **click the menu [Run] - [Run Module] ** or **Press F5**

Have Fun!

## Who am I?
___
I am a duck from konkuk Univ illgamho lake!
Hello humans!

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
