from flask import render_template, url_for,flash,redirect,request,abort,Blueprint,jsonify
from app import db,bcrypt
from flask_cors import CORS,cross_origin

db_cles = db.collection('cles')
db_client = db.collection('client')
db_compteur = db.collection('compteur')
db_extenssion= db.collection('extenssion')
db_piece= db.collection('piece')
db_rubriq= db.collection('rubriq')
db_user= db.collection('user')
db_voie= db.collection('voie')
db_logement= db.collection('logement') 
db_rdv= db.collection('rdv')







rdv =Blueprint('rdv',__name__)

@cross_origin(origin=["http://127.0.0.1:5274","http://195.15.228.250","*"],headers=['Content-Type','Authorization'],automatic_options=False)
@rdv.route('/rdv/ajouter', methods=['POST'])
def create():
    try:
        id=[doc.to_dict() for doc in db_logement.stream()]#[-1]['id']
        id=[int(i['id']) for i in id]
        id.sort()
        id=str(id[-1]+1)
    except:
        id='0'
    if id:
        request.json['id']=str(id)
        request.json['pass']=bcrypt.generate_password_hash(request.json['pass']).decode('utf-8')
        todo = db_rdv.document(id).get()
        if  todo.to_dict() is None :
            db_rdv.document(id).set(request.json)
            all_=db_rdv.document(id).get()
            return jsonify(all_.to_dict()), 200
        else:
            return jsonify({"Fail": "donnee exist deja"}), 400
    else:
        return 400

@cross_origin(origin=["http://127.0.0.1","http://195.15.228.250","*"],headers=['Content- Type','Authorization'])
@rdv.route('/rdv/tous', methods=['GET'])
def read():
    all_todos = [doc.to_dict() for doc in db_rdv.stream()]
    return jsonify(all_todos), 200

@cross_origin(origin=["http://127.0.0.1","http://195.15.228.250","*"],headers=['Content- Type','Authorization'])
@rdv.route('/rdv/tous', methods=['GET'])
def read_all():
    all_rdv = [doc.to_dict() for doc in db_rdv.stream()]
    all_logement = [doc.to_dict() for doc in db_logement.stream()]
    all_cles = [doc.to_dict() for doc in db_cles.stream()]
    all_client = [doc.to_dict() for doc in db_client.stream()]
    all_compteur = [doc.to_dict() for doc in db_compteur.stream()]
    all_extension = [doc.to_dict() for doc in db_extenssion.stream()]
    all_rubriq = [doc.to_dict() for doc in db_rubriq.stream()]
    all_piece = [doc.to_dict() for doc in db_piece.stream()]
    all_user = [doc.to_dict() for doc in db_user.stream()]
    all_voie = [doc.to_dict() for doc in db_voie.stream()]
     
     
     
     
    return jsonify({"rdv":all_rdv,
        "logement": all_logement,
        "cles": all_cles,
        "client": all_client,
        "compteur": all_compteur,
        "extenssion" : all_extension,
        "rubriq" : all_rubriq,
        "piece" : all_piece,
        "user" : all_user,
        "voie" : all_voie
        }), 200
    

@cross_origin(origin=["http://127.0.0.1","http://195.15.228.250","*"],headers=['Content- Type','Authorization'])
@rdv.route('/rdv/<string:ide>', methods=['GET'])#hide data
def read_ind(ide):
    todo_id = str(ide)
    
    if todo_id:
        todo = db_rdv.where('email','==',todo_id)
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            return jsonify(todo.to_dict()), 200

@cross_origin(origin=["http://127.0.0.1:5274","http://195.15.228.250","*"],headers=['Content-Type','Authorization'],automatic_options=False)
@rdv.route('/rdv/update/<int:ide>', methods=['POST', 'PUT'])
def update(ide):
        todo_id = str(ide)
        todo = db_rdv.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            db_rdv.document(todo_id).update(request.json)
            return jsonify({"success": True}), 200

@cross_origin(origin=["http://127.0.0.1:5274","http://195.15.228.250","*"],headers=['Content-Type','Authorization'],automatic_options=False)
@rdv.route('/rdv/delete/<int:ide>', methods=['GET', 'DELETE'])
def delete(ide):
    todo_id = str(ide)
    todo = db_rdv.document(todo_id).get()
    if todo.to_dict() is None:
        return jsonify({"Fail": "donnee n'exist pas"}), 400
    else:
        db_rdv.document(todo_id).delete()
        return jsonify({"success": True}), 200