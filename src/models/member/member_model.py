from ..base import db


class MemberModel(db.Model):
    __tablename__ = "members"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    address = db.Column(db.String(255), nullable=True, default="")

    def update_from_dict(self, data: dict) -> None:
        self.username = data["username"]
        self.email = data["email"]
        self.password = data["password"]
        self.address = data.get("address", "")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "address": self.address,
        }
