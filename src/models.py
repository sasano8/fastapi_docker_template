import sqlalchemy as sa

from src.db import Base


class UserModel(Base):
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    name = sa.Column(sa.String)
    age = sa.Column(sa.Integer)
