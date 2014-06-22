# -*- coding: utf-8 -*-
"""abydos.phones

The phones module implements ...


Copyright 2014 by Christopher C. Little.
This file is part of Abydos.

Abydos is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Abydos is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Abydos. If not, see <http://www.gnu.org/licenses/>.
"""

from __future__ import unicode_literals
from ._compat import _unicode
import unicodedata


PHONETIC_FEATURES = {'t': 0b0110101000010110100000000010001010101010101010,
                     'd': 0b0110101000010110100000000010000110101010101010,
                     's': 0b0110101000010110100000000010001010100101101010,
                     'z': 0b0110101000010110100000000010000110100101101010,
                     'ɬ': 0b0110101000010110100000000010001001100110011010,
                     'ɮ': 0b0110101000010110100000000010000110100110011010,
                     'θ': 0b0110101000010110100000000010001010100110101010,
                     'ð': 0b0110101000010110100000000010000110100110101010,
                     'ʃ': 0b0110101000011001100000000010001010100101101010,
                     'ʒ': 0b0110101000011001100000000010000110100101101010,
                     'c': 0b0110101000011001010110101010001010101010101010,
                     'ɟ': 0b0110101000011001010110101010000110101010101010,
                     'ç': 0b0110101000011001010110101010001010100110101010,
                     'ʝ': 0b0110101000011001010110101010000110100110101010,
                     'p': 0b0110100110100000100000000010001010101010101010,
                     'b': 0b0110100110100000100000000010000110101010101010,
                     'f': 0b0110100110100000100000000010001010100110101010,
                     'v': 0b0110100110100000100000000010000110100110101010,
                     'ɸ': 0b0110100110100000100000000010001010100110101010,
                     'β': 0b0110100110100000100000000010000110100110101010,
                     'k': 0b0110101000100000010110011010001010101010101010,
                     'g': 0b0110101000100000010110011010000110101010101010,
                     'x': 0b0110101000100000010110011010001010100110101010,
                     'ɣ': 0b0110101000100000010110011010000110100110101010,
                     'q': 0b0110101000100000011010011010001010101010101010,
                     'ɢ': 0b0110101000100000011010011010000110101010101010,
                     'χ': 0b0110101000100000011010011010001010100110101010,
                     'ʁ': 0b0110101000100000011010011010000110100110101010,
                     'ħ': 0b0110101000100000100000000001101010100110101010,
                     'ʕ': 0b0110101000100000100000000001101010100110101010,
                     'h': 0b1010101000100000100000000010001001100110101010,
                     'ɦ': 0b1010101000100000100000000010000101100110101010,
                     'ʔ': 0b1010101000100000100000000010001010011010101010,
                     'tʃ': 0b0110101000011001010110101010001010101001100110,
                     'dʒ': 0b0110101000011001010110101010000110101001100110,
                     'ts': 0b0110101000010110100000000010001010101001100110,
                     'dz': 0b0110101000010110100000000010000110101001100110,
                     'kx': 0b0110101000100000010110011010001010101010100110,
                     'pf': 0b0110100110100000100000000010001010101001100110,
                     'm': 0b0101100110100000100000000010000110101010101001,
                     'n': 0b0101101000010110100000000010000110101010101001,
                     'ŋ': 0b0101101000100000010110011010000110101010101001,
                     'ɳ': 0b0101101000011010011010101010000110101010101001,
                     'ɲ': 0b0101101000100000010110101010000110101010101001,
                     'ɴ': 0b0101101000100000011010011010000110101010101001,
                     'l': 0b0101101000010110100000000010000110100110011010,
                     'ʎ': 0b0101101000100000010110101010000110100110011010,
                     'r': 0b0101101000010110100000000010000110100110101010,
                     'ɹ': 0b0101101000010110100000000010000110100110101010,
                     'ʀ': 0b0101101000100000011010011010000110100110101010,
                     'j': 0b1001100110100000010110101010000110100110101010,
                     'w': 0b1001100101100000010110011010000110100110101010,
                     'ɥ': 0b1001100101100000010110101010000110100110101010,
                     'ɰ': 0b1001100110100000010110011010000110100110101010,
                     'i': 0b1001010110100000010110100101010110100110101010,
                     'ɪ': 0b1001010110100000010110101001100110100110101010,
                     'u': 0b1001010101100000010110010101010110100110101010,
                     'ʊ': 0b1001010101100000010110011001100110100110101010,
                     'e': 0b1001010110100000011010100101010110100110101010,
                     'ɛ': 0b1001010110100000011010101001100110100110101010,
                     'o': 0b1001010101100000011010010101010110100110101010,
                     'ɔ': 0b1001010101100000011010011001100110100110101010,
                     'a': 0b1001010110100000011001101001100110100110101010,
                     'æ': 0b1001010110100000011001100101100110100110101010,
                     'y': 0b1001010101100000010110100101010110100110101010,
                     'ʏ': 0b1001010101100000010110101001100110100110101010,
                     'ø': 0b1001010101100000011010100101010110100110101010,
                     'œ': 0b1001010110100000011010101001100110100110101010,
                     'ə': 0b1001010101100000011010011001100110100110101010,
                     'ɯ': 0b1001010101100000010110010101100110100110101010,
                     'kw': 0b0110100101100000010110011010001010101010101010,
                     'gw': 0b0110100101100000010110011010000110101010101010}

