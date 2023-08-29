from flask import Flask, render_template, request, jsonify
# from models import Anime
from serializers import AnimeModel
# from db imporxt db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pdb

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost/dbp'

db = SQLAlchemy(app)  # Initialize SQLAlchemy

class Anime(db.Model):
    __tablename__ = 'anime'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    poster = db.Column(db.String(255))
    categoria = db.Column(db.String(255))
    rating = db.Column(db.Numeric(4, 2))
    descripcion = db.Column(db.Text)


@app.route('/animes')
def all_animes():
    animes = Anime.query.all()
    all = []
    for anime in animes:
        print(anime.title)
        anime_model = AnimeModel(**anime.__dict__)
        anime_data = anime_model.dict()
        all.append(anime_data)

    return all

@app.route("/animes/<int:id>")
def mostrar_anime(id):
    anime = Anime.query.filter_by(id=id).first()
    if anime:
        anime_model = AnimeModel(**anime.__dict__)
        anime_data = anime_model.dict()
        return jsonify(anime_data)
    else:
        return jsonify({'error': 'Anime not found'}), 404

@app.route('/animes/create')
def show_create():
    return render_template('anime_create.html')

@app.route("/animes", methods=['POST'])
def create_anime():
    data = request.json
    pdb.set_trace()
    anime_create_model = AnimeModel(**data)
    anime = Anime(**anime_create_model.dict())
    db.session.add(anime)
    db.session.commit()
    return jsonify({'message': 'Anime created successfully'}), 201

@app.route("/animes/<int:id>", methods=['PUT'])
def update_anime(id):
    data = request.json
    anime = Anime.query.get(id)
    pdb.set_trace()
    if anime:
        anime_update_model = AnimeModel(**data)
        for key, value in anime_update_model.dict().items():
            setattr(anime, key, value)
        db.session.commit()
        return jsonify({'message': 'Anime updated successfully'}), 200
    else:
        return jsonify({'error': 'Anime not found'}), 404


@app.route("/animes/<int:id>", methods=['DELETE'])
def delete_anime(id):
    anime = Anime.query.get(id)

    if anime:
        db.session.delete(anime)
        db.session.commit()
        return jsonify({'message': 'Anime deleted successfully'}), 200
    else:
        return jsonify({'error': 'Anime not found'}), 404
    


# @app.route('/animes', methods=['POST'])
# def create_anime():
#     new_anime = {
#         'id':len(animes) +1,
#         'title':request.json['title'],
#         'poster':request.json['poster'],
#         'categoria':request.json['categoria'],
#         'rating':request.json['rating'],
#         'descripcion':request.json['descripcion'],
#     }
#     animes.append(new_anime)
#     return jsonify(new_anime)


# #PUT
# @app.route('/animes/<int:id>', methods=['PUT'])
# def edit_anime(id):
#     for i , a in enumerate (animes): #usar un for no es optimo, si se usa bdd se llamaria un filter usando el id para obtener el objeto
#         if a['id'] == id:
#             animes[i] = {
#                 'id':id,
#                 'title':request.json['title'],
#                 'poster':request.json['poster'],
#                 'categoria':request.json['categoria'],
#                 'rating':request.json['rating'],
#                 'descripcion':request.json['descripcion'],
#             }
#             return jsonify(animes[i])  
#         else: 
#             return jsonify({'message':'error'})

# #DELETE
# @app.route('/animes/<int:id>', methods=['DELETE']) 
# def delete_anime(id):
#     animes.pop(id-1)
#     if len(animes) == 0:  #Esto es un ejemplo reduccionista porque la lista solo tiene un elemento
#         return jsonify({'message': 'El anime ha sido eliminado'})
#     else:
#         return jsonify({'message':'error'})


#if name = main
if __name__ == "__main__":
    app.run(debug=True)