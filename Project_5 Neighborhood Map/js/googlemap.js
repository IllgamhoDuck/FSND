// Google map api
var map;
var global_infowindow;
var locations = [
  {title: 'sangheo Memorial Library', location: {lat: 37.542012, lng: 127.073822}},
  {title: 'Comprehensive Lecture room', location: {lat: 37.541595, lng: 127.075044}},
  {title: 'International bachelor\'s degree', location: {lat: 37.539734, lng: 127.077294}},
  {title: 'Life hall', location: {lat: 37.538999, lng: 127.077308}},
  {title: 'Science Hall', location: {lat: 37.541484, lng: 127.080433}},
  {title: 'Post Office', location: {lat: 37.54179, lng: 127.078016}},
  {title: 'Duck\'s Paradise', location: {lat: 37.541972, lng: 127.076728}},
  {title: 'Engineering Building', location: {lat: 37.541595, lng: 127.078905}},
  {title: 'Reserve Officers Training Corps', location: {lat: 37.542178, lng: 127.072711}},
  {title: 'Konkuk Univ Station', location: {lat: 37.540781, lng: 127.07105}},
  {title: 'Ducky home', location: {lat: 32.731841, lng: 139.614258}},
  {title: 'Top Right', location: {lat: 45.58329, lng: 141.152344}},
  {title: 'Bottom Left', location: {lat: 31.44741, lng: 117.13623}},
  {title: 'Top Left', location: {lat: 43.357138, lng: 117.905273}},
];
var markers = [];

function initMap() {

  var styles = [
    {
        "featureType": "all",
        "elementType": "labels.text.fill",
        "stylers": [
            {
                "saturation": 36
            },
            {
                "color": "#000000"
            },
            {
                "lightness": 40
            }
        ]
    },
    {
        "featureType": "all",
        "elementType": "labels.text.stroke",
        "stylers": [
            {
                "visibility": "on"
            },
            {
                "color": "#000000"
            },
            {
                "lightness": 16
            }
        ]
    },
    {
        "featureType": "all",
        "elementType": "labels.icon",
        "stylers": [
            {
                "visibility": "off"
            }
        ]
    },
    {
        "featureType": "administrative",
        "elementType": "geometry.fill",
        "stylers": [
            {
                "color": "#000000"
            },
            {
                "lightness": 20
            }
        ]
    },
    {
        "featureType": "administrative",
        "elementType": "geometry.stroke",
        "stylers": [
            {
                "color": "#000000"
            },
            {
                "lightness": 17
            },
            {
                "weight": 1.2
            }
        ]
    },
    {
        "featureType": "landscape",
        "elementType": "geometry",
        "stylers": [
            {
                "color": "#000000"
            },
            {
                "lightness": 20
            }
        ]
    },
    {
        "featureType": "poi",
        "elementType": "geometry",
        "stylers": [
            {
                "color": "#000000"
            },
            {
                "lightness": 21
            }
        ]
    },
    {
        "featureType": "road.highway",
        "elementType": "geometry.fill",
        "stylers": [
            {
                "color": "#000000"
            },
            {
                "lightness": 17
            }
        ]
    },
    {
        "featureType": "road.highway",
        "elementType": "geometry.stroke",
        "stylers": [
            {
                "color": "#000000"
            },
            {
                "lightness": 29
            },
            {
                "weight": 0.2
            }
        ]
    },
    {
        "featureType": "road.arterial",
        "elementType": "geometry",
        "stylers": [
            {
                "color": "#000000"
            },
            {
                "lightness": 18
            }
        ]
    },
    {
        "featureType": "road.local",
        "elementType": "geometry",
        "stylers": [
            {
                "color": "#000000"
            },
            {
                "lightness": 16
            }
        ]
    },
    {
        "featureType": "transit",
        "elementType": "geometry",
        "stylers": [
            {
                "color": "#000000"
            },
            {
                "lightness": 19
            }
        ]
    },
    {
        "featureType": "water",
        "elementType": "geometry",
        "stylers": [
            {
                "color": "#ffffff"
            },
            {
                "lightness": 17
            }
        ]
    }
  ];

  map = new google.maps.Map(document.getElementById('google-map'), {
    center: {lat: 37.540911, lng: 127.076315},
    zoom: 17,
    styles: styles,
    mapTypecontrol: false
  });

  // Default map information

  var bounds = new google.maps.LatLngBounds();
  var Infowindow = new google.maps.InfoWindow();
  global_infowindow = Infowindow;

  // Add infowindow dom an id to apply CSS when we click the marker
  addInfoStyle();

  // Style the markers a bit. This will be our listing marker icon.
  var defaultIcon = makeMarkerIcon('ffffff');

  // Create a "highlighted location" marker color for when the user
  // mouses over the marker.
  var highlightedIcon = makeMarkerIcon('6F62EC');

  //Create the default markers
  for (var i = 0; i < locations.length; i++) {

    var title = locations[i].title;
    var position = locations[i].location;

    var marker = new google.maps.Marker({
      map: map,
      title: title,
      position: position,
      icon: defaultIcon,
      animation: google.maps.Animation.DROP,
      id: i
    });

    marker.addListener('click', function() {
      toggleInfoWindow(this, Infowindow);
    });

    // Two event listeners - one for mouseover, one for mouseout,
    // to change the colors back and forth.
    marker.addListener('mouseover', function() {
      this.setIcon(highlightedIcon);
    });
    marker.addListener('mouseout', function() {
      this.setIcon(defaultIcon);
    });

    // int2marker
    id2marker[i] = marker;

    markers.push(marker);
    bounds.extend(markers[i].position)
  }
  map.fitBounds(bounds);
}


