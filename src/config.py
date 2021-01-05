from pydantic import BaseSettings


class Env(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_DB: str
    PGADMIN_LISTEN_PORT: int
    PGADMIN_DEFAULT_EMAIL: str
    PGADMIN_DEFAULT_PASSWORD: str

    class Config:
        env_file = ".env"  # .envを読み込み、初期化時のキーワード引数を受け取らなかった場合に、それらの値が適用される

    @property
    def connection_string(self) -> str:
        return "postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DB}".format(
            POSTGRES_USER=self.POSTGRES_USER,
            POSTGRES_PASSWORD=self.POSTGRES_PASSWORD,
            POSTGRES_SERVER=self.POSTGRES_SERVER,
            POSTGRES_DB=self.POSTGRES_DB,
        )

    def to_env_file_str(self) -> str:
        values = []
        for field_name in self.__fields__.keys():
            value = getattr(self, field_name)
            values.append(
                f"{field_name}={value}",
            )
        return "\n".join(values)
