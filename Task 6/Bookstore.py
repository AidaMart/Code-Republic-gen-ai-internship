# Here you can find Bookstore application code

from flask import Flask, request, jsonify

app = Flask(__name__)

books = []

def find_book_by_id(book_id):
    for book in books:
        if book['id'] == book_id:
            return book
    return None

@app.route('/api/books/<int:book_id>', methods = ['GET'])
def get_book(book_id):
    book = find_book_by_id(book_id)
    if book:
        return jsonify(book), 200
    else:
        return jsonify("Book not found"), 404


@app.route('/api/books', methods=['GET'])
def get_all_books():
    return jsonify(books), 200

@app.route('/api/books', methods=['POST'])
def create_book():
    req = request.json
    if 'title' in req and 'author' in req and 'price' in req:
        new_id = len(books) + 1
        title = req['title']
        author = req['author']
        price = req['price']
        new_book = {"id": new_id, "title": title, "author": author, "price": price}
        books.append(new_book)
        return jsonify("New book created successfully"), 201
    else:
        return jsonify("Invalid request data"), 400

@app.route('/api/books/<int:book_id>', methods=['PATCH'])
def update_book(book_id):
    book = find_book_by_id(book_id)
    req = request.json
    if book:
        if 'title' in req:
            book['title'] = req['title']
        if 'author' in req:
            book['author'] = req['author']
        if 'price' in req:
            book['price'] = req['price']
        return jsonify("The book updated successfully"), 200
    else:
        return jsonify("Invalid or incomplete request"), 400

@app.route('/api/books/<int:book_id>', methods = ['DELETE'])
def delete_book(book_id):
    book = find_book_by_id(book_id)
    if book:
        books.remove(book)
        return jsonify('The book deleted successfully'), 200
    else:
        return jsonify('Book not found'), 404


if __name__ == '__main__':
    app.run(debug = True)





