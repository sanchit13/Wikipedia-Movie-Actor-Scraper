from Graph import *

g = Graph("json.txt")
g.saveToJson()

while True:
    print("Press 1 to input a Movie and see how much it grossed")
    print("Press 2 to input an Actor and see which movies they worked on")
    print("Press 3 to input a Movie and see which actors starred in it")
    print("Press 4 to view top 10 actors with the most total grossing value")
    print("Press 5 to see top 10 oldest actors")
    print("Press 6 to input a year and see movies for a given year")
    print("Press 7 to input a year and see actors for a given year")
    val = int(input("Enter your Choice: "))

    if val == 1:
        movieName = input("Enter Movie Name: ")
        print(g.getMovieGross(movieName))

    elif val == 2:
        actorName = input("Enter Actor Name: ")
        print(g.getMoviesForActor(actorName))

    elif val == 3:
        movieName = input("Enter Movie Name: ")
        print(g.getActorsInMovie(movieName))

    elif val == 4:
        print(g.getHighestWeightedActors())

    elif val == 5:
        print(g.getOldestActors())

    elif val == 6:
        year = input("Enter Year: ")
        print(g.getMoviesFromYear(year))

    elif val == 7:
        year = input("Enter Year: ")
        print(g.getActorsFromYear(year))
