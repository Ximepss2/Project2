from flask import Flask, render_template, jsonify, request
import pymongo

#Crear conexión con mongo
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

#Nos conectamos con nuestra Base de Datos
db = client.moviesProject_DB

app = Flask(__name__,
            static_url_path='', 
            static_folder='static')

app.config['JSON_AS_ASCII'] = False

@app.route("/")
def home():
        #print(db.list_database_names_())
        movies = list(db.movies.find())
        print(movies)
        return render_template("index.html", movies = movies)

#@app.route("/start")
#def inicio():
 #       start = list(db.start.find())
  #      print(start)
   #     return render_template("home.html", start = start)


#@app.route("/api/oneGenre/<one>")
#def onlyGenres(one):
 #       only = db.moviesProject.distinct({"Genre":one}, {"_id":0, "Genre":1})
  #      only = [only for only in only]
   #     print(only)
    #    return jsonify({
     #           "only": only
      #  })

#API that filters data for genres and give you movies
@app.route("/api/genre/<genres>")
def genre(genres):
        x = db.moviesProject.find({"Genre":genres}, {"_id":0, "Title":1})
        x = [x for x in x]
        print(x)
        return jsonify({
                "data": x
        })

#API that filters data for movies and give all teh information about it.
@app.route("/api/movieDescription/<movi>")
def description(movi):
        data = db.moviesProject.find({"Title":movi}, {"_id":0, "Genre":0})
        data = [data for data in data]
        print(data)
        return jsonify({
                "pelicula": data
        })

if __name__ == "__main__":
        app.run(debug = True)