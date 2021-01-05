# FastAPI + Docker Template
FastAPI(Python) + DockerプロジェクトをVSCodeで開発するための雛形です。

# 何ができる？
- Dockerコンテナを用いた再現性が高い開発環境を提供します
- VSCodeプラグインを管理し、VSCodeのエディタ環境まで再現します
- リモート上でデバッグ（ブレークポイント）できます

# PyCharmは対応してますか？
できません（色々試しましたが、満足がいく環境を構築できず、また、再現手順も複雑なので断念しました）。

# 前提条件
検証環境は、ubuntu 20.04です。Mac、Windowsは動かないかもしれません。

開発を開始するために、次の作業が必要です。

- 開発ホストにDockerがインストールされていること
- VSCodeプラグインのRemote-Containersがインストールされていること


# 開発してみよう

## プロジェクトをクローンする

``` shell
git clone xxx
cd xxx
```

## ユーザー
コンテナはdeveloperユーザとしてログインされます。
ホストのユーザーをdeveloperグループに所属させ、権限を共有しましょう。

``` shell
sudo usermod -aG developer `whoami`
```

## 関連コンテナを立ち上げる
DBサーバと接続する場合など、予めコンテナを起動する必要があります。
本プロジェクトは、PostgreSQL + SqlAlchemyの構成でデータベースを取り扱います。

## リモート開発を開始する
1. `Crtl + Shift + P`でコマンドパレットを起動します。
2. `Remote-Containers: Reopen in Container`を選択します。


# 開発準備
1. VSCodeプラグインのRemote-Containersを導入する
2. docker-composeでAPIサーバとDBサーバのコンテナを立ち上げる
3. リモートコンテナでリモート開発を開始する
4. インタープリタを選択する
5. デバッグ構成
6. [openapi](http://localhost:8080/docs)


## フォーマッタ・静的コード解析ツールの動作確認

### isortの確認
main.pyを次のようなコードに修正し、保存してください。

``` Python
from fastapi import FastAPI

import datetime
import asyncio

app = FastAPI()
```

isortが動作していれば、標準ライブラリ->サードパーティライブラリの順にインポート順が修正されます。

### flake8の確認
main.pyを次のようなコードに修正し、保存してください。

``` Python
import asyncio
import datetime

from fastapi import FastAPI

app = FastAPI()
```

flake8が動作していれば、エディタ上にエラー（asyncioとdatetimeが未使用）が表示されます。
また、VSCodeの問題タブにもエラー箇所が出力され、クリックすると問題箇所にジャンプできます。

### blackの確認
main.pyの最後に次のようなコードを追加し、保存してください。

``` Python
def func1():
    ...




def func2():
    ...
```

blackが動作していれば、関数の間の空行を２行に統一してくれます。

### mypyの確認
main.pyの最後に次のようなコードを追加し、保存してください。

``` Python
num = 1


def func(name: str):
    ...


func(name=num)
```

mypyが動作していれば、エラー（想定している型と異なる）が表示されます。

### Kiteの確認
何かコードを入力し、インテリセンスにKiteの文字が出てくれば、Kiteが動作してます。


## デバッグ確認
main.pyに次のようなコードを仕込んであります。

``` Python
debugpy.listen(("0.0.0.0", 5678))
debugpy.wait_for_client()
```

`debugpy`は、VSCodeでPythonをデバッグするためのモジュールです。
`wait_for_client`でクライアントからの接続を待機し、VSCodeからデバッグ開始すると、`debugpy`と接続され、デバッグ（ブレークポイントの利用）可能な状態になります。

コードにブレークポイントを設定し、openapiからapiを実行すれば、ブレークポイントでプログラムが停止するので、試してみましょう。

## Kite Engineインストール
Kiteプラグイン自体には解析機能がついてないので、コンテナ上にKite Engineをインストールする必要がある。

[公式サイト](https://www.kite.com/download/)を参考に、コンテナ上にKite Engineをインストールする。

``` shell
bash -c "$(wget -q -O - https://linux.kite.com/dls/linux/current)"
```

KiteのProfessional版を利用する場合は、ログインが必要。
CUIモードでKite Engineをインストールした場合は、次のメッセージが表示されているはずなので、メッセージに従いログイン用のコマンドを実行する。

アカウントを持っていなくとも、フリーの範囲でなら動作する、はず。

```
No X11 or Wayland session was found.
Kite Copilot UI won't be launched after the installation.
To login, run this command in a terminal:
        ~/.local/share/kite/login-user
```

難点は、コンテナをビルドし直したら、再度インストール、ログインが必要。
Dockerfileに組み込んでしまうのも気が引ける。


# TODO: 1. __pycache__がdeveloper権限で作成されていること
# TODO: 2. poetry add時にグローバル環境にインストールされること　→　仮想環境を作成せず、デフォルトの検索パッケージ用フォルダに格納されるのでOK
# TODO: 3. jupyter notebookが動くこと
# TODO: 4. 定義へ移動ができること
