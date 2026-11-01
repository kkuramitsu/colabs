# 日本語の文を単語(形態素)に分けて、品詞などを表示する。
# 形態素解析には外部ライブラリ janome と SudachiPy を使う。
from .install import require


def show_tokens_janome(text):
    """janome で text を形態素解析して、1語ずつ表示する。

    janome が入っていないときは、自動でインストールする。

    使い方:
        from colabs import show_tokens_janome
        show_tokens_janome("すもももももももものうち")
    """
    # janome がまだ入っていなければ、自動でインストールして読み込む
    Tokenizer = require("janome.tokenizer").Tokenizer

    # Tokenizer(単語に分けるもの)を作る
    t = Tokenizer()

    # 形態素解析の実行。結果は、1語ごとの情報(token)のリストになる。
    tokens = list(t.tokenize(text))

    print(f"トークン数: {len(tokens)}")
    for token in tokens:
        print(f"字句: {token.surface} / 品詞: {token.part_of_speech} / 原形: {token.base_form}")


def show_tokens_sudachi(text, mode="C"):
    """SudachiPy で text を形態素解析して、1語ずつ表示する。

    mode は単語の区切りの細かさ。
        "A": 最も短く区切る  "B": 中間  "C": 最も長く区切る(標準)
    SudachiPy が入っていないときは、自動でインストールする。

    使い方:
        from colabs import show_tokens_sudachi
        show_tokens_sudachi("国家公務員法", mode="A")
    """
    # SudachiPy がまだ入っていなければ、自動でインストールして読み込む。
    # SudachiPy は、辞書(sudachidict_core)も一緒に必要になる。
    dictionary = require("sudachipy.dictionary", "sudachipy sudachidict_core")
    tokenizer = require("sudachipy.tokenizer")

    # 区切りの細かさ(A/B/C)を、SudachiPy の指定に対応づける辞書
    modes = {
        "A": tokenizer.Tokenizer.SplitMode.A,
        "B": tokenizer.Tokenizer.SplitMode.B,
        "C": tokenizer.Tokenizer.SplitMode.C,
    }
    # 辞書にない指定(例: "X")のときは C にする。
    # modes.get(キー, 初期値) は、キーがなければ初期値を返す。
    split_mode = modes.get(mode, modes["C"])

    # 単語に分けるもの(tokenizer)を作って、形態素解析を実行する
    tokenizer_obj = dictionary.Dictionary().tokenizer()
    tokens = tokenizer_obj.tokenize(text, split_mode)

    print(f"分割モード: {mode}")
    print(f"トークン数: {len(tokens)}")
    for token in tokens:
        pos = ",".join(token.part_of_speech())
        print(f"字句: {token.surface()} / 品詞: {pos} / 原形: {token.dictionary_form()}")
