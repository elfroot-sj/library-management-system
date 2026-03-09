from dataclasses import dataclass


@dataclass
class Book:
    id: int
    title: str
    authors: list[str]
    languages: list[str]
    first_publish_year: int

    def __str__(self) -> str:
        authors = ", ".join(self.authors)
        languages = ", ".join(self.languages)
        return f"{self.title} ({self.first_publish_year}) - {authors} [{languages}]"
