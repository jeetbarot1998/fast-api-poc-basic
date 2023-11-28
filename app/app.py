import datetime
import secrets

from fastapi import FastAPI, status, HTTPException, Depends, Form, websockets
from fastapi.responses import RedirectResponse
from geopy import Nominatim
from starlette.websockets import WebSocket

from app.connections.mysql_connection_orm import get_db
from app.dal import add_into_table_with_dict
from app.models import UserLocation, UserTable
from app.schemas import UserOut, UserAuth, TokenSchema, SystemUser, UserLocationData
from app.utils import (
    get_hashed_password,
    create_access_token,
    create_refresh_token,
    verify_password
)
from app.deps import get_current_user
from typing import Union, Any, Annotated
from sqlalchemy.orm import Session

app = FastAPI()



@app.get('/', response_class=RedirectResponse, include_in_schema=False)
async def docs():
    return RedirectResponse(url='/docs')


@app.post('/signup', summary="Create new user", response_model=UserOut)
async def create_user(data: UserAuth,  db: Session = Depends(get_db)):
    # querying database to check if user already exist
    user = db.query(UserTable).filter(UserTable.email == data.email).first()
    if user is not None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist")
    user = dict(data)
    user['password'] = get_hashed_password(data.password)
    add_into_table_with_dict(UserTable, db, user)
    return user


@app.post('/login', summary="Create access and refresh tokens for user", response_model=TokenSchema)
async def login(form_data: UserAuth = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserTable).filter(UserTable.email == form_data.email).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    hashed_pass = user.password
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    return {
        "access_token": create_access_token(user.email),
        "refresh_token": create_refresh_token(user.email),
    }

@app.get('/me', summary='Get details of currently logged in user')
async def get_me(db: Session = Depends(get_db), user: SystemUser = Depends(get_current_user)):
    print("me===================" + str(db))
    return user

@app.post('/test', summary='Test Post Api')
async def test(payload:dict, db: Session = Depends(get_db), user=Depends(get_current_user) ):
    print("test===================" + str(db))
    print(user)
    print(payload)
    print(type(payload))
    a = {1:2}
    return 1


@app.post("/create_item/")
async def create_item(name: str, db: Session = Depends(get_db),  user: SystemUser = Depends(get_current_user)):
    new_item = UserTable(username=name)
    db.add(new_item)
    db.commit()
    return new_item

@app.get("/get_item")
async def create_item(email: str, db: Session = Depends(get_db),  user: SystemUser = Depends(get_current_user)):
    item = db.query(UserTable).filter(UserTable.email == email).all()
    return item


# ============================================


@app.post("/generate_url")
async def generate_url(payload : UserLocationData = Depends() ,  db: Session = Depends(get_db), user: SystemUser = Depends(get_current_user)):
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
    data:UserLocation = db.query(UserLocation).filter(UserLocation.map_id == user.id).first()
    if data:
        for key, value in (dict(payload)).items():
             setattr(data, key, value)
        if payload.first_attempt:
            token = secrets.token_urlsafe(16)  # Generate a random token
            setattr(data, 'expiration_time', expiration_time)
            setattr(data, 'token', token)
    else:
        token = secrets.token_urlsafe(16)  # Generate a random token
        data = UserLocation(token=token, longitude=payload.longitude,
                                latitude=payload.latitude,
                                map_id=user.id, expiration_time=expiration_time)
        db.add(data)
    db.commit()

    db.refresh(data)
    # db.close()
    url = f"ws://localhost:8080/ws/live-location/{data.token}"
    return {"url": url}


@app.post("/update_location")
async def update_location(payload : UserLocationData = Depends() ,  db: Session = Depends(get_db), user: SystemUser = Depends(get_current_user)):
    user_location = db.query(UserLocation).filter(UserLocation.map_id == user.id).first()
    if user_location:
        user_location.latitude = payload.latitude
        user_location.longitude = payload.longitude
        db.commit()
        db.refresh(user_location)
        return 'Success'


@app.websocket("/ws/live-location/{token}")
async def get_live_location(token: str, websocket: WebSocket, db: Session = Depends(get_db)):

    await websocket.accept()
    geolocator = Nominatim(user_agent="location_tracker")  # Initialize geolocator
    while True:
        try:
            data = await websocket.receive_text()
            db_token : UserLocation=  db.query(UserLocation).filter(UserLocation.token == token).first()
            if db_token:
                if (datetime.datetime.utcnow() + datetime.timedelta(minutes=60)) < db_token.expiration_time:
                    # Valid token, provide access to live location data
                    latitude = db_token.latitude
                    longitude = db_token.longitude

                    location = geolocator.reverse(f"{40.7128}, {-74.0060}")  # Get location details
                    # location = geolocator.reverse(f"{latitude}, {longitude}")  # Get location details
                    print(location)
                    location_data = {
                        'latitude': str(latitude),
                        'longitude': str(longitude),
                        # 'address': location.address if location else None
                    }

                    await websocket.send_json(location_data)  # Sending location data as JSON to the client
                    # await asyncio.sleep(5)  # Simulate updating the location every 5 seconds (adjust as needed)
                else:
                    await websocket.send_json({'message': 'link expired'})
                    # await websocket.close()
        except websockets.ConnectionClosedError:
            break
        except Exception as e:
        # Handle the specific exception for a closed connection
            if isinstance(e, ConnectionError):
                print("Connection closed or error occurred:", e)
            else:
                print("Other exception occurred:", e)


# @app.get("/live-location/{token}")
# async def get_live_location(token: str, db: Session = Depends(get_db), user: SystemUser = Depends(get_current_user)):
#     db_token = db.query(Token).filter(Token.id == token).first()
#
#     if db_token:
#         if datetime.utcnow() < db_token.expiration_time:
#             # Valid token, provide access to live location data
#             user_id = db_token.user_id
#             # Here you would retrieve and return the live location data associated with the user_id
#             db.close()
#             return {"message": f"Access granted to live location for user {user_id}"}
#         else:
#             db.delete(db_token)  # Remove expired token from the database
#             db.commit()
#             db.close()
#             raise HTTPException(status_code=401, detail="Token expired")
#
#     db.close()
#     raise HTTPException(status_code=401, detail="Invalid token")

# =============================================

active_connections = {}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    geolocator = Nominatim(user_agent="location_tracker")  # Initialize geolocator

    await websocket.accept()

    while True:

        try:
            data = await websocket.receive_text()
            # Simulated data, replace this with your actual location data logic
            latitude = 40.7128
            longitude = -74.0060

            location = geolocator.reverse(f"{latitude}, {longitude}")  # Get location details

            location_data = {
                'latitude': latitude,
                'longitude': longitude,
            }

            await websocket.send_json(location_data)  # Sending location data as JSON to the client
            # await asyncio.sleep(5)  # Simulating updates every 5 seconds, adjust as needed
        except Exception:
            break







# post clicking of go button => A url is generated with the token appended. This
# url is saved in the db. In the entry, there will be location of the user and the list of user ids of
# emergency contacts. When these emergency contacts try to access the uri,
# backend will get an access to 2 things
# 1. the uri, hence the token. So we will get the location of the primary user
# 2. the user requesting, so we will get the user id. If this user id exists in the list of users
#     for the respective token in the db, then we will give access else abort.

# user_details table
# id
# email
# username
# password
# emergency 1
# emergency 2
# emergency 3
# created at
# updated on

