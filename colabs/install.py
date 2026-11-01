# 外部ライブラリを「なければ自動でインストールして」使うための共通関数。
import importlib
import os
import sys


def _in_notebook():
    """Jupyter / Colab のノートブックの中で動いているかを返す。"""
    try:
        from IPython import get_ipython
        shell = get_ipython()
        # ノートブックでは、shell が kernel(計算を担当する部分)を持っている
        return shell is not None and hasattr(shell, "kernel")
    except ImportError:
        return False


def require(module, pip_name=None):
    """module を import して返す。入っていなければ、pip でインストールする。

    module:   import したいモジュール名。例: "janome.tokenizer"
    pip_name: pip でインストールするときの名前(空白区切りで複数可)。
              省略すると、module の最初の部分(例: "janome")を使う。

    使い方:
        tokenizer = require("janome.tokenizer")
        Tokenizer = tokenizer.Tokenizer
    """
    # まずは普通に import してみる。入っていればここで終わり。
    # try / except ImportError は「import に失敗したとき」の処理を書く方法。
    try:
        return importlib.import_module(module)
    except ImportError:
        pass

    if pip_name is None:
        pip_name = module.split(".")[0]

    message = f"{pip_name} をインストールします..."
    if _in_notebook():
        # ノートブックでは、あとでこのメッセージだけを消せるように
        # 「表示の目印(display_id)」を付けて表示する。
        # (clear_output() だと、同じセルの前の出力まで全部消えてしまう)
        from IPython.display import display
        handle = display(message, display_id=True)
    else:
        print(message)
        handle = None

    # os.system() は、ターミナルのコマンドを実行する。
    # sys.executable は、今使っている Python の場所。
    # これを使うと、今の Python に確実にインストールできる。
    # -q は、pip のメッセージを少なくするオプション。
    os.system(f"{sys.executable} -m pip install -q --disable-pip-version-check {pip_name}")

    # インストールしたばかりのライブラリを見つけられるようにする
    importlib.invalidate_caches()

    # ノートブックなら、「インストールします...」のメッセージを消す
    if handle is not None:
        handle.update("")

    return importlib.import_module(module)
