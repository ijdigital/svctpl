from fastapi import Depends
from typing import Dict, Optional, Any, AnyStr

from config.application import service as app
from services import OptionService
from schemas import OptionCreateModel, OptionResponseModel, OptionsResponseModel, OptionUpdateRequestModel


@app.get('/options')
async def get() -> Any:
    service: OptionService = OptionService()
    return await service.get()


@app.get('/options/{key}', response_model=OptionResponseModel, status_code=200)
async def single(key: AnyStr) -> OptionResponseModel:
    service: OptionService = OptionService()
    return await service.single(key=key)


@app.post('/options', response_model=OptionResponseModel, status_code=201)
async def create(option: OptionCreateModel) -> OptionResponseModel:
    service: OptionService = OptionService()
    return await service.create(option=option)


@app.patch('/options/{key}', response_model=OptionResponseModel, status_code=202)
async def update(key: AnyStr, option: OptionUpdateRequestModel) -> OptionResponseModel:
    service: OptionService = OptionService()
    return await service.update(key=key, option_request=option)


@app.delete('/options/{key}', status_code=204)
async def delete(key: AnyStr) -> None:
    service: OptionService = OptionService()
    return await service.delete(key=key)
