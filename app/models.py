from sqlalchemy import Integer, Column, String, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.sql.expression import text
from app.sqlalchemy_database import Base
from sqlalchemy.orm import relationship

class Posts(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=False, server_default='True')
    likes = Column(Integer, nullable=False, server_default='0')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User")


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))