// toggle infowindow when the marker is clicked
function toggleInfoWindow(marker, infowindow) {
  var togglebounds = new google.maps.LatLngBounds();

  if (infowindow.marker != marker) {

    StopAllAnimation();
    BounceStart(marker);

    // Use forsquare api to make the infowindow
    foursquare_api(marker, infowindow);

    togglebounds.extend(marker.position);
    map.fitBounds(togglebounds);
    map.setZoom(16);

    infowindow.addListener('closeclick', function() {
      StopAllAnimation()
      infowindow.marker = null;

      // Delete all effect on listmenu side too
      selectedDOM.id = null;
      selectedDOM.dom = null;
      DeleteListEffect();
      click_marker = 0;
      // Go back to default map view
      defaultMapview();
    });
  } else {
    StopAllAnimation()
    infowindow.marker = null;
    infowindow.close();
    click_marker = 0;
    // Go back to default map view
    defaultMapview();
  }

  // Is listmenu clicked first?
  if (click_listmenu === 1) {
    // Yes. So we end the loop here.
    click_listmenu = 0;
  } else {
    // No. Marker is clicked for the first time.
    click_marker = 1;
    // Treat as listmenu is also clicked
    toggleListmenu(marker.id);
  }
}

// Make the marker bounce when it is clicked.
function BounceStart(marker) {
    marker.setAnimation(google.maps.Animation.BOUNCE);
}

// Delete all markers animation
function StopAllAnimation() {
  markers.forEach(function(marker) {
    marker.setAnimation(null);
  });
}

// Hide all markers
function hideMarkers() {
  for (var i = 0; i < markers.length; i++) {
    markers[i].setMap(null);
  }
}

// Show all markers
function showMarkers() {
  var bounds = new google.maps.LatLngBounds();
  // Extend the boundaries of the map for each marker and display the marker
  for (var i = 0; i < markers.length; i++) {
    markers[i].setMap(map);
    bounds.extend(markers[i].position);
  }
  map.fitBounds(bounds);
}

// Filtered markers
function filtered_Markers(filter) {
  for (var i = 0; i < markers.length; i++) {
    if ( filter.indexOf(i) != -1  ){
      markers[i].setMap(map);
    }
  }
}

