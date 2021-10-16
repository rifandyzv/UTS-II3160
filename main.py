from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from starlette.responses import RedirectResponse
from app.schemas import Token, TokenData, User, LoginSchema, MenuItem
import json
from app.auth import signJWT
from app.auth_bearer import JWTBearer

from fastapi.security import OAuth2PasswordBearer


app = FastAPI()


# Menus
with open('menu.json', 'r') as read_file:
    data = json.load(read_file)


def saveJson(data):
    with open('menu.json', 'w') as dumpFile:
        json.dump(data, dumpFile)

menu = data['menu']

# Users
users = []






# Routing
@app.get("/")
async def root():
    return (RedirectResponse("/docs"))


@app.post("/user/signup", tags=['Authorization'])
async def signup(newUser: User):
    users.append(newUser)
    return signJWT(newUser.username)


def check_user(data: LoginSchema):
    for user in users :
        if user.username == data.username and user.password == data.password :
            return True
    return False

@app.post("/user/login", tags=['Authorization'])
async def user_login(user: LoginSchema):
    if check_user(user) :
        return signJWT(user.username)
    return {
        'error' : 'wrong login details!'
    }



@app.get('/menu/', dependencies=[Depends(JWTBearer())], tags=['Menu'])
async def read_menu():
    try:
        return menu
    except:
        raise HTTPException(status_code=404, detail=f'item not found')


@app.get('/menu/{item_id}', dependencies=[Depends(JWTBearer())], tags=['Menu'])
async def read_menu(item_id: int):
    for menu_item in menu:
        if menu_item['id'] == item_id:
            return(menu_item)
    raise HTTPException(status_code=404, detail=f'item not found')


@app.post('/menu/', dependencies=[Depends(JWTBearer())], tags=['Menu'])
async def add_menu(request: MenuItem):
    newMenu = {'id': len(menu)+1, **request.dict()}
    menu.append(newMenu)
    
    # rewrite data menu with new menu
    data['menu'] = menu

    saveJson(data)
    return(newMenu)


@app.patch('/menu/{item_id}', dependencies=[Depends(JWTBearer())], tags=['Menu'])
async def update_menu(item_id: int, request: MenuItem):
    req = request.dict()
    for menu_item in menu:
        if menu_item['id'] == item_id:
            menu_item['name'] = req['name']
            return(menu_item)
    data['menu'] = menu
    saveJson(data, "updated")


@app.delete('/menu/{item_id}', dependencies=[Depends(JWTBearer())], tags=['Menu'])
async def delete_menu(item_id: int):
    for menu_item in menu:
        if menu_item['id'] == item_id:
            menu.remove(menu_item)
            data['menu'] = menu
            saveJson(data)
            return(menu_item, "deleted")

    raise HTTPException(status_code=404, detail=f'item not found')



