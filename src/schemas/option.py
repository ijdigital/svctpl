from pydantic import BaseModel
from typing import List, Dict


class OptionCreateModel(BaseModel):
    key: str
    value: Dict


class OptionResponseModel(BaseModel):
    key: str
    value: Dict


class OptionsResponseModel(BaseModel):
    options: List[OptionResponseModel]
