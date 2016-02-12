# coding: utf-8
from __future__ import unicode_literals

from collections import namedtuple

import pytest
from markdown import Markdown
from pinyin_markdown import PinyinExtension, pinyin_regex
from .expected import md_html, numbered_accented

MarkdownTest = namedtuple('MarkdownTest', 'md html')


@pytest.fixture(params=[PinyinExtension(), 'pinyin_markdown'],
                ids=["import", "str"])
def pinyin_markdown(request):
    return Markdown(extensions=[request.param])


@pytest.fixture(params=["hello", "fanian", "fa xing4qi you", "NI3HAO3"])
def pass_through(request):
    return request.param


@pytest.fixture(params=md_html, ids=[test[0][:10] for test in md_html])
def md_test(request):
    return MarkdownTest(*request.param)


def test_pass_through(pinyin_markdown, pass_through):
    assert pinyin_markdown.convert(pass_through) == '<p>{}</p>'.format(pass_through)


def test_not_passed_through(pinyin_markdown, md_test):
    assert not pinyin_markdown.convert(md_test.md) == '<p>{}</p>'.format(md_test.md)


def test_md(pinyin_markdown, md_test):
    assert pinyin_markdown.convert(md_test.md) == '<p>{}</p>'.format(md_test.html)


def test_conversion(pinyin_markdown):
    for numbered, accented in numbered_accented.items():
        assert accented in pinyin_markdown.convert(numbered)


def test_conversion_neutral(pinyin_markdown):
    for syllable in pinyin_regex.SYLLABLES:
        assert pinyin_markdown.convert(syllable + '5') == '<p><span class="tone5">{}</span></p>'.format(syllable)


def test_no_classes():
    pinyin_md_no_classes = Markdown(extensions=['pinyin_markdown(tone_class=,erhua_class=,entities=False)'])
    assert pinyin_md_no_classes.convert('lu:5') == '<p><span>lü</span></p>'
    assert pinyin_md_no_classes.convert('yi1dian3r') == '<p><span>yī</span><span>diǎn</span><span>r</span></p>'


def test_entities():
    pinyin_md_no_classes = Markdown(extensions=['pinyin_markdown(entities=True)'])
    assert pinyin_md_no_classes.convert('lu:5') == '<p><span class="tone5">l&#252;</span></p>'
    assert pinyin_md_no_classes.convert('yi1dian3') ==\
        '<p><span class="tone1">y&#299;</span><span class="tone3">di&#462;n</span></p>'
