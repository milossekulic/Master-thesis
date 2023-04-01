from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP, BigInteger

from .database import Base





class LicensePlate(Base):
    __tablename__ = "license_plate"

    id = Column(Integer, primary_key=True, nullable=False)
    license_plate = Column(String, nullable=False)
    owner = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    # created_by = Column(Integer, ForeignKey(
    #     "users.id", ondelete="CASCADE"), nullable=False)

    users = relationship("User")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(255), nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))