// Return the map view to default
function defaultMapview() {
  var bounds = new google.maps.LatLngBounds();
  // Extend the boundaries of the map for each marker and display the marker
  for (var i = 0; i < markers.length; i++) {
    bounds.extend(markers[i].position);
  }
  map.fitBounds(bounds);
}

// This function takes in a COLOR, and then creates a new marker
// icon of that color. The icon will be 21 px wide by 34 high, have an origin
// of 0, 0 and be anchored at 10, 34).
function makeMarkerIcon(markerColor) {
  var markerImage = new google.maps.MarkerImage(
    'http://chart.googleapis.com/chart?chst=d_map_spin&chld=1.15|0|'+ markerColor +
    '|40|_|%E2%80%A2',
    new google.maps.Size(21, 34),
    new google.maps.Point(0, 0),
    new google.maps.Point(10, 34),
    new google.maps.Size(21,34));
  return markerImage;
}


// Get information from 3rd Party Api - Foursquare
// We will get the nearby places information
// place title / image / address / phone number
function foursquare_api(marker, infowindow) {

  // Content of infowindow
  var prefix = '<div id="infowindow-container"><div id="infowindow-list">';
  var suffix = '</div><div id="infowindow-explain">' +
               'NEARBY PLACE FROM' + '</div><div id="infowindow-title">' +
                marker.title + '</div></div>';

  // Foursquare client_id & client_secret
  var client_id = 'SQYRLLQMR5EGIUNYMRXD0GCG5UO0HZOGAD4QUW02CSS0RGBX';
  var client_secret = 'ASBIBJ0LWEKOQBLO1GKT11YPEOSQYECVD4CUDDUHLRGR4RV2';

  // Get latitude, longitude value
  var lat = locations[place2id[marker.title]].location.lat.toFixed(2);
  var lng = locations[place2id[marker.title]].location.lng.toFixed(2);

  // Search nearby venue in 3km. Result will limit to 15.
  var foursquareUrl = 'https://api.foursquare.com/v2/venues/search?ll=' +
                    lat + ',' + lng + '&radius=3000' + '&limit=15' +
                    '&client_id=' + client_id +
                    '&client_secret=' + client_secret + '&v=20171001';

  // Send Ajax request to foursquare Api server
  $.ajax({
    url: foursquareUrl,
    dataType: "jsonp",
    success: function(response) {
      if (response.meta.code == 200) {
        // The info window where the detailed information will be populated
        var innerHTML = "";

        // Get place information
        var venues = response.response.venues;

        // If there is no place near, break the loop
        if (venues.length == 0) {
          var innerHTML = "<div class='infowindow-venue-image'>" +
                          '<img class="foursquare-img" src="img/default.png">' +
                          "<div class='duck-talking'>No Place Near QUARK!!!</div></div>"
          infowindow.marker = marker;
          infowindow.setContent(prefix + innerHTML + suffix);
          infowindow.open(map, marker);
        } else {
          venues.forEach(function(venue) {
          innerHTML += getPlaceDetailes(venue);
        })
          infowindow.marker = marker;
          infowindow.setContent(prefix + innerHTML + suffix);
          infowindow.open(map, marker);
        };
      } else {
        var innerHTML = "<div class='infowindow-venue-image'>" +
                        '<img class="foursquare-img" src="img/default.png">' +
                        "<div class='duck-talking'>Failed to get response QUARK!!</div></div>"
        infowindow.marker = marker;
        infowindow.setContent(prefix + innerHTML + suffix);
        infowindow.open(map, marker);
      }
    }}).fail(function() {
      var innerHTML = "<div class='infowindow-venue-image'>" +
                      '<img class="foursquare-img" src="img/default.png">' +
                      "<div class='duck-talking'>Failed to get response QUARK!!!</div></div>";
      infowindow.marker = marker;
      infowindow.setContent(prefix + innerHTML + suffix);
      infowindow.open(map, marker);
    });
}

