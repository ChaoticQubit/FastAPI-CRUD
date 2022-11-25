from sqlalchemy import Integer, Column, String, Boolean, TIMESTAMP
from sqlalchemy.sql.expression import text
from app.sqlalchemy_database import Base

class Posts(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=False, server_default='True')
    likes = Column(Integer, nullable=False, server_default='0')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))