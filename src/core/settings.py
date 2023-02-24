from pydantic import BaseSettings


class Settings(BaseSettings):
    host: str
    port: int

    login: str
    password: str 
    database_host: str 
    database_port: int 
    database_name: str

    admin_login: str
    admin_password: str

    jwt_expires_seconds: int
    jwt_secret: str
    jwt_algorithm: str

    class Config:
        env_file = '../.env'
        env_encoding = 'utf-8'


settings = Settings()
