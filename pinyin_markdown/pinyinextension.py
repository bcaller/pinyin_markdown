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


def make_span(parent, text, cls):
    span = etree.SubElement(parent, "span")
    span.text = text
    if cls is not None and len(cls) > 0:
        span.attrib = {"class": cls}
    return span


class NumberedPinyinPattern(Pattern):
    def __init__(self, *args, **kwargs):
        _tone_class = kwargs.pop('tone_class')
        self.tone_class = (lambda tone: _tone_class.format(tone)) if _tone_class is not None else lambda x: None
        self.erhua_class = kwargs.pop('erhua_class')
        self.apostrophe_class = kwargs.pop('apostrophe_class')
        super(NumberedPinyinPattern, self).__init__(*args, **kwargs)

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
                make_span(parent, 'r', self.erhua_class)
            else:
                if i > 0 and sound[0] in 'aeo':
                    make_span(parent, "'", self.apostrophe_class)
                accented = numbered_accented.numbered_syllable_to_accented(sound)
                if accented == sound:
                    raise Exception("Pinyin conversion error: " + sound)
                make_span(parent, accented, self.tone_class(sound[-1]))
        return parent


class PinyinExtension(Extension):
    def __init__(self, *args, **kwargs):
        """Initialize."""

        self.config = {
            'tone_class': ['tone{}', "HTML class name for tones, which will be formatted with tone_class.format(tone)"
                                     "May be empty"
                                     "where tone is a number [1-5]"
                                     " - Default: True"],
            'erhua_class': ['erhua', "Class for the erhua (r in dian3r)"
                                     "May be empty"
                                     " - Default: 'erhua"],
            'apostrophe_class': ['pyap', "Class for apostrophe inserted between vowels"
                                         "e.g. xi3an4 => xi3an4"
                                         "May be empty"
                                         " - Default: pyap"]
        }

        super(PinyinExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        config = self.getConfigs()
        pinyin_pattern = NumberedPinyinPattern(pinyin_regex.POLYSYLLABIC_REGEX_STR,
                                               tone_class=config.get('tone_class', 'tone{}'),
                                               erhua_class=config.get('erhua_class', 'erhua'),
                                               apostrophe_class=config.get('apostrophe_class', 'pyap'))
        md.inlinePatterns.add('pinyin', pinyin_pattern, '_begin')
        md.treeprocessors.add('pinyin_remove_junk', RemoveJunkParentTreeprocessor(md), '_end')


def makeExtension(*args, **kwargs):
    return PinyinExtension(*args, **kwargs)
