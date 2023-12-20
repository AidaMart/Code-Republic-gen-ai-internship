from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# Let us load data from JSON files
with open("users.json", "r") as users_file:
    users = json.load(users_file)

with open("notes.json", "r") as notes_file:
    notes = json.load(notes_file)

with open("user_notes.json", "r") as user_notes_file:
    user_notes = json.load(user_notes_file)

def find_notes_by_userID(user_id):
    # variables to keep notes ids and notes of the specific user
    user_noteIDs = []
    user_notes_list = []
    for user in user_notes:
        if user['userId'] == user_id:
            user_noteIDs.append(user['noteId'])
    for note in notes:
        if note['id'] in user_noteIDs:
            user_notes_list.append(note)

    if user_notes_list == []: # empty, no notes
        return None
    else:
        return user_notes_list

def find_note_by_id(note_id):
    for note in notes:
        if note['id'] == note_id:
            return note
    return None

# Specific GET method to request only notes of specific user
@app.route('/notes/<int:user_id>', methods=['GET'])
def get_note(user_id):
    notes = find_notes_by_userID(user_id)
    if notes:
        return jsonify({"Here you can find your specified user's note_ids and note_texts": notes}), 200
    else:
        return jsonify("Notes not found"), 404


# General GET method to request all notes of users
@app.route('/notes', methods=['GET'])
def get_all_notes():
    return jsonify({"notes": notes}), 200

# POST method to create new note
@app.route('/notes', methods=['POST'])
def create_note():
    req = request.json
    if 'text' in req:
        new_id = len(notes) + 1
        text = req['text']
        new_note = {"id": new_id, "text": text}
        notes.append(new_note)

        with open("notes.json", 'w') as notes_file:
            json.dump(notes, notes_file)
        return jsonify("New note created successfully"), 201
    else:
        return jsonify("Invalid request data"), 400

# PUT method to update the note
@app.route('/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    note = find_note_by_id(note_id)
    req = request.json
    if note:
        if 'text' in req:
            note['text'] = req['text']
        with open("notes.json", 'w') as notes_file:
            json.dump(notes, notes_file)
        return jsonify("The note's text updated successfully"), 200
    else:
        return jsonify("Invalid or incomplete request"), 400

# DELETE method to delete the note
@app.route('/notes/<int:note_id>', methods = ['DELETE'])
def delete_book(note_id):
    note = find_note_by_id(note_id)
    if note:
        notes.remove(note)
        with open("notes.json", "w") as notes_file:
            json.dump(notes, notes_file)
        return jsonify('The note deleted successfully'), 200
    else:
        return jsonify('Note not found'), 404

if __name__ == '__main__':
    app.run(debug=True)