from fastapi import FastAPI, HTTPException
from starlette.responses import RedirectResponse
from app.schemas import *
import json

app = FastAPI()


# Menus
with open('menu.json', 'r') as read_file:
    data = json.load(read_file)


def saveJson(data):
    with open('menu.json', 'w') as dumpFile:
        json.dump(data, dumpFile)

menu = data['menu']

# Users
users = [
    {
        'username': 'admin',
        'password': 'admin'
    }
]





# Routing
@app.get("/")
async def root():
    return (RedirectResponse("/docs"))

@app.get('/menu/')
async def read_menu():
    try:
        return menu
    except:
        raise HTTPException(status_code=404, detail=f'item not found')


@app.get('/menu/{item_id}')
async def read_menu(item_id: int):
    for menu_item in menu:
        if menu_item['id'] == item_id:
            return(menu_item)
    raise HTTPException(status_code=404, detail=f'item not found')


@app.post('/menu/')
async def add_menu(request: MenuItem):
    newMenu = {'id': len(menu)+1, **request.dict()}
    menu.append(newMenu)
    
    # rewrite data menu with new menu
    data['menu'] = menu

    saveJson(data)
    return(newMenu)


@app.patch('/menu/{item_id}')
async def update_menu(item_id: int, request: MenuItem):
    req = request.dict()
    for menu_item in menu:
        if menu_item['id'] == item_id:
            menu_item['name'] = req['name']
            return(menu_item)
    data['menu'] = menu
    saveJson(data, "updated")


@app.delete('/menu/{item_id}')
async def delete_menu(item_id: int):
    for menu_item in menu:
        if menu_item['id'] == item_id:
            menu.remove(menu_item)
            data['menu'] = menu
            saveJson(data)
            return(menu_item, "deleted")

    raise HTTPException(status_code=404, detail=f'item not found')


@app.post("/user/signup")
async def signup(newUser: User):
    users.append(newUser)
    return(newUser)


