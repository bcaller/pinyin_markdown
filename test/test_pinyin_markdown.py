# coding: utf-8
from __future__ import unicode_literals

from collections import namedtuple

import pytest
from markdown import Markdown
from pinyin_markdown import PinyinExtension, pinyin_regex
from .expected import md_html, numbered_accented


class MarkdownTest(namedtuple('MarkdownTest', 'md html')):
    """Checks that the md parameter is converted to the html parameter surrounded by a <p> tag"""

    def __call__(self, markdown):
        return markdown.convert(self.md) == '<p>{}</p>'.format(self.html)


@pytest.fixture(params=[PinyinExtension(), 'pinyin_markdown'],
                ids=["import", "str"])
def pinyin_markdown(request):
    return Markdown(extensions=[request.param])


@pytest.fixture
def pinyin_md_no_classes():
    return Markdown(extensions=['pinyin_markdown(tone_class=,erhua_class=,apostrophe_class=)'])


@pytest.fixture
def pinyin_md_entities():
    return Markdown(extensions=['pinyin_markdown(entities=True)'])


@pytest.fixture(params=["hello", "fanian", "fa xing4qi you", "NI3HAO3"])
def pass_through_test(request):
    return MarkdownTest(request.param, request.param)


@pytest.fixture(params=md_html, ids=[test[0][:10] for test in md_html])
def md_test(request):
    return MarkdownTest(*request.param)


def test_pass_through(pinyin_markdown, pass_through_test):
    assert pass_through_test(pinyin_markdown)


def test_not_passed_through(pinyin_markdown, md_test):
    assert not pinyin_markdown.convert(md_test.md) == '<p>{}</p>'.format(md_test.md)


def test_md(pinyin_markdown, md_test):
    assert md_test(pinyin_markdown)


def test_conversion(pinyin_md_no_classes):
    for numbered, accented in numbered_accented.items():
        assert MarkdownTest(numbered, '<span>{}</span>'.format(accented))(pinyin_md_no_classes)


def test_conversion_neutral(pinyin_markdown):
    for syllable in pinyin_regex.SYLLABLES:
        assert MarkdownTest(syllable + '5', '<span class="tone5">{}</span>'.format(syllable))(pinyin_markdown)


def test_no_classes(pinyin_md_no_classes):
    assert MarkdownTest('lu:5', '<span>lü</span>')(pinyin_md_no_classes)
    assert MarkdownTest('yi1dian3r', '<span>yī</span><span>diǎn</span><span>r</span>')(pinyin_md_no_classes)


def test_entities(pinyin_md_entities):
    assert MarkdownTest('lu:5', '<span class="tone5">l&#252;</span>')(pinyin_md_entities)
    assert MarkdownTest('yi1dian3',
                        '<span class="tone1">y&#299;</span><span class="tone3">di&#462;n</span>')(pinyin_md_entities)


def test_fenced_code_unaffected(pinyin_markdown):
    assert MarkdownTest('x `li3 li2 li1` y', 'x <code>li3 li2 li1</code> y')(pinyin_markdown)


def test_urls_unaffected(pinyin_markdown):
    assert MarkdownTest('http://x.com/wo3 [wo3](http://x.com/wo3)',
                        'http://x.com/<span class="tone3">wǒ</span> '
                        '<a href="http://x.com/wo3"><span class="tone3">wǒ</span></a>')(pinyin_markdown)
