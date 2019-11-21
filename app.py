from flask import Flask, escape, request, make_response, jsonify
from Graph import *

app = Flask(__name__)

@app.route("/")
def home():
    return str(g.getNumActors())

# http://localhost:5000/actors/all
@app.route("/actors/all", methods=["GET"])
def getAllActors():
    actors = g.getActors()
    return make_response(jsonify({'Actors': actors}), 200)

# http://localhost:5000/movies/all
@app.route("/movies/all", methods=["GET"])
def getAllMovies():
    movies = g.getMovies()
    return make_response(jsonify({'Movies': movies}), 200)

# http://localhost:5000/actors/Danny%20McBride
@app.route("/actors/<actorName>", methods=["GET"])
def getActorByName(actorName):
    actor = g.getActor(actorName)
    if actor != None:
       return make_response(jsonify({'Success': actor}), 200)
    else:
        return make_response(jsonify({'Error': 'No Actor found!'}), 404)


# http://localhost:5000/movies/Die%20Hard%202
@app.route("/movies/<movieName>", methods=["GET"])
def getMovieByName(movieName):
    movie = g.getMovie(movieName)
    if movie != None:
        return make_response(jsonify({'Success': movie}), 200)
    else:
        return make_response(jsonify({'Error': 'No Movie found!'}), 404)

# http://localhost:5000/actors?age=45
@app.route("/actors", methods=["GET"])
def getActorsByFilter():
    name = request.args.get("name", None)
    age = request.args.get("age", None)
    totalGross = request.args.get("total_gross", None)
    actors = g.getActorsByFilter(name, age, totalGross)
    if len(actors) > 0:
        return make_response(jsonify({'Success': actors}), 200)
    else:
        return make_response(jsonify({'Error': 'No Actors found!'}), 404)

# http://localhost:5000/movies?year=2003
@app.route("/movies", methods=["GET"])
def getMoviesByFilter():
    name = request.args.get("name", None)
    wikiPage = request.args.get("wiki_page", None)
    boxOffice = request.args.get("box_office", None)
    year = request.args.get("year", None)
    movies = g.getMoviesByFilter(name, wikiPage, boxOffice, year)
    if len(movies) > 0:
        return make_response(jsonify({'Success': movies}), 200)
    else:
        return make_response(jsonify({'Error': 'No Movies found!'}), 404)


# http://localhost:5000/actors/Danny%20McBride?age=50&total_gross=2323
@app.route("/actors/<actorName>", methods=["PUT"])
def updateActor(actorName):
    totalGross = request.args.get("total_gross", None)
    age = request.args.get("age", None)
    res = g.updateActor(actorName, age, totalGross)
    if res == "Successfully Updated!":
        return make_response(jsonify({'Success': res}), 200)
    else:
        return make_response(jsonify({'Error': res}), 404)

# http://localhost:5000/movies/Die%20Hard%202?year=32323
@app.route("/movies/<movieName>", methods=["PUT"])
def updateMovie(movieName):
    boxOffice = request.args.get("box_office", None)
    year = request.args.get("year", None)
    res = g.updateMovie(movieName, boxOffice, year)
    if res == "Successfully Updated!":
        return make_response(jsonify({'Success': res}), 200)
    else:
        return make_response(jsonify({'Error': res}), 404)

# http://localhost:5000/actors?name=Sanchit Dhiman&total_gross=32323
@app.route("/actors", methods=["POST"])
def createNewActor():
    name = request.args.get("name", None)
    if name == None:
        return make_response(jsonify({'Error': "No Name Provided"}), 400)
    age = request.args.get("age", None)
    totalGross = request.args.get("total_gross", None)
    movies = request.args.get("movies", None)
    res = g.createNewActor(name, age, totalGross, movies)
    if res == "Actor Already Exists":
        return make_response(jsonify({'Error': res}), 404)
    else:
        return make_response(jsonify({'Success': res}), 201)

# http://localhost:5000/movies?name=The Life Of Sanchit Dhiman&box_office=32323&year=2018
@app.route("/movies", methods=["POST"])
def createNewMovie():
    name = request.args.get("name", None)
    if name == None:
        return make_response(jsonify({'Error': "No Name Provided"}), 400)
    wiki_page = request.args.get("wiki_page", None)
    box_office = request.args.get("box_office", None)
    year = request.args.get("year", None)
    actors = request.args.get("actors", None)
    res = g.createNewMovie(name, year, box_office, wiki_page, actors)
    if res == "Movie Already Exists":
        return make_response(jsonify({'Error': res}), 404)
    else:
        return make_response(jsonify({'Success': res}), 201)

# http://localhost:5000/actors/Danny McBride
@app.route("/actors/<actorName>", methods=["DELETE"])
def deleteActorByName(actorName):
    result = g.deleteActorByName(actorName)
    if result == "Actor Deleted!":
        return make_response(jsonify({'Success': result}), 202)
    return make_response(jsonify({'Error': result}), 404)

# http://localhost:5000/movies/Die%20Hard%202
@app.route("/movies/<movieName>", methods=["DELETE"])
def deleteMovieByName(movieName):
    result = g.deleteMovieByName(movieName)
    if result == "Movie Deleted!":
        return make_response(jsonify({'Success': result}), 202)
    return make_response(jsonify({'Error': result}), 404)


if __name__ == "__main__":
    g = Graph("data.json")
    app.run(debug=True)
