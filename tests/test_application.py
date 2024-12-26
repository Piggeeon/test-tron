from unittest.mock import MagicMock

from fastapi.testclient import TestClient
from src.main import app

from src.schemas import AddWalletInfo
from src.tron_service import TronService

client = TestClient(
    app,
    base_url="http://127.0.0.1:8080/api/v1",
    raise_server_exceptions=True
)

def test_add_wallet_info():
    response = client.post("/wallet", params={"address": "TE2RzoSV3wFK99w6J9UnnZ4vLfXYoxvRwP"})
    assert response.status_code == 200


def test_save_wallets_info():
    mock_repository = MagicMock()
    wallet_service = TronService(wallet_repository=mock_repository)

    sample_wallet_info = AddWalletInfo(address="TE2RzoSV3wFK99w6J9UnnZ4vLfXYoxvRwP",
                                       bandwidth=600,
                                       energy=0,
                                       balance_trx=1000)

    wallet_service.save_wallet_info(sample_wallet_info)

    mock_repository.add_wallet_info.assert_called_once()
