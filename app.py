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
    anime_create_model = AnimeModel(**data)
    anime = Anime(**anime_create_model.dict())
    db.session.add(anime)
    db.session.commit()
    return jsonify({'message': 'Anime created successfully'}), 201

@app.route("/animes/<int:id>", methods=['PUT'])
def update_anime(id):
    data = request.json
    anime = Anime.query.get(id)
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
    
@app.route("/animes/<int:id>", methods=['PATCH'])
def partial_update_anime(id):
    data = request.json
    anime = Anime.query.get(id)

    if anime:
        anime_update_model = AnimeModel(**anime.__dict__)  # Initialize with existing data
        for key, value in data.items():
            if hasattr(anime_update_model, key):
                setattr(anime_update_model, key, value)
        for key, value in anime_update_model.dict().items():
            setattr(anime, key, value)
        db.session.commit()
        return jsonify({'message': 'Anime updated successfully'}), 200
    else:
        return jsonify({'error': 'Anime not found'}), 404
    

#if name = main
if __name__ == "__main__":
    app.run(debug=True)