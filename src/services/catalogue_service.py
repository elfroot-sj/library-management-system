from src.models.base import db
from src.models.book.book import Book
from src.models.book.book_model import BookModel
from src.models.catalogue.catalogue import Catalogue
from src.models.catalogue.catalogue_model import CatalogueModel
from src.services.reader import Reader


class CatalogueService:
    def __init__(self) -> None:
        self.reader = Reader()
        self.catalogue = Catalogue()

    # --- Metodi di Dominio & Integrazione ---

    def add_book_from_search(self, title_query: str) -> Book | None:
        raw_data = self.__fetch_external_data(title_query)
        if not raw_data or "error" in raw_data:
            return None

        # Crea istanza di dominio
        new_book = self.__map_to_domain(raw_data)
        self.catalogue.add_book(new_book)

        # Persistenza su DB
        # Cerchiamo o creiamo un catalogo di default
        main_catalogue: CatalogueModel | None = CatalogueModel.query.filter_by(
            name="Main Catalogue"
        ).first()
        if not main_catalogue:
            main_catalogue = CatalogueModel()
            main_catalogue.name = "Main Catalogue"
            db.session.add(main_catalogue)
            db.session.commit()

        self.add_book(
            {
                "title": new_book.get_title(),
                "authors": new_book.get_authors(),
                "languages": new_book.get_languages(),
                "first_publish_year": new_book.get_first_publish_year(),
                "cover_url": new_book.get_cover_url(),
                "catalogue_id": main_catalogue.id,
            }
        )

        return new_book

    def __fetch_external_data(self, title: str) -> dict:
        path = f"search.json?title={title.replace(' ', '+')}"
        return self.reader.get_data(path)

    def __map_to_domain(self, data: dict) -> Book:
        return Book(
            id=data.get("id"),
            title=data.get("title"),
            authors=data.get("authors", []),
            languages=data.get("languages", []),
            first_publish_year=data.get("first_publish_year"),
            cover_url=data.get("cover_url"),
        )

    # --- Metodi di Persistenza (SQLAlchemy) ---

    def get_all_books(self) -> list[BookModel]:
        return BookModel.query.all()

    def get_book_by_id(self, book_id: int) -> BookModel | None:
        return BookModel.query.get(book_id)

    def add_book(self, data: dict) -> BookModel:
        book = BookModel()
        book.title = data["title"]
        book.authors = (
            ",".join(data["authors"])
            if isinstance(data["authors"], list)
            else data["authors"]
        )
        book.languages = (
            ",".join(data["languages"])
            if isinstance(data["languages"], list)
            else data["languages"]
        )
        book.first_publish_year = data.get("first_publish_year")
        book.cover_url = data.get("cover_url")
        book.catalogue_id = data.get("catalogue_id")
        db.session.add(book)
        db.session.commit()
        return book

    def remove_book(self, book_id: int) -> bool:
        book = self.get_book_by_id(book_id)
        if book is None:
            return False
        db.session.delete(book)
        db.session.commit()
        return True

    def search_by_title(self, title: str) -> list[BookModel]:
        return BookModel.query.filter(BookModel.title.ilike(f"%{title}%")).all()

    def search_by_author(self, author: str) -> list[BookModel]:
        return BookModel.query.filter(BookModel.authors.ilike(f"%{author}%")).all()
