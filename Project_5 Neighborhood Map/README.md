# Neighborhood Map Project

![frontend](https://github.com/IllgamhoDuck/FSND/blob/master/Project_5%20Neighborhood%20Map/full.png)
![frontend](https://github.com/IllgamhoDuck/FSND/blob/master/Project_5%20Neighborhood%20Map/small.png)

Greeting Humans! I'm the duck from illgamho lake! QUARK!

This project pursue to develop single page application featuring a map of the DUCK'S neighborhood HUMANS would like to visit. Functionality to this map including highlighted locations, third-party data about those locations and various ways to browse the content.

The main function we develop is

1. **MVVM** - Using KnockoutJS MVVM Framwork to bind model to view easily
2. **Google Map API** - Creating Map, Marker, Infowindow
3. **Neighborhood list** - Showing the neighborhood list at Map
4. **3rd Party API** - Giving aditional information using Foursquare
5. **Filter** - Easily search the neighborhood list by filter.
6. **RESPONSIVE DESIGN** - Made by using HTML/CSS/JavaScript
7. **UX** - Good User Experience

## The program you need
___

* Browser
* Code editor

This Project includes just front-end development.
Just need browser and code editor to open HTML/CSS/JavaScript

## What this project includes?
___

* css - **Folder filled with CSS file!**
* img - **Image used at Website!**
* js - **Includes knockoutJS & Googlemap.js & neighbor.js**
* index.html - **JUST CLICK THIS QUARK! YOU KNOW WHAT IT IS!**

Now lets activate this project.

## How to run the application?
___
### 1. OPEN index.html!

### 2. Have FUN!

## Detailed explanation about this project
---
##### MVVM (Model / View / ViewModel)

### [Model]

#### locations - EVERYTHING STARTS HERE!
**[list]**
- The first data (every data must be changed here first)

#### markers - Based on locations
**[list]**
- List type, including the google map markers. If something changed at
locations, it need to initial the marker and put at here.

#### mapList - Use place2id indexing to update
**[ko.observableArray]**
- knockout js observableArray type. It includes the locations places.

### [viewModel]

### - Indexing
**place2id / id2marker / id2dom**
The project handle every data with id.
And this indexing file helps to treat the data with id.

when the Model changed, the Indexing file must be changed.
##### (1) place2id - Based on locations
**{object}**
- The first thing to be changed just after the locations(Model) changed.
We can get the the place id.

##### (2) id2marker - Made when initializing markers(Model)
**{object}**
- This is used to get marker object by id.

##### (3) id2dom - Based on neighborhood list DOM
**{object}**
- After the knockout creates the neighborhood list based on mapList(model)
This is used to get neighborhood list by id.

### - State Saving
It is used when we want to check the Action's state

##### (1) selectedDOM - Located at toggleListmenu
**{object}**
- Save information about the selected list menu DOM.
When the Dom is unselected it saves null.

### - State Checking
This is used as boolean. But represent True as 1 & False as 0.
It answers about the state is true or false.

##### (1) click_marker
- Located at toggleListmenu / toggleListmenu(id)
##### (2) click_listmenu
- Located at toggleListmenu / toggleListmenu(id)
##### (3) filter_applied_suscessful
- Located at ViewModel.filter

### - Normal ViewModel
**Used as normal viewmodel**

##### toggleInfoWindow(marker, infowindow)
- The process when we select the marker
##### toggleListmenu(id)
- The process when we select the list menu
##### regExp(text, list)
- Find the corresponding list factor matching the given text

### - 3rd Party API - foursquare
![foursquare](http://78.media.tumblr.com/ffaf0075be879b3ab0b87f0b8bcc6814/tumblr_inline_n965bkOymr1qzxhga.png)
##### Foursquare_api
- With marker and infowindow it returns content for infowindow.
title / image / address / phone number will be returned

##### <Reference>
**https://developer.foursquare.com/docs/api/venues/explore**
- Find venue near selected lat / lng

**https://developer.foursquare.com/docs/api/venues/photos**
- Get picture by venue id

### [View]

##### defaultMapview()
- Show the default settings of map
##### AddListEffect(dom)
- Add purple background to the selected menu DOM
##### DeleteListEffect()
- Delete the purple background from menu DOM

##### hideListMenus()
- Hide all list menus. Process before filtering.
##### hideMarkers()
- Hide all markers. Process before filtering.

##### filtered_listmenu(filtered_id_list)  
- filter the listmenu
##### filtered_Markers(filtered_id_list)
- filter the markers

##### showListMenus()
- Show every list menus
##### showMarkers()
- Show every marker

##### ScrollMove(id)
- Controll the scroll bar at the list

##### addInfoStyle()
- Designing the Infowindow

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
