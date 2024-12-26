from sqlalchemy.orm import Session

from src.database.models import WalletInfoModel
from src.schemas import WalletInfo


class WalletRepository:
    def __init__(self, session):
        self.session: Session = session

    def add_wallet_info(self, wallet_info: WalletInfo):
        wallet_info_model = WalletInfoModel(**wallet_info.model_dump())
        self.session.add(wallet_info_model)

    def get_wallets_info(self, limit: int = 10, offset: int = 0) -> list[WalletInfo]:
        wallets = self.session.query(WalletInfoModel).offset(offset).limit(limit).all()
        res = []
        for wallet in wallets:
            res.append(WalletInfo.model_validate(wallet))

        return res
