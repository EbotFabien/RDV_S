from flask import render_template, url_for,flash,redirect,request,abort,Blueprint,jsonify
from app import db,bcrypt
from flask_cors import CORS,cross_origin



db_rubriq = db.collection('rubriq')

rubriq = Blueprint('rubriq',__name__)


@cross_origin(origin=["http://127.0.0.1:5274","http://195.15.228.250","*"],headers=['Content-Type','Authorization'],automatic_options=False)
@rubriq.route('/rubriq/ajouter', methods=['POST'])
def create():
    try:
        id=[doc.to_dict() for doc in db_rubriq.stream()]#[-1]['id']
        id=[int(i['id']) for i in id]
        id.sort()
        id=str(id[-1]+1)
    except:
        id='0'
    if id:
        request.json['id']=str(id)
        request.json['pass']=bcrypt.generate_password_hash(request.json['pass']).decode('utf-8')
        todo = db_rubriq.document(id).get()
        if  todo.to_dict() is None :
            db_rubriq.document(id).set(request.json)
            return jsonify({"success": True}), 200
        else:
            return jsonify({"Fail": "donnee exist deja"}), 400
    else:
        return 400

@cross_origin(origin=["http://127.0.0.1","http://195.15.228.250","*"],headers=['Content-Type','Authorization'])
@rubriq.route('/rubriq/tous', methods=['GET'])
def read():
    all_todos = [doc.to_dict() for doc in db_rubriq.stream()]
    return jsonify(all_todos), 200

@cross_origin(origin=["http://127.0.0.1","http://195.15.228.250","*"],headers=['Content-Type','Authorization'])
@rubriq.route('/rubriq/<int:ide>', methods=['GET'])
def read_ind(ide):


    todo_id = str(ide)
    
    if todo_id:
        todo = db_rubriq.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            return jsonify(todo.to_dict()), 200


@cross_origin(origin=["http://127.0.0.1:5274","http://195.15.228.250","*"],headers=['Content-Type','Authorization'],automatic_options=False)
@rubriq.route('/rubriq/update/<int:ide>', methods=['POST', 'PUT'])
def update(ide):
        todo_id = str(ide)
        todo = db_rubriq.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            db_rubriq.document(todo_id).update(request.json)
            return jsonify({"success": True}), 200
        

@cross_origin(origin=["http://127.0.0.1:5274","http://195.15.228.250","*"],headers=['Content-Type','Authorization'],automatic_options=False)
@rubriq.route('/rubriq/delete/<int:ide>', methods=['GET', 'DELETE'])
def delete(ide):
    todo_id = str(ide)
    todo = db_rubriq.document(todo_id).get()
    if todo.to_dict() is None:
        return jsonify({"Fail": "donnee n'existe pas"}), 400
    else:
        db_rubriq.document(todo_id).delete()
        return jsonify({"success": True}), 200
    