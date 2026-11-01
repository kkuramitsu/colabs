# colabs

授業の演習用に関数を定義するパッケージ。

## インストール

ターミナルの場合:

```
pip install git+https://github.com/kkuramitsu/colabs.git
```

Google Colab / Jupyter の場合は、セルの先頭に `!` を付けます。

```
!pip install git+https://github.com/kkuramitsu/colabs.git
```

### 更新する

```
pip install --upgrade git+https://github.com/kkuramitsu/colabs.git
```

Colab では、更新後に「ランタイム → セッションを再起動」が必要になる場合があります。

### バージョンを指定する

タグ(例: `v0.1.0`)を指定すると、そのバージョンに固定できます。

```
pip install git+https://github.com/kkuramitsu/colabs.git@v0.1.0
```

## 使い方

```python
from colabs import func

func(3)  # 6
```

## 収録している関数

| 関数 | 説明 |
|---|---|
| `func(x)` | 受け取った値を2倍にして返す(サンプル) |
| `show_chars(text)` | 文字列を1文字ずつ分解し、Unicode コードポイント・UTF-8 バイト列・カテゴリ・文字名を表示する |

## 構成

```
colabs/
├── pyproject.toml      # パッケージ定義
├── README.md
└── colabs/
    ├── __init__.py     # 公開する関数を import する
    ├── exercises.py    # 演習用の関数
    └── chars.py        # 文字コード関連(show_chars)
```

## 関数の追加方法(教員向け)

1. `colabs/exercises.py` に関数を書く。
2. `colabs/__init__.py` で import し、`__all__` に加える。

   ```python
   from .exercises import func, new_func

   __all__ = ["func", "new_func"]
   ```

3. 上の表に関数を追記し、必要なら `pyproject.toml` の `version` を上げる。
4. commit して push する。

手元で動作を確認するには、リポジトリのフォルダで次を実行します。

```
pip install -e .
```

## 注意

- リポジトリが private だと、URL だけではインストールできません。授業で配布する場合は public にしてください。

## ライセンス

[LICENSE](LICENSE) を参照してください。
