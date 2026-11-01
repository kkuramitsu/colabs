# 関数やクラスのソースコード(プログラムの中身)を表示する。
#
# inspect は Python に最初から入っている標準ライブラリで、
# 関数やクラスの情報(ソースコードなど)を調べるために使う。
import inspect


def source(obj):
    """関数やクラス obj のソースコードを表示する。

    使い方:
        from colabs import source, show_chars
        source(show_chars)

    注意: () を付けずに、関数そのものを渡す。
        source(show_chars)    # 正しい
        source(show_chars())  # 間違い(関数を実行した結果を渡してしまう)
    """
    try:
        # getsource は、関数のソースコードを文字列で返す
        code = inspect.getsource(obj)
    except (TypeError, OSError):
        # print や len のような Python 本体の組み込み関数は、
        # ソースコードが Python で書かれていないため取得できない。
        # try / except でエラーを受け止めて、分かりやすいメッセージを出す。
        print(f"ソースコードを取得できませんでした: {obj!r}")
        return

    print(code)