FEATURE_MASK = {'consonantal': 0b1100000000000000000000000000000000000000000000,
                'sonorant': 0b0011000000000000000000000000000000000000000000,
                'syllabic': 0b0000110000000000000000000000000000000000000000,
                'labial': 0b0000001100000000000000000000000000000000000000,
                'round': 0b0000000011000000000000000000000000000000000000,
                'coronal': 0b0000000000110000000000000000000000000000000000,
                'anterior': 0b0000000000001100000000000000000000000000000000,
                'distributed': 0b0000000000000011000000000000000000000000000000,
                'dorsal': 0b0000000000000000110000000000000000000000000000,
                'high': 0b0000000000000000001100000000000000000000000000,
                'low': 0b0000000000000000000011000000000000000000000000,
                'back': 0b0000000000000000000000110000000000000000000000,
                'tense': 0b0000000000000000000000001100000000000000000000,
                'pharyngeal': 0b0000000000000000000000000011000000000000000000,
                'ATR': 0b0000000000000000000000000000110000000000000000,
                'voice': 0b0000000000000000000000000000001100000000000000,
                'spread_glottis':
                0b0000000000000000000000000000000011000000000000,
                'constricted_glottis':
                0b0000000000000000000000000000000000110000000000,
                'continuant': 0b0000000000000000000000000000000000001100000000,
                'strident': 0b0000000000000000000000000000000000000011000000,
                'lateral': 0b0000000000000000000000000000000000000000110000,
                'delayed_release':
                0b0000000000000000000000000000000000000000001100,
                'nasal': 0b0000000000000000000000000000000000000000000011}


def ipa_to_features(ipa):
    """Return the feature representation (as a list of ints) of one or more
    phones

    Arguments:
    ipa -- the IPA representation of a phone or series of phones
    """
    features = []
    pos = 0
    ipa = unicodedata.normalize('NFC', _unicode(ipa.lower()))

    while pos < len(ipa):
        if pos+2 <= len(ipa) and ipa[pos:pos+3] in PHONETIC_FEATURES:
            features.append(PHONETIC_FEATURES[ipa[pos:pos+3]])
            pos += 3
        elif pos+1 <= len(ipa) and ipa[pos:pos+2] in PHONETIC_FEATURES:
            features.append(PHONETIC_FEATURES[ipa[pos:pos+2]])
            pos += 2
        elif ipa[pos] in PHONETIC_FEATURES:
            features.append(PHONETIC_FEATURES[ipa[pos]])
            pos += 1
        else:
            features.append(-1)
            pos += 1

    return features

def has_feature(vector, feature, binary=False):
    """Returns a list of ints representing presents/absence/neutrality with
    respect to a particular phonetic feature

    Arguments:
    vector -- a tuple or list of ints representing the phonetic features of a
        phone (such as is returned by the ipa_to_features function
    feature -- a feature name from the set:
        'consonantal', 'sonorant', 'syllabic', 'labial', 'round', 'coronal',
        'anterior', 'distributed', 'dorsal', 'high', 'low', 'back', 'tense',
        'pharyngeal', 'ATR', 'voice', 'spread_glottis', 'constricted_glottis',
        'continuant', 'strident', 'lateral', 'delayed_release', 'nasal'
    binary -- if False, -1, 0, & 1 represent -, 0, & +
              if True, only binary oppositions are allowed:
              0 & 1 represent - & + and 0s are mapped to -
    """
    if feature not in FEATURE_MASK:
        raise AttributeError("feature must be one of: 'consonantal', \
'sonorant', 'syllabic', 'labial', 'round', 'coronal', 'anterior', \
'distributed', 'dorsal', 'high', 'low', 'back', 'tense', 'pharyngeal', 'ATR', \
'voice', 'spread_glottis', 'constricted_glottis', 'continuant', 'strident', \
'lateral', 'delayed_release', 'nasal'")

    # each feature mask contains two bits, one each for - and +
    mask = FEATURE_MASK[feature]
    # the lower bit represents +
    pos_mask = mask >> 1
    retvec = []
    for char in vector:
        if char < 0:
            retvec.append(float('NaN'))
        else:
            masked = char & mask
            if not masked:
                retvec.append(0) # 0
            elif masked & pos_mask:
                retvec.append(1) # +
            elif binary:
                retvec.append(0) # -
            else:
                retvec.append(-1) # -

    return retvec