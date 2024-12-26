import logging
import time
import uuid

from tronpy import Tron
from tronpy.exceptions import AddressNotFound

from src.schemas import AddWalletInfo, WalletInfo

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


class TronServiceException(Exception):
    pass


class InvalidAddressException(TronServiceException):
    pass


class TronService:
    def __init__(self, wallet_repository):
        self.client = Tron()
        self.wallet_repository = wallet_repository

    def get_new_wallet_info(self, address: str) -> AddWalletInfo:
        """Get wallet info by given address."""
        try:
            time.sleep(1)
            account_resource = self.client.get_account_resource(address)
            energy_limit =  account_resource.get("EnergyLimit", 0)
            energy_used =  account_resource.get("EnergyUsed", 0)
            energy = energy_limit - energy_used
            time.sleep(1)

            bandwidth = self.client.get_bandwidth(address)
            time.sleep(1)

            balance_trx = int(self.client.get_account_balance(address))
            time.sleep(1)

            return AddWalletInfo(
                address=address,
                bandwidth=bandwidth,
                energy=energy,
                balance_trx=balance_trx
            )

        except AddressNotFound as err:
            LOGGER.error(f"Invalid wallet address: {address}")
            raise InvalidAddressException(f"Invalid wallet address: {address}") from err
        except Exception as err:
            raise TronServiceException(f"Error with get wallet info {err}")

    def save_wallet_info(self, wallet_info: AddWalletInfo):
        uid = uuid.uuid4()
        wallet_info_with_uid = WalletInfo(uid=uid, **wallet_info.model_dump())
        self.wallet_repository.add_wallet_info(wallet_info_with_uid)

    def get_wallets(self, limit: int = 10, offset: int = 0):
        return self.wallet_repository.get_wallets_info(limit, offset)
