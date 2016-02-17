# Pinyin and Python and Markdown, together!

Type Chinese pinyin with tone numbers, and have them automagically converted to beautiful accented pinyin.

[![travis](https://travis-ci.org/bcaller/pinyin_markdown.svg)](https://travis-ci.org/bcaller/pinyin_markdown)
[![PyPI version](https://badge.fury.io/py/pinyin_markdown.svg)](https://badge.fury.io/py/pinyin_markdown)

A Markdown extension that looks through your text for things like `yi1dian3r`, `Xi3an4` and `lu:5` and replaces
them with accented pinyin. The pinyin syllables are marked up with span tags with classes denoting
the tone.

Add `'pinyin_markdown'` to your Markdown call and watch the magic unfold:

```python
>>> from markdown import Markdown

>>> markdown = Markdown(extensions=['pinyin_markdown']
>>> markdown.convert('i ♥ Xi3an4!')
<p>i ♥ <span class="tone3">Xǐ</span><span class="pyap">'</span><span class="tone4">àn</span></p>

>>> markdown = Markdown(extensions=['pinyin_markdown(tone_class=, apostrophe_class=apo)']
>>> markdown.convert('i ♥ Xi3an4!')
<p>i ♥ <span>Xǐ</span><span class="apo">'</span><span>àn</span></p>
```

The three examples above are rendered as:  yīdiǎnr, Xǐ'àn and lü, with HTML:

```html
<span class="tone1">yī</span><span class="tone3">diǎn</span><span class="erhua">r</span>
<span class="tone3">Xǐ</span><span class="pyap">'</span><span class="tone4">àn</span>
<span class="tone5">lü</span>
```

## Options
| Option    | Type | Default |Description |
|-----------|------|---------|------------|
| tone_class | str | 'tone{}' | HTML class name for tones, which will be formatted with tone_class.format(tone) where tone is a number 1-5|
| apostrophe_class | str | 'pyap' | HTML class name for apostrophes needed between vowels |
| erhua_class | str | 'erhua' | HTML class name for the erhua 'r' e.g. in dianr |
| entities | bool | False | If True, output the accented characters as entity codes `&466#;` |


## Installation
From Github:

```
git clone https://github.com/bcaller/pinyin_markdown.git
pip install -e ./pinyin_markdown
```

From Pypi:

```
pip install pinyin_markdown
```

Also have a look at [tsroten's zhon](https://github.com/tsroten/zhon) for more Python pinyin goodness.
