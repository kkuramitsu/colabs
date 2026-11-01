"""授業の演習用関数集。

使い方:
    from colabs import func, show_chars, show_tokens_janome, show_tokens_sudachi, source
"""

from .exercises import func
from .chars import show_chars
from .morphology import show_tokens_janome, show_tokens_sudachi
from .source import source

__all__ = ["func", "show_chars", "show_tokens_janome", "show_tokens_sudachi", "source"]
