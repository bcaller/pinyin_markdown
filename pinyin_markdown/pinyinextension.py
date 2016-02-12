from markdown.extensions import Extension
from markdown.inlinepatterns import Pattern
from markdown.treeprocessors import Treeprocessor
from markdown.util import etree
from pinyin_markdown import pinyin_regex, numbered_accented

JUNK_TAG = "junkpinyinmd"


# Seriously there must be a better way of adding multiple
class RemoveJunkParentTreeprocessor(Treeprocessor):
    """Removes the <junkpinyinmd> tag and puts the pinyin <span>s under the parent <p>"""

    def run(self, root: etree.Element):
        junk_parents = root.findall('.//{}/..'.format(JUNK_TAG))
        for parent in junk_parents:
            i = 0
            while i < len(parent):
                junk = parent[i]
                if junk.tag == JUNK_TAG:
                    parent.remove(junk)
                    last = True
                    for accented_span in reversed(junk):
                        parent.insert(i, accented_span)
                        if last:
                            accented_span.tail = junk.tail  # Remainder of surrounding <p>
                            last = False
                i += 1


class NumberedPinyinPattern(Pattern):
    def __init__(self, *args, **kwargs):
        tone_cls = kwargs.pop('tone_class')
        self.tone_class = (lambda tone: tone_cls.format(tone)) if tone_cls is not None else lambda x: None
        self.erhua_class = kwargs.pop('erhua_class')
        self.apostrophe_class = kwargs.pop('apostrophe_class')
        self.entities = kwargs.pop('entities')
        super(NumberedPinyinPattern, self).__init__(*args, **kwargs)

    @staticmethod
    def make_span(parent, text, cls):
        span = etree.SubElement(parent, "span")
        span.text = text
        if cls is not None and len(cls) > 0:
            span.attrib = {"class": cls}
        return span

    @staticmethod
    def convert_to_entities(accented):
        for c in accented:
            if ord(c) > 122:  # Z is 122
                return accented.replace(c, '&#{};'.format(ord(c)))
        return accented

    def handleMatch(self, m):
        """
        Makes an ElementTree for the discovered Pinyin syllables.
        The root element holding all syllables is <junkpinyinmd>, which is removed by RemoveJunkParentTreeprocessor
        Converts Xi3ban4 to <junkpinyinmd><span class="tone3">Xǐ</span><span class="tone4">bàn</span></junkpinyinmd>
        :param m: polysyllabic_chinese_word = m.group(2)
        :return: etree
        """

        polysyllabic_chinese_word = m.group(2)
        parent = etree.Element(JUNK_TAG)
        for i, sound in enumerate(pinyin_regex.split_syllables(polysyllabic_chinese_word)):
            if sound == 'r':
                self.make_span(parent, 'r', self.erhua_class)
            else:
                if i > 0 and sound[0] in 'aeo':
                    self.make_span(parent, "'", self.apostrophe_class)
                accented = numbered_accented.numbered_syllable_to_accented(sound)
                if accented == sound:
                    raise Exception("Pinyin conversion error: " + sound)
                if self.entities:
                    accented = self.convert_to_entities(accented)
                self.make_span(parent, accented, self.tone_class(sound[-1]))
        return parent


class PinyinExtension(Extension):
    def __init__(self, *args, **kwargs):
        """Initialize."""

        self.config = {
            'tone_class': ['tone{}', "HTML class name for tones, which will be formatted with tone_class.format(tone)"
                                     "where tone is a number [1-5]"
                                     "May be empty"
                                     " - Default: 'tone{}'"],
            'erhua_class': ['erhua', "HTML class name for the erhua 'r' e.g. in dianr"
                                     "May be empty"
                                     " - Default: 'erhua"],
            'apostrophe_class': ['pyap', "HTML class name for apostrophes needed between vowels"
                                         "e.g. xi3an4 => xi3an4"
                                         "May be empty"
                                         " - Default: pyap"],
            'entities': [False, "If True, output the accented characters as entity codes"
                                " like &#466;"
                                " - Default: False"]
        }

        super(PinyinExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        pinyin_pattern = NumberedPinyinPattern(pinyin_regex.POLYSYLLABIC_REGEX_STR, **self.getConfigs())
        md.inlinePatterns.add('pinyin', pinyin_pattern, '_end')
        md.treeprocessors.add('pinyin_remove_junk', RemoveJunkParentTreeprocessor(md), '_end')


def makeExtension(*args, **kwargs):
    return PinyinExtension(*args, **kwargs)
