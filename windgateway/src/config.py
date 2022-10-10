from pydantic import BaseConfig, BaseModel

class MongoConfig(BaseModel):
    connectionUrl: str

class AWSConfig(BaseModel):
    cognitoUrl: str

class Config(BaseConfig):
    mongo: MongoConfig
    aws: AWSConfig

