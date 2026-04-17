from fastapi import Depends, FastAPI

from auth import get_current_user


app = FastAPI()


@app.get('/')
async def root():
    return {"message": "Welcome"}


@app.get('/health')
async def health():
    return {'message': "healthy"}


@app.get('/public')
async def public():
    return {'message': "Public handler"}


@app.get('/private', responses={
    200: {"description": "Access"},
    401: {"description": "Not authentificat"}})
async def private(username: str = Depends(get_current_user)):
    return {'message': 'OK',
            'user': username}