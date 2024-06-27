from fastapi import Response
from typing import List, Optional, Dict

from models import Option
from schemas import *


class OptionService:
    _model: Option = Option

    async def get(self) -> OptionsResponseModel:
        options: List[Option] = await Option.all()

        return_dict: Dict = {
            'options': [OptionResponseModel(**x.__dict__) for x in options]
        }
        return OptionsResponseModel(**return_dict)

    async def create(self, option: OptionCreateModel) -> OptionResponseModel:
        option: Option = await Option.create(**option.dict())
        await option.save()

        return OptionResponseModel(**option.__dict__)
