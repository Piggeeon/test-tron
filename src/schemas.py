from uuid import UUID

from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class AddWalletInfo(BaseSchema):
    address: str
    bandwidth: int
    energy: int
    balance_trx: int

class WalletInfo(AddWalletInfo):
    uid: UUID
