from models.base import Base


from sqlalchemy.sql import func
from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import mapped_column
import bcrypt

class Users(Base):
    __tablename__ = "users"

    id = mapped_column(String, primary_key=True)
    username = mapped_column(String, nullable=False)
    fullname = mapped_column(String, nullable=False)
    password = mapped_column(String, nullable=False)
    is_deleted = mapped_column(Integer, default=0)
    time_updated = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))