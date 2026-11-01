# 文字列を1文字ずつ分解して、文字コードなどの情報を表にして表示する。
#
# unicodedata は Python に最初から入っている標準ライブラリで、
# 文字の名前やカテゴリ(種類)を調べるために使う。
import unicodedata


# ---------------------------------------------------------------
# 表をきれいに揃えるための補助関数
# (関数名の先頭の _ は「このファイルの内部用」という目印)
# ---------------------------------------------------------------

def _width(s: str) -> int:
    """画面に表示したときの幅を返す。

    len(s) は「文字の数」だが、日本語(全角)は画面上で半角の2文字分の
    幅をとる。表の縦線 | を揃えるには、文字数ではなく表示幅が必要。
      半角(A, 1 など) -> 幅 1
      全角(あ, 漢, 絵文字など) -> 幅 2
      結合文字(濁点だけの文字など) -> 幅 0
    """
    w = 0
    for ch in s:
        # 結合文字は直前の文字に重ねて表示されるので、幅に数えない
        if unicodedata.combining(ch) or unicodedata.category(ch) in ('Mn', 'Me'):
            continue
        # east_asian_width が 'W'(Wide) か 'F'(Fullwidth) なら全角扱い
        w += 2 if unicodedata.east_asian_width(ch) in ('W', 'F') else 1
    return w


def _ljust(s: str, width: int) -> str:
    """表示幅が width になるまで、右側に空白を足して左寄せにする。"""
    # max(0, ...) は、すでに幅を超えているときに空白が負にならないようにする
    return s + ' ' * max(0, width - _width(s))


def _center(s: str, width: int) -> str:
    """表示幅が width になるまで、左右に空白を足して中央寄せにする。"""
    pad = max(0, width - _width(s))  # 足りない空白の合計
    left = pad // 2                  # 左に入れる分(// は切り捨ての割り算)
    return ' ' * left + s + ' ' * (pad - left)


# ---------------------------------------------------------------
# メインの関数
# ---------------------------------------------------------------

def show_chars(text: str):
    """text の文字を1文字ずつ、表にして表示する。

    使い方:
        from colabs import show_chars
        show_chars("Aあ😀")
    """
    # 各列の幅(表示幅で数える)
    w_char, w_cp, w_hex, w_len, w_cat = 24, 8, 15, 8, 10

    # 1行ぶんを表示する関数。ヘッダーも各文字も同じ形式で出すために使う。
    # *cols は「引数をいくつでも受け取ってタプルにまとめる」書き方。
    def row(*cols):
        c, cp, hx, ln, cat, name = cols  # 6つの値を名前を付けて取り出す
        # 各列を幅に合わせて整え、' | ' でつないで1行にする
        print(' | '.join([
            _ljust(c, w_char), _ljust(cp, w_cp), _ljust(hx, w_hex),
            _center(ln, w_len), _ljust(cat, w_cat), name,
        ]))

    # 表の見出しと区切り線
    row('文字 (可視化)', 'Unicode', 'UTF-8 (16進数)', 'バイト数', 'カテゴリ', '文字名 / 種類')
    print('-' * 110)

    # 改行やスペースは、そのまま表示すると何も見えない。
    # そこで「見える言葉」に置き換えるための辞書(キー: 文字, 値: 表示する文字列)。
    # '\n' のような書き方は「エスケープシーケンス」と呼び、特殊な文字を表す。
    # '　' は「Unicode 番号 3000 の文字」という意味。
    visible_map = {
        '\n': '[改行 LF]',
        '\r': '[改行 CR]',
        '\t': '[タブ HT]',
        ' ': '[半角スペース]',
        '　': '[全角スペース]',
        '​': '[ゼロ幅スペース(ZWSP)]',
        '‌': '[ゼロ幅非接合子(ZWNJ)]',
        '‍': '[ゼロ幅接合子(ZWJ)]',
        '﻿': '[BOM / ZWNBSP]',
    }

    # 文字列は for で回すと、1文字ずつ取り出せる
    for char in text:
        # ord() で文字を番号(コードポイント)に変換する。例: 'A' -> 65
        codepoint = ord(char)
        # f"U+{...:04X}" は、番号を16進数(大文字)で4桁以上にそろえる書式。例: U+0041
        formatted_cp = f"U+{codepoint:04X}"

        # UTF-8 は、文字をバイト(0〜255の数)の列に変える方式。
        # 文字によってバイト数が違う(英数字は1、ひらがなは3、絵文字は4など)。
        utf8_bytes = char.encode('utf-8')
        byte_length = len(utf8_bytes)  # バイト数
        # 各バイトを16進数2桁にして、スペース区切りでつなぐ。例: E3 81 82
        hex_bytes = ' '.join(f'{b:02X}' for b in utf8_bytes)

        # カテゴリ(文字の種類)を2文字の記号で取得する。
        # 例: Lu=大文字, Ll=小文字, Lo=ひらがな・漢字など,
        #     Zs=スペース, Cc=制御文字, So=記号・絵文字
        category = unicodedata.category(char)

        # 文字の正式名称を取得する。
        # 名前のない文字(制御文字など)ではエラー(ValueError)になるので、
        # try / except でエラーを受け止めて、代わりの文字列を使う。
        try:
            name = unicodedata.name(char)
        except ValueError:
            name = "(名前なし/制御文字等)"

        # 画面に表示する文字を決める。
        # 辞書にあれば置き換え後の文字列、なければ文字そのまま。
        display_char = visible_map.get(char, char)
        # カテゴリが C で始まるのは制御文字(画面に見えない文字)。
        # 辞書にないものは、番号つきの表示にする。
        if category.startswith('C') and char not in visible_map:
            display_char = f"[制御文字 0x{codepoint:02X}]"

        # 1文字ぶんの情報を表の1行として表示する
        row(display_char, formatted_cp, hex_bytes, str(byte_length), category, name)
