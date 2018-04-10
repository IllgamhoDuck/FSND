import media
import fresh_tomatoes


# Making instance(object) about Movie you like!
# Need to write 3 informations.
# "title","poster_image_url","trailer_youtube_url"

designated_survivor = media.Movie("Designated Survivor",
                                  "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRCFqueE694TEPiY2v5TRtZlCHA9kWG4PRhAG4ccEYcPLnzWQc8Ug",  # noqa
                                  "https://www.youtube.com/watch?v=N_f1v0Nx5Sw"
                                  )

cloudatlas = media.Movie("Cloud Atlas",
                         "https://upload.wikimedia.org/wikipedia/en/2/20/Cloud_Atlas_Poster.jpg",  # noqa
                         "https://www.youtube.com/watch?v=ByehYal_cCs"
                         )

starwars = media.Movie("Starwars:The Last Jedi",
                       "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/Star_Wars_Logo.svg/375px-Star_Wars_Logo.svg.png",  # noqa
                       "https://www.youtube.com/watch?v=zB4I68XVPzQ")

bicentannial_man = media.Movie("Bicentannial Man",
                               "http://image.cine21.com/IMGDB/poster/2004/0902/large/162542_bicen.jpg",  # noqa
                               "https://www.youtube.com/watch?v=B320zb2H8eY&t=41s")  # noqa

interstella = media.Movie("Interstella",
                          "https://upload.wikimedia.org/wikipedia/en/b/bc/Interstellar_film_poster.jpg",  # noqa
                          "https://www.youtube.com/watch?v=hRhyJPmfoNg")

matrix = media.Movie("Matrix",
                     "http://ticketimage.interpark.com/Movie/still_image/V16/V1601447p_s01.gif",  # noqa
                     "https://www.youtube.com/watch?v=vKQi3bBA1y8")


# merge your instance(object) of movie by array to apply on fresh_tomatoe.py
movies = [cloudatlas,
          starwars,
          designated_survivor,
          bicentannial_man,
          interstella,
          matrix]

# You can choose your HTML page name!
choose_html_title = "Ducky movies"

# put 2 information. (instance(object) of movie information you merged by array, html_title you choosed)  # noqa
fresh_tomatoes.open_movies_page(movies, choose_html_title)
