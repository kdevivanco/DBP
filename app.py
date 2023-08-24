from flask import Flask, render_template, request,redirect,jsonify
from flask import Flask, render_template, request,redirect,jsonify
import pdb

app = Flask(__name__)

animes = [
    {'id': 1,
    'stats':{
        'title':'titulo',
        'poster':'poster_prueba',
        'categoria':'cat',
        'rating':1.00,
        'descripcion':'desc',
    }
    }
]

class Anime:
    def __init__(self, title, category, img):
        self.title = title
        self.category = category
        self.img = img

@app.route('/animes')
def all_animes():
    return jsonify(animes)

@app.route("/animes/<int:id>")
def mostrar_anime(id):
    p = animes[0]
    return jsonify(p)

@app.route('/animes', methods=['POST'])
def create_anime():
    new_anime = {
        'id': animes[-1]['id'] + 1,
        'stats':{
            'title':request.json['title'],
            'poster':request.json['poster'],
            'categoria':request.json['categoria'],
            'rating':request.json['rating'],
            'descripcion':request.json['descripcion'],
        }
    }
    animes.append(new_anime)
    return jsonify(new_anime)


#PUT
@app.route('/animes/<int:id>', methods=['POST'])
def edit_anime(id):
    animes[id-1]['stats']['title'] = request.json['title']
    animes[id-1]['stats']['poster'] = request.json['poster']
    animes[id-1]['stats']['categoria'] = request.json['categoria']
    animes[id-1]['stats']['rating'] = request.json['rating']
    animes[id-1]['stats']['descripcion'] = request.json['descripcion']
    return jsonify(animes[id-1])

#DELETE
@app.route('/animes/<int:id>', methods=['DELETE']) 
def delete_anime(id):
    animes.pop(id-1)
    return jsonify({'message': 'El anime ha sido eliminado'})



#if name = main
if __name__ == "__main__":
    app.run(debug=True)