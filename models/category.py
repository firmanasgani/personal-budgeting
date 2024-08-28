from models.base import Base

from sqlalchemy.sql import func
from sqlalchemy import String, Integer, DateTime,Enum
from sqlalchemy.orm import mapped_column

class Category(Base):
    __tablename__ = "category"

    id = mapped_column(String, primary_key=True)
    name = mapped_column(String, nullable=False)
    code = mapped_column(String, nullable=False)
    is_deleted = mapped_column(Integer, default=0)
    time_updated = mapped_column(DateTime(timezone=True), server_default=func.now())
    created_by = mapped_column(String, nullable=False)
    time_updated = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    updated_by = mapped_column(String, nullable=False)
    type=mapped_column(Enum("expenses", "income", name="type"), nullable=False)
