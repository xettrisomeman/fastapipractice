from pydantic import BaseModel





# user schema
class UserSchema(BaseModel):
    username: str

    class Config:
        orm_mode = True


class UserCreateSchema(UserSchema):
    password: str



class UserDisplaySchema(UserSchema):
    id: int



class UserDataSchema(UserDisplaySchema):
    hashed_password: str


#######################################################


# post schema

class PostSchema(BaseModel):
    title: str
    body: str


    class Config:
        orm_mode = True


class PostCreateSchema(PostSchema):
    pass


class PostDisplaySchema(PostSchema):
    id: int
    author_id: int



