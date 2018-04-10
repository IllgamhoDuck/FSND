// Make Global variables object id2marker, place2id, id2dom
// Make indexing more comfortable
var id2marker = {};
var place2id = {};
var id2dom = {};

// To check what Dom is selected now
var selectedDOM = { id: null,
                    dom: null };

// State represent did the marker or list menu clicked?
// Used as switch at toggleListmenu & toggleInfoWindow
var click_marker = 0;
var click_listmenu = 0;

// Make a switch representing of did the user ever suscessfully filtered once?
var filter_applied_suscessful = 0;

// Populate place2int object based on locations
for (i = 0; i < locations.length; i++) {
  place2id[locations[i].title] = i;
}

// Knockout JS viewmodel
var viewModel = function() {
  var self = this;

  this.mapList = ko.observableArray([]);

  // Populate the mapList with locations list
  locations.forEach(function(map) {
    var title = map.title;
    var id = 'list' + place2id[map.title];
    var mapobject = {};

    mapobject.title = title;
    mapobject.id = id;

    self.mapList.push(mapobject);
  });

  // Show the clicked list menu
  this.selectListmenu = function(data) {
    var clickedid = place2id[data.title];
    toggleListmenu(clickedid);
  }

  // Filter Function
  this.filter = function() {
    // Check is the text entered in the filter input text field?
    if ($('#filter-text').val() != "") {
      // Checked that the user has suscessfully used filter
      filter_applied_suscessful = 1;

      var filterText = $('#filter-text').val();

      // Check filter text with Regular Expression
      // Make a list to check.
      var checklist = [];
      for (i = 0; i < locations.length; i++) {
        checklist.push(locations[i].title);
      }

      // Make a variable to get the filtered function
      var filtered_id_list;
      filtered_id_list = regExp(filterText, checklist);

      // Hide every list menu and markers
      hideListMenus();
      hideMarkers();

      // Show filtered list and markers
      filtered_listmenu(filtered_id_list);
      filtered_Markers(filtered_id_list);
    } else {
      // If user used filter button with no text in input field.
      // Checked did the user used filter suscessfully before
      if (filter_applied_suscessful === 0) {
        // When user doesn't entered anything in the filter occur error
        alert("Enter the text to use filter!");
      } else {
        filter_applied_suscessful = 0;
        // Show every list menu and markers because the filter has no text
        showListMenus();
        showMarkers();
      }
    }
  }

  // default settings
  this.default_settings = function() {
    // Hide every list menu and markers
    hideListMenus();
    hideMarkers();

    filter_applied_suscessful = 0;
    // Show every list menu and markers
    showListMenus();
    showMarkers();
  }
}

ko.applyBindings(new viewModel());

// Populate id2dom with jquery object.
// To use dom object easily
for (i = 0; i < locations.length; i++) {
  id2dom[i] = $("#list" + i);
}

// Hide and show the sidebar by clicking hamburger icon
// Change the css of both sidebar & google map
// It also hide and show the sidebar by the screen size

var media700 = window.matchMedia("(min-width: 700px)");
var media399 = window.matchMedia("(max-width: 399px)");

// Delete Every class
$("#side-menu").removeClass("side-menu");
$("#side-menu").removeClass("side-menu-hide");
$("#side-menu").removeClass("side-menu-699");
$("#side-menu").removeClass("side-menu-399");
$("#side-menu").removeClass("side-menu-hide-699");
$("#side-menu").removeClass("side-menu-hide-399");

$("#google-map").removeClass("google-map");
$("#google-map").removeClass("google-map-spread");
$("#google-map").removeClass("google-map-699");
$("#google-map").removeClass("google-map-399");
$("#google-map").removeClass("google-map-spread-699");
$("#google-map").removeClass("google-map-spread-399");

if (media700.matches) {
  //Make the class to default
  $("#side-menu").addClass("side-menu");
  $("#google-map").addClass("google-map");

  // Change the class when the hamburger icon is clicked
  $("#ham-img").click(function() {
    $("#side-menu").toggleClass("side-menu");
    $("#side-menu").toggleClass("side-menu-hide");
    $("#google-map").toggleClass("google-map");
    $("#google-map").toggleClass("google-map-spread");

    // Resize google map when we change the size of map
    google.maps.event.trigger(map, 'resize');
  });
} else {
  //Make the class to default
  $("#side-menu").addClass("side-menu-hide-699 side-menu-hide-399");
  $("#google-map").addClass("google-map-spread-699 google-map-spread-399");

  // Change the class when the hamburger icon is clicked
  $("#ham-img").click(function() {
    $("#side-menu").toggleClass("side-menu-699 side-menu-399");
    $("#side-menu").toggleClass("side-menu-hide-699 side-menu-hide-399");
    $("#google-map").toggleClass("google-map-699 google-map-399");
    $("#google-map").toggleClass("google-map-spread-699 google-map-spread-399");

    // Resize google map when we change the size of map
    google.maps.event.trigger(map, 'resize');
  });
}

