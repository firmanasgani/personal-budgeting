from models.base import Base
from sqlalchemy.sql import func
from sqlalchemy import String, Integer, DateTime, Date
from sqlalchemy.orm import mapped_column

class Budget(Base):
    __tablename__ = "budget"

    id = mapped_column(String, primary_key=True)
    userid = mapped_column(String, nullable=False)
    categoryid = mapped_column(String, nullable=False)
    is_deleted = mapped_column(Integer, default=0)
    time_created = mapped_column(DateTime(timezone=True), server_default=func.now())
    created_by = mapped_column(String, nullable=False)
    time_updated = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    updated_by = mapped_column(String, nullable=False)
    amount = mapped_column(Integer, nullable=False)
    start_date = mapped_column(Date, nullable=False)
    end_date = mapped_column(Date, nullable=False)
    description = mapped_column(String)