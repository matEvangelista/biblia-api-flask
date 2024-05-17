from flask import Flask, jsonify, abort
import json

app = Flask(__name__)

file = open("biblia-catolica.json")
bible = json.load(file)


@app.route("/<book>/<int:chapter>/<int:verse>")
def get_verse(book, chapter, verse):
    chapter_data = []
    try:
        chapter_data = next(boo for boo in bible if boo['livro'] == book and boo['capitulo'] == chapter)
    except StopIteration:
        abort(404, description="Book or chapter not found")

    if verse <= 0 or verse > len(chapter_data['versiculos']):
        abort(404, description="Verse not found")

    verse_text = chapter_data['versiculos'][verse - 1]

    response = {
        'book': book,
        'chapter': chapter,
        'verse': verse,
        'data': verse_text
    }
    return jsonify(response), 200


@app.route("/<book>/<int:chapter>/<int:v1>-<int:v2>")
def get_verses(book, chapter, v1, v2):
    chapter_data = []
    try:
        chapter_data = next(boo for boo in bible if boo['livro'] == book and boo['capitulo'] == chapter)
    except StopIteration:
        abort(404, description="Book or chapter not found")

    if v1 <= 0 or v1 > len(chapter_data['versiculos']) or v2 <= v1 or v2 > len(chapter_data['versiculos']):
        abort(404, description="Verses not found or bad prompting")

    verse_text = ' '.join(chapter_data['versiculos'][v1 - 1:v2])

    response = {
        'book': book,
        'chapter': chapter,
        'verses': list(range(v1, v2 + 1)),
        'data': verse_text
    }
    return jsonify(response), 200


@app.errorhandler(404)
def resource_not_found(e):
    response = jsonify(error=str(e))
    response.status_code = 404
    return response


if __name__ == "__main__":
    app.run(debug=True)
