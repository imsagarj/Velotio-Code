from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/noteapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Note(db.Model):
    title = db.Column(db.Text, primary_key=True)
    name = db.Column(db.Text)


@app.route('/ping', methods=['GET'])
def home():
    return 'Service up and running'


@app.route('/create_or_update_note', methods=['POST', 'PUT'])
def create_or_update_note():
    """
        This method is used to store note.
    """
    try:
        if request.method == 'POST':
            req_body = request.get_json()
            note_obj = Note()
            note_obj.title = req_body.get('title', '')
            note_obj.name = req_body.get('name', '')
            db.session.add(note_obj)
            db.session.commit()
            return 'Note record created'
        elif request.method == 'PUT':
            req_body = request.get_json()
            is_note = Note.query.filter_by(title=req_body.get('title')).first()
            if is_note:
                is_note.name = req_body.get('name', '')
                db.session.commit()
            return "Note Successfully Updated."
        return "Method not allowed."
    except Exception as ex:
        raise ex


@app.route('/get_all_notes', methods=['GET'])
def get_all_records():
    """
        This method is used to get all notes.
    """
    try:
        if request.method == 'GET':
            notes = Note.query.all()
            note_records = []
            for note in notes:
                if '_sa_instance_state' in note.__dict__:
                    del note.__dict__['_sa_instance_state']
                note_records.append(note.__dict__)
            return {"data": note_records}
        return "Method not found. Please try again."
    except Exception as ex:
        raise ex


@app.route('/delete_note', methods=['DELETE'])
def delete_note():
    """
        This method use for delete the note
    """
    try:
        if request.method == 'DELETE':
            req_body = request.get_json()
            is_note = Note.query.filter_by(title=req_body.get('title')).first()
            if is_note:
                db.session.delete(is_note)
                db.session.commit()
                return "Note Successfully Deleted."
            return "Note not found."
        return "Method not found."
    except Exception as ex:
        raise ex


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
