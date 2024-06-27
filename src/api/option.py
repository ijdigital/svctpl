from fastapi import Depends
from typing import Dict, Optional, Any

from config.application import service as app
from services import OptionService
from schemas import OptionCreateModel, OptionResponseModel, OptionsResponseModel


@app.get('/options')
async def get() -> Any:
    service: OptionService = OptionService()
    return await service.get()


@app.post('/options', response_model=OptionResponseModel, status_code=201)
async def create(option: OptionCreateModel) -> OptionResponseModel:
    service: OptionService = OptionService()
    return await service.create(option=option)
