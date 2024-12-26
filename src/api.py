import logging
from fastapi import APIRouter, HTTPException, Depends

from src.database.core import DatabaseCore
from src.database.repository import WalletRepository
from src.schemas import WalletInfo, AddWalletInfo
from src.config import DATABASE_URL
from src.tron_service import TronService, TronServiceException, InvalidAddressException

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

wallet_router = APIRouter()

db_core = DatabaseCore(url=DATABASE_URL)
db_core.create_tables()


@wallet_router.post("/wallet", response_model=AddWalletInfo)
def add_wallet_info(address: str, db_session = Depends(db_core.get_session)):
    LOGGER.info(f"Wallet information query: {address}")
    try:
        wallet_repository = WalletRepository(session=db_session)
        tron_service = TronService(wallet_repository=wallet_repository)
        wallet_info = tron_service.get_new_wallet_info(address)

        tron_service.save_wallet_info(wallet_info=wallet_info)
        db_session.commit()

        LOGGER.info(f"Wallet information was saved: {wallet_info}")
        return wallet_info

    except InvalidAddressException as err:
        LOGGER.error(f"Invalid tron address: {err}")
        raise HTTPException(status_code=400, detail=str(err))

    except TronServiceException as err:
        LOGGER.error(f"Cant get information from tron api: {err}")
        raise HTTPException(status_code=500, detail=str(err))

    except Exception as err:
        LOGGER.error(f"Error retrieving wallet information: {err}")
        raise HTTPException(status_code=500, detail=str(err))


@wallet_router.get("/wallets", response_model=list[WalletInfo])
def get_wallets(limit: int = 10, offset: int = 0, db_session = Depends(db_core.get_session)):
    try:
        wallet_repository = WalletRepository(session=db_session)
        tron_service = TronService(wallet_repository=wallet_repository)
        wallets = tron_service.get_wallets(limit, offset)

        LOGGER.info(f"Got {len(wallets)} wallets from db.")
        return wallets

    except Exception as err:
        LOGGER.error(f"Cant get wallets from db with error: {err}")
        raise HTTPException(status_code=500, detail=str(err))
