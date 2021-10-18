import jwt

JWT_SECRET = b'7d02b0a882dac395c44e1fc000bc5340a2d055b30be580cd'
JWT_ALGORITHM = 'HS256'

def token_response(token: str):
    return {
        "access_token" : token
    }

def signJWT(user_id: str) :
    payload = {
        "user_id" : user_id
    }
    token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)

    return token_response(token)

def decodeJWT(token: str) :
    try :
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token
    except :
        return {'message' : 'Failed to decode token'}


