"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False #con esto no hace falta el último / de las endpoint
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
#esto es para trabajar en modo desarrollo y poder visualizar lo que estoy haciendo
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "hello": "world",
        "family": members
    }
    return jsonify(response_body), 200

#con los endpoint es lo que le decimos y queremos que  nos muestre
#en este ejemplo "no mostramos datos, solo el mensaje de error o buena respuesta"
@app.route('/member', methods=['POST'])
def add_member():
    #el request.json es la respuesta qeu recibimos de lo que nosotros enviamos al body y le damos
    #esa respuesta un nombre de variable que se llama new_member 
    #request es el objeto que contiene toda la información de la solicitud, y request.json se usa para obtener los datos JSON del cuerpo de la solicitud.

    new_member = request.json 
    member = jackson_family.add_member(new_member)
    if(member):
        #Con jsonify enviamos una respuesta desde el servidor
        #Es una función de Flask que se usa para crear una respuesta HTTP que contiene datos JSON.
        return jsonify({'msg':'adding new member to family'}),200
    return jsonify({'error':'error adding member'}),400


@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = jackson_family.get_member(member_id)
    if (member):
        return jsonify({'msg':'showing member', "member":member}),200
    return jsonify({'error':'error showing member'}),400


@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    member = jackson_family.delete_member(member_id)
    if(member):
        return jsonify({'msg':'removed member'}),200
    return jsonify({'error':'error deleting member'}),400



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
