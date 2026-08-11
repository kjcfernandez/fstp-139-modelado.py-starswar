from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Column, ForeignKey, Integer, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

favorite_planet = Table(
    "favorite_planet",
    db.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("planet_id", ForeignKey("planet.id"), primary_key=True)
)

favorite_character = Table(
    "favorite_character",
    db.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("character_id", ForeignKey("character.id"), primary_key=True)
)

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=True)
    firstname: Mapped[str] = mapped_column(String(80), nullable=False)
    lastname: Mapped[str] = mapped_column(String(80), nullable=False)

    favorite_planets: Mapped[list["Planet"]] = relationship("Planet", secondary=favorite_planet, back_populates="favorited_by_users")
    favorite_characters: Mapped[list["Character"]] = relationship("Character", secondary=favorite_character, back_populates="favorited_by_users")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "is_active": self.is_active,
            "favorite_planets": [p.serialize() for p in self.favorite_planets],
            "favorite_characters": [c.serialize() for c in self.favorite_characters]
        }


class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    height: Mapped[str] = mapped_column(String(20))
    hair_color: Mapped[str] = mapped_column(String(30))
    birth_year: Mapped[str] = mapped_column(String(20))

    favorited_by_users: Mapped[list["User"]] = relationship("User", secondary=favorite_character, back_populates="favorite_characters")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "hair_color": self.hair_color,
            "birth_year": self.birth_year,
        }


class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    climate: Mapped[str] = mapped_column(String(50))
    terrain: Mapped[str] = mapped_column(String(50))
    population: Mapped[str] = mapped_column(String(30))

    favorited_by_users: Mapped[list["User"]] = relationship("User", secondary=favorite_planet, back_populates="favorite_planets")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "terrain": self.terrain,
            "population": self.population,
        }