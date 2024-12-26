import uuid

from sqlalchemy import UUID, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship

Base = declarative_base()


class WalletInfoModel(Base):
    __tablename__ = 'wallets'

    uid: Mapped[uuid.UUID] = mapped_column(type_=UUID, primary_key=True, nullable=False)
    address: Mapped[str]
    bandwidth: Mapped[int]
    energy: Mapped[int]
    balance_trx: Mapped[int]