media700.addListener(function(media700) {
  // Delete Every class
  $("#side-menu").removeClass("side-menu");
  $("#side-menu").removeClass("side-menu-hide");
  $("#side-menu").removeClass("side-menu-699");
  $("#side-menu").removeClass("side-menu-399");
  $("#side-menu").removeClass("side-menu-hide-699");
  $("#side-menu").removeClass("side-menu-hide-399");

  $("#google-map").removeClass("google-map");
  $("#google-map").removeClass("google-map-spread");
  $("#google-map").removeClass("google-map-699");
  $("#google-map").removeClass("google-map-399");
  $("#google-map").removeClass("google-map-spread-699");
  $("#google-map").removeClass("google-map-spread-399");

  // Delete every former event
  $("#ham-img").off('click');

  if (media700.matches) {
    //Make the class to default
    $("#side-menu").addClass("side-menu");
    $("#google-map").addClass("google-map");

    // Change the class when the hamburger icon is clicked
    $("#ham-img").click(function() {
      $("#side-menu").toggleClass("side-menu");
      $("#side-menu").toggleClass("side-menu-hide");
      $("#google-map").toggleClass("google-map");
      $("#google-map").toggleClass("google-map-spread");

      // Resize google map when we change the size of map
      google.maps.event.trigger(map, 'resize');
    });
  } else {
    //Make the class to default
    $("#side-menu").addClass("side-menu-hide-699 side-menu-hide-399");
    $("#google-map").addClass("google-map-spread-699 google-map-spread-399");

    // Change the class when the hamburger icon is clicked
    $("#ham-img").click(function() {
      $("#side-menu").toggleClass("side-menu-699 side-menu-399");
      $("#side-menu").toggleClass("side-menu-hide-699 side-menu-hide-399");
      $("#google-map").toggleClass("google-map-699 google-map-399");
      $("#google-map").toggleClass("google-map-spread-699 google-map-spread-399");

      // Resize google map when we change the size of map
      google.maps.event.trigger(map, 'resize');
    });
  }
});

// toggle list menu when the menu is clicked
function toggleListmenu(id) {
  if (selectedDOM.id != id) {
    DeleteListEffect();
    selectedDOM.id = id;
    selectedDOM.dom = id2dom[id];
    AddListEffect(selectedDOM.dom);
    ScrollMove(id)
  } else {
    selectedDOM.id = null;
    selectedDOM.dom = null;
    DeleteListEffect();
    click_listmenu = 0;
  }

  // Is marker clicked first?
  if (click_marker === 1) {
    // Yes. So we end the loop here.
    click_marker = 0;
  } else {
    // No. listmenu is clicked for the first time.
    click_listmenu = 1;
    // Treat as marker is also clicked
    toggleInfoWindow(id2marker[id], global_infowindow);
  }
}

// Delete every selected-list-menu css at list DOM
function AddListEffect(dom) {
  dom.addClass('selected-list-menu');
}

// Delete every selected-list-menu css at list DOM
function DeleteListEffect() {
  $('#neighbor-list').children().removeClass('selected-list-menu');
}

// Hide every list menu
function hideListMenus() {
  $('#neighbor-list').children().hide();
}

// Show every list menu
function showListMenus() {
  $('#neighbor-list').children().show();
}

// Regular Expression.
// returns the list of id that is correspond to the condition.
// text = 'a' list = ['a', 'b' 'asdf']
function regExp(text, list) {
  var text = new RegExp(text, "i");
  var correspond_id = [];
  for (i = 0; i < list.length; i++) {
    var result = text.test(list[i]);
    if (result == true) {
      correspond_id.push(place2id[list[i]]);
    }
  }
  return correspond_id;
}

// Show filtered listmenu
function filtered_listmenu(filter) {
  for (var i = 0; i < markers.length; i++) {
    if ( filter.indexOf(i) != -1 ){
      id2dom[i].show();
    }
  }
}

// list menu scroll auto controller
function ScrollMove(id) {
  if (media399.matches) {
    var position = id2dom[id].position();
    $('#neighbor-list').animate({ scrollTop: position.top - 115 }, 300);
  } else {
    var position = id2dom[id].position();
    $('#neighbor-list').animate({ scrollTop: position.top - 255 }, 300);
  }
}