// Get detailed information at the place
function getPlaceDetailes(venue) {
  var innerHTML = "<div class='infowindow-list-menu'>";
  if (venue.name) {
    innerHTML += "<div class='infowindow-venue-name'>" +
                 venue.name + "</div>";
  }
  if (venue.id) {
    var venue_id = venue.id;
    innerHTML += getPlaceImage(venue_id);
  }
  if (venue.location.address){
    innerHTML += "<div class='infowindow-venue-address'>" +
                 venue.location.address + "</div>";
  }
  if (venue.contact.formattedPhone){
    innerHTML += "<div class='infowindow-venue-phone'>" +
                 venue.contact.formattedPhone + "</div>";
  }
  innerHTML += "</div>";

  return innerHTML;
}

// Get picture from foursquare by venue_id
function getPlaceImage(venue_id) {
  // Foursquare client_id & client_secret
  var client_id = 'SQYRLLQMR5EGIUNYMRXD0GCG5UO0HZOGAD4QUW02CSS0RGBX';
  var client_secret = 'ASBIBJ0LWEKOQBLO1GKT11YPEOSQYECVD4CUDDUHLRGR4RV2';

  // Use foursquare api - Get a Venue's Photos
  var foursquareUrl = 'https://api.foursquare.com/v2/venues/' +
                    venue_id + '/photos?' + '&v=20171001' +
                    '&client_id=' + client_id +
                    '&client_secret=' + client_secret;

  var innerHTML;

  // Send Ajax request. Set async false because this is in for loop.
  $.ajax({
    url: foursquareUrl,
    dataType: "json",
    async: false,
    success: function(response) {
      if (response.meta.code == 200) {
        //Get the first picture
        var image = response.response.photos.items[0];

        // If there is no picture return default pic.. QUARK!!!
        if (image == null) {
          innerHTML = "<div class='infowindow-venue-image'>" +
                      '<img class="foursquare-img" src="img/default.png">' +
                      "<div class='duck-talking'>No Image QUARK!!!</div></div>";
        } else {
          // Get the imgURL
          var prefix = image.prefix;
          var suffix = image.suffix;
          var imgURL = prefix + "300x300" + suffix;

          innerHTML = "<div class='infowindow-venue-image'>" +
                      '<img class="foursquare-img" src="' + imgURL + '">' +
                      "</div>";
        }
      } else {
        innerHTML = "<div class='infowindow-venue-image'>" +
                    '<img class="foursquare-img" src="img/default.png">' +
                    "<div class='duck-talking'>Failed to get response QUARK!!!</div></div>"
      }
    }}).fail(function() {
      innerHTML = "<div class='infowindow-venue-image'>" +
                  '<img class="foursquare-img" src="img/default.png">' +
                  "<div class='duck-talking'>Failed to get response QUARK!!!</div></div>"
    })

  return innerHTML;
}

// Add id to infowindow DOM for Google map styling with CSS
function addInfoStyle() {
  google.maps.event.addListener(global_infowindow, 'domready', function() {
    // The DOM that includes all style about infowindow
    var info_style_standard = $('.gm-style-iw').prev();

    // Infowindow shadow DOM
    var info_style_shadow = info_style_standard.children(':nth-child(2)');
    info_style_shadow.attr('id', 'info-hide');

    // Infowindow background color DOM
    var info_style_background = info_style_standard.children(':nth-child(4)');
    info_style_background.attr('id', 'info-color');

    // Infowindow cursor DOM
    var info_style_cursor = info_style_standard.children(':nth-child(3)');
    var info_style_cursor_left = info_style_cursor.children(':nth-child(1)').children(':nth-child(1)');
    var info_style_cursor_right = info_style_cursor.children(':nth-child(2)').children(':nth-child(1)');
    info_style_cursor_left.attr('class', 'info-cursor');
    info_style_cursor_right.attr('class', 'info-cursor');

    // Controlling the position of infowindow Content
    var infowindow_content_position = $('.gm-style-iw');
    infowindow_content_position.attr('id', 'info-content-position');

  });
}
