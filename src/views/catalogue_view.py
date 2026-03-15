# Rotte per esplorare o cercare i libri nel database usando il Catalogue.

from flask import Blueprint, jsonify, request

from src.services.catalogue_service import CatalogueService

catalogue_bp = Blueprint("catalogue", __name__, url_prefix="/catalogue")
catalogue_service = CatalogueService()


@catalogue_bp.route("/books", methods=["GET"])
def get_books():
    books = catalogue_service.get_all_books()
    return jsonify([book.to_dict() for book in books]), 200


@catalogue_bp.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id: int):
    book = catalogue_service.get_book_by_id(book_id)
    if book is None:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(book.to_dict()), 200


@catalogue_bp.route("/books", methods=["POST"])
def add_book():
    data = request.get_json()
    if not data or "title" not in data or "authors" not in data:
        return jsonify({"error": "Missing required fields"}), 400
    book = catalogue_service.add_book(data)
    return jsonify(book.to_dict()), 201


@catalogue_bp.route("/books/<int:book_id>", methods=["DELETE"])
def remove_book(book_id: int):
    success = catalogue_service.remove_book(book_id)
    if not success:
        return jsonify({"error": "Book not found"}), 404
    return jsonify({"message": "Book deleted"}), 200


@catalogue_bp.route("/books/search", methods=["GET"])
def search_books():
    title = request.args.get("title")
    author = request.args.get("author")
    if title:
        books = catalogue_service.search_by_title(title)
    elif author:
        books = catalogue_service.search_by_author(author)
    else:
        return jsonify({"error": "Provide title or author query parameter"}), 400
    return jsonify([book.to_dict() for book in books]), 200
