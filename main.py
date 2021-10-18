from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from starlette.responses import RedirectResponse
from app.schemas import User, LoginSchema, MenuItem
from app.menu import saveJson, data, menu
from app.auth import signJWT
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.hash import get_password_hash, verify_password

app = FastAPI()

# Users
users = [
    {
        'username' : 'asdf',
        'password' : '$2b$12$Vaco7Mnoe3kFAKd7EJictuMLP53VyNyQgtM2EUUNxIUQIeuFQBtyu'
    }
]



auth_scheme = OAuth2PasswordBearer(tokenUrl='user/login')

# Routing
@app.get('/')
async def root():
    return (RedirectResponse('/docs'))


@app.post('/user/signup', tags=['Authorization'])
async def signup(newUser: User):
    user = newUser.dict()
    user['password'] = get_password_hash(user['password'])
    users.append(user)
    print(users)
    return ({
        'username' : newUser.username,
        'status' : 'user created'
    })


def check_user(data: LoginSchema):
    for user in users :
        if user['username'] == data.username and verify_password(data.password, user['password']) :
            return True
    return False

@app.post('/user/login', tags=['Authorization'])
async def user_login(user: OAuth2PasswordRequestForm = Depends()):
    if check_user(user) :
        return signJWT(user.username)
    return {
        'error' : 'wrong login details!'
    }

@app.get('/menu/', dependencies=[Depends(auth_scheme)], tags=['Menu'])
async def read_all_menu():
    try:
        return menu
    except:
        raise HTTPException(status_code=404, detail=f'item not found')


@app.get('/menu/{item_id}', dependencies=[Depends(auth_scheme)], tags=['Menu'])
async def read_menu(item_id: int):
    for menu_item in menu:
        if menu_item['id'] == item_id:
            return(menu_item)
    raise HTTPException(status_code=404, detail=f'item not found')


@app.post('/menu/', dependencies=[Depends(auth_scheme)], tags=['Menu'])
async def add_menu(request: MenuItem):
    newMenu = {'id': len(menu)+1, **request.dict()}
    menu.append(newMenu)
    
    # rewrite data menu with new menu
    data['menu'] = menu

    saveJson(data)
    return(newMenu)


@app.patch('/menu/{item_id}', dependencies=[Depends(auth_scheme)], tags=['Menu'])
async def update_menu(item_id: int, request: MenuItem):
    req = request.dict()
    for menu_item in menu:
        if menu_item['id'] == item_id:
            menu_item['name'] = req['name']
            data['menu'] = menu
            saveJson(data)
            return(menu_item, 'updated')


@app.delete('/menu/{item_id}', dependencies=[Depends(auth_scheme)], tags=['Menu'])
async def delete_menu(item_id: int):
    for menu_item in menu:
        if menu_item['id'] == item_id:
            menu.remove(menu_item)
            data['menu'] = menu
            saveJson(data)
            return(menu_item, 'deleted')

    raise HTTPException(status_code=404, detail=f'item not found')



