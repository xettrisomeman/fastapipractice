from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from jose import jwt, ExpiredSignatureError, JWTError




from models import User, Post
from schema import (
    UserCreateSchema, UserDisplaySchema, UserDataSchema,
    PostCreateSchema, PostDisplaySchema)
import utils
from database import get_db

from sqlalchemy.orm import Session

from datetime import datetime, timedelta


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name='static')


templates = Jinja2Templates(directory="templates/")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

JWT_SECRET = "salttlas....everestsereve" # salt maybe lol
JWT_ALGORITHM = "HS256"
JWT_VALID_TIME = 30 # 30 minutes



def authenticate_user(token: str = Depends(oauth2_scheme),
db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to decode token, error: Signature has expired"
        )
    except JWTError:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials."
        )

    user_name = payload.get("sub")

    user = db.query(User).filter_by(username=user_name).first()

    return UserDataSchema.from_orm(user)


# show posts















###################################################################
#API


@app.get("/api/me")
def get_me(user: UserDataSchema = Depends(authenticate_user)):
    return {
        "message" : user
    }



@app.get("/api/post/{id}")
def get_posts(id: int , user: UserDataSchema = Depends(authenticate_user), 
db: Session = Depends(get_db)):
    
    data = db.query(Post).filter_by(id=id).first() # calling backref table
    if not data:
        return {
                "message": f"There is no post with id {id}"
        }
    return PostDisplaySchema.from_orm(data)



@app.get("/api/posts")
def get_posts(user: UserDataSchema = Depends(authenticate_user), 
db: Session = Depends(get_db)):
    datasets = db.query(User).filter_by(username=user.username).first().posts
    if not datasets:
        return {
                "message": "The user has not created a post."
        }
    data_list = [PostDisplaySchema.from_orm(data) for data in datasets]

    return data_list


@app.post('/api/posts')
def create_posts(user_posts: PostCreateSchema, user: UserDataSchema = Depends(authenticate_user), db: Session = Depends(get_db)):

    user_id = user.id
    posts = Post(
        title=user_posts.title,
        body=user_posts.body,
        author_id=user_id
    )
    db.add(posts)
    db.commit()

    return PostDisplaySchema.from_orm(posts)




@app.post("/api/login")
def login(request_data: OAuth2PasswordRequestForm = Depends(),
db: Session = Depends(get_db)):
    #check if user exists or not
    user = db.query(User).filter_by(username = request_data.username).first()
    #check password hash
    password = utils.verify_password(request_data.password, user.hashed_password)

    if not password or not user:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Incorrect username or password"
        )

    user_obj = user.username

    data = {
        'sub': user_obj, # sub -> username
        'iat': datetime.utcnow(), # start date
        'exp': datetime.utcnow() + timedelta(minutes=JWT_VALID_TIME) # expiry date
    }

    token = jwt.encode(data, JWT_SECRET)


    return {'access_token': token, 'token_type': 'bearer'}




@app.post('/api/register', response_model=UserDisplaySchema, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreateSchema,
            db: Session = Depends(get_db)):

    # check if user exists or not
    user_obj = db.query(User).filter_by(username=user.username).first()

    if user_obj:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail= "User with the username already exists."
        )

    if len(user.password) < 8:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Password length should be greather than 8"
        )

    hashed_password = utils.hash_password(user.password)
    new_user = User(
        username=user.username,
        hashed_password = hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)


    return UserDisplaySchema.from_orm(new_user)

