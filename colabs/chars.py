# 文字列を1文字ずつ分解して、文字コードなどの情報を表示する。


def show_chars(text):
    """text の文字数と、1文字ずつの情報を表示する。

    使い方:
        from colabs import show_chars
        show_chars("Aあ\n")
    """
    # len() で文字の数を調べる
    print(f"文字数: {len(text)}")

    # 文字列は for で回すと、1文字ずつ取り出せる
    for char in text:
        # repr() は、見えない文字を \n や 　 のような
        # エスケープ表記にして、'' で囲んだ文字列にする。
        # 例: 改行 -> '\n'、全角スペース -> '　'
        visible = repr(char)

        # ord() で文字を番号(コードポイント)に変換する。例: 'A' -> 65
        # :04X は、16進数(大文字)で4桁以上にそろえる書式。例: U+0041
        code_point = f"U+{ord(char):04X}"

        # UTF-8 は、文字をバイト(0〜255の数)の列に変える方式。
        # 文字によってバイト数が違う(英数字は1、ひらがなは3、絵文字は4など)。
        data = char.encode("utf-8")

        # 各バイトを16進数2桁にして、スペースでつなぐ。例: E3 81 82
        hex_bytes = " ".join(f"{b:02X}" for b in data)

        print(f"{visible}  {code_point}  {hex_bytes}  {len(data)}バイト")
