import os

import typer

from src.config import Env

app = typer.Typer()
server = typer.Typer(help="APIサーバー関連のコマンド集です。")
conf = typer.Typer(help="設定ファイル関連のコマンド集です。")
db = typer.Typer(help="データベース関連のコマンド集です。")

app.add_typer(server, name="server")
app.add_typer(conf, name="config")
app.add_typer(db, name="db")


@server.command()
def start() -> None:
    """アプリケーションサーバを起動します"""
    import uvicorn

    uvicorn.run("src.api:app", host="0.0.0.0", port=8080)


@server.command()
def start_debug() -> None:
    """VSCodeとデバッグ連携可能なアプリケーションサーバを起動します"""
    import uvicorn

    editor = "VSCODE"

    if editor == "VSCODE":
        import debugpy

        # デバッガーがアタッチされるまで待機する
        debugpy.listen(("0.0.0.0", 5678))
        debugpy.wait_for_client()
    else:
        raise Exception()

    uvicorn.run("src.api:app", host="0.0.0.0", port=8080, reload=True)


@conf.command()
def init(
    POSTGRES_USER: str = typer.Option("postgres", prompt=True),
    POSTGRES_PASSWORD: str = typer.Option(
        "81f4e99fd99fb97039cf755532ce2b98f308dc417c0ed6d34ba2b9f739a2e30d", prompt=True
    ),
    POSTGRES_SERVER: str = typer.Option("db", prompt=True),
    POSTGRES_DB: str = typer.Option("sample_db", prompt=True),
    PGADMIN_LISTEN_PORT: int = typer.Option(5050, prompt=True),
    PGADMIN_DEFAULT_EMAIL: str = typer.Option("admin@example.com", prompt=True),
    PGADMIN_DEFAULT_PASSWORD: str = typer.Option(
        "81f4e99fd99fb97039cf755532ce2b98f308dc417c0ed6d34ba2b9f739a2e30d", prompt=True
    ),
) -> None:
    """アプリケーション起動に必要な設定ファイル（.env）を生成します。"""

    path = ".env"
    if os.path.exists(path):
        typer.echo(".envファイルがすでに存在します。")
        raise typer.Abort()

    obj = Env(
        POSTGRES_USER=POSTGRES_USER,
        POSTGRES_PASSWORD=POSTGRES_PASSWORD,
        POSTGRES_SERVER=POSTGRES_SERVER,
        POSTGRES_DB=POSTGRES_DB,
        PGADMIN_LISTEN_PORT=PGADMIN_LISTEN_PORT,
        PGADMIN_DEFAULT_EMAIL=PGADMIN_DEFAULT_EMAIL,
        PGADMIN_DEFAULT_PASSWORD=PGADMIN_DEFAULT_PASSWORD,
    )

    with open(path, mode="w") as f:
        f.write(obj.to_env_file_str())

    typer.echo(f"Generated {path}")


@conf.command()
def show() -> None:
    """設定を表示します。"""

    obj = Env()
    typer.echo(obj)


@db.command()
def create() -> None:
    """データベースを作成します。"""
    from src import db

    db.create_db()


@db.command()
def drop() -> None:
    """データベースを削除します。"""
    from src import db

    db.drop_db()


if __name__ == "__main__":
    app()
