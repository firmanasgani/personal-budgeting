from models.base import Base
from sqlalchemy.sql import func
from sqlalchemy import String,  Float, DateTime, Date
from sqlalchemy.orm import mapped_column

class Transaction(Base):
    __tablename__ = "transactions"

    id = mapped_column(String, primary_key=True)
    userid = mapped_column(String, nullable=False)
    categoryid = mapped_column(String, nullable=False)
    amount = mapped_column(Float)
    description = mapped_column(String)
    date_transaction = mapped_column(Date)
    date_created = mapped_column(DateTime(timezone=True), server_default=func.now())
    created_by = mapped_column(String)
    date_updated = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    updated_by = mapped_column(String)