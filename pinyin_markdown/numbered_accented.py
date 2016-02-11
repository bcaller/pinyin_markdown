# Grabbed from https://github.com/tsroten/zhon
import re


VOWELS = 'aeiouv\u00FC'
VOWEL_MAP = {
    'a1': '\u0101', 'a2': '\xe1', 'a3': '\u01ce', 'a4': '\xe0', 'a5': 'a',
    'e1': '\u0113', 'e2': '\xe9', 'e3': '\u011b', 'e4': '\xe8', 'e5': 'e',
    'i1': '\u012b', 'i2': '\xed', 'i3': '\u01d0', 'i4': '\xec', 'i5': 'i',
    'o1': '\u014d', 'o2': '\xf3', 'o3': '\u01d2', 'o4': '\xf2', 'o5': 'o',
    'u1': '\u016b', 'u2': '\xfa', 'u3': '\u01d4', 'u4': '\xf9', 'u5': 'u',
    '\u00fc1': '\u01d6', '\u00fc2': '\u01d8', '\u00fc3': '\u01da',
    '\u00fc4': '\u01dc', '\u00fc5': '\u00fc'
}


def _num_vowel_to_acc(vowel, tone):
    """Convert a numbered vowel to an accented vowel."""
    try:
        return VOWEL_MAP[vowel + str(tone)]
    except IndexError:
        raise ValueError("Vowel must be one of '{}' and tone must be a tone.".format(VOWELS))


def numbered_syllable_to_accented(syllable):
    """Convert a numbered pinyin syllable to an accented pinyin syllable.

    Implements the following algorithm, modified from https://github.com/tsroten/zhon:
        1. If the syllable has an 'a' or 'e', put the tone over that vowel.
        2. If the syllable has 'ou', place the tone over the 'o'.
        3. Otherwise, put the tone on the last vowel.

    """
    def keep_case_replace(s, vowel, replacement):
        accented = s.replace(vowel, replacement)
        if syllable[0].isupper():
            return accented[0].upper() + accented[1:]
        return accented

    tone = syllable[-1]
    if tone == '5':
        return re.sub('u:|v', '\u00fc', syllable[:-1])
    # Homogenise representation of u:
    syl = re.sub('u:|v', '\u00fc', syllable[:-1].lower())
    if 'a' in syl:
        return keep_case_replace(syl, 'a', _num_vowel_to_acc('a', tone))
    elif 'e' in syl:
        return keep_case_replace(syl, 'e', _num_vowel_to_acc('e', tone))
    elif 'ou' in syl:
        return keep_case_replace(syl, 'o', _num_vowel_to_acc('o', tone))
    last_vowel = syl[max(map(syl.rfind, VOWELS))]  # Find last vowel index.
    return keep_case_replace(syl, last_vowel, _num_vowel_to_acc(last_vowel, tone))
