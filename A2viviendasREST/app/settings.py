from pydantic import BaseModel, BaseSettings, HttpUrl


class MongoConfig(BaseModel):
    url: str
    collection: str
    valoraciones: str
    database: str

    class Config:
        frozen = True

class AuthConfig(BaseModel):
    baseurl: HttpUrl
    audience: str

    class Config:
        frozen = True

class Settings(BaseSettings):
    mongo: MongoConfig
    # aws: AWSConfig
    auth: AuthConfig

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "_"
        frozen = True