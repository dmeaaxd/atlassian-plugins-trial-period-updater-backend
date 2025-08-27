from fastapi import APIRouter


plugins_router = APIRouter(tags=["Основная логика получения триальных ключей для плагинов Atlassian"])


@plugins_router.get("/get-trial-keys")
async def get_trial_keys():
    if True:
        return {"message": "Success"}
    else:
        return {"message": "Error"}
    