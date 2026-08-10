from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Column, ForeignKey, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=True)
    firstname: Mapped[str] = mapped_column(String(80), nullable=False)
    lastname: Mapped[str] = mapped_column(String(80), nullable=False)
    subscription_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.timezone.utc)

    favorites: Mapped[list["Favorite"]] = relationship("Favorite", back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "is_active": self.is_active,
            "subscription_date": self.subscription_date.isoformat(),
            "favorites": [fav.serialize() for fav in self.favorites]
            # do not serialize the password, its a security breach
        }


class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    height: Mapped[str] = mapped_column(String(20))
    hair_color: Mapped[str] = mapped_column(String(30))
    birth_year: Mapped[str] = mapped_column(String(20))

    favorited_by: Mapped[list["Favorite"]] = relationship("Favorite", back_populates="character")

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

    favorited_by: Mapped[list["Favorite"]] = relationship("Favorite", back_populates="planet")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "terrain": self.terrain,
            "population": self.population,
        }


class Favorite(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"), nullable=True)
    character_id: Mapped[int] = mapped_column(ForeignKey("character.id"), nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="favorites")
    planet: Mapped["Planet"] = relationship("Planet", back_populates="favorited_by")
    character: Mapped["Character"] = relationship("Character", back_populates="favorited_by")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet": self.planet.serialize() if self.planet else None,
            "character": self.character.serialize() if self.character else None,
        }