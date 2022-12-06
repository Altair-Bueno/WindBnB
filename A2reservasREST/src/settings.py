from pydantic import BaseModel, BaseSettings, MongoDsn, HttpUrl


class MongoConfig(BaseModel):
    url: MongoDsn
    collection: str
    database: str

    class Config:
        frozen = True

class PaypalConfig(BaseModel):
    url: HttpUrl
    clientid: str
    secret: str
    class Config:
        frozen = True

class Settings(BaseSettings):
    mongo: MongoConfig
    paypal: PaypalConfig

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "_"
        frozen = True
