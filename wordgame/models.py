import re
from collections import defaultdict

VERSION = '1.0.0'

WORD_DELIMITER = '\n'
RGX_VERSION = re.compile(r'^@version (\d+\.\d+\.\d+)$')
RGX_ENTRY_NOUN = re.compile(r'^(?P<noun>.+) \(n\), (der|die|das)')
RGX_ENTRY_VERB = re.compile(r'^(?P<verb>.+) \(v\)(?:, (sich))?')
RGX_LIST_ITEM = re.compile(r'^- (.+)')
RGX_KEY_STR_VALUE = re.compile(r'^(?P<key>.+): (?P<value>.+)$')
RGX_KEY_LIST_VALUE = re.compile('^ex:$')
RGX_EX = 'ex:'

ACTION_ADD_EX = 'add-ex'

class Word(object):
    def __init__(self, text=None, category=None, *,
                 meaning=None,
                 gender=None,
                 reflexive=None):
        self.text = text
        self.category = category
        self.gender = gender
        self.reflexive = reflexive
        self.meaning = meaning
        self.particles = None
        self.examples = []

    def __str__(self):
        if self.category == 'noun':
            return '{} {}'.format(self.gender, self.text)
        elif self.category == 'verb':
            return '{} {}'.format(self.reflexive, self.text)
        else:
            return 'word({}, ({}))'.format(self.text, self.category)


class Game(object):
    def __init__(self):
        self.words = []
        self._results = defaultdict(int)

    def add_word(self, word):
        self.words.append(word)

    def collect_result(self, word_text, correct):
        self._results[(word_text, correct)] += 1

    @property
    def results(self):
        return [(key[0], key[1], value) for (key, value) in  self._results.items()]

    @staticmethod
    def parse_line(line):
        match = RGX_LIST_ITEM.match(line)

        if match is not None:
            return {
                'type': 'LIST_ITEM',
                'value': match[1]
            }
        else:
            match = RGX_ENTRY_NOUN.match(line) or RGX_ENTRY_VERB.match(line)
            if match is not None:
                if 'noun' in match.groupdict():
                    word = Word(match.group('noun'), 'noun',
                                gender=match[2])
                elif 'verb' in match.groupdict():
                    word = Word(match.group('verb'), 'verb',
                                reflexive=match[2])
                else:
                    return None

                return {
                    'type': 'NEW_ENTRY',
                    'value': word
                }
            else:
                match = RGX_KEY_STR_VALUE.match(line.strip())
                if match is not None:
                    return {
                        'type': 'KEY_VALUE',
                        'key': match.group('key'),
                        'value': match.group('value')
                    }

                else:
                    match = RGX_VERSION.match(line)

                    if match is not None:
                        return {
                            'type': 'VERSION',
                            'value': match[1]
                        }
                    return None

    @staticmethod
    def load(filename):
        game = Game()
        word = None
        current_action = None

        with open(filename, 'r') as f:
            for line in f:
                if line == WORD_DELIMITER:
                    word = None
                    continue
                else:
                    result = Game.parse_line(line)
                    if result is None:
                        if line.strip() == RGX_EX:
                            current_action = 'add-ex'
                        continue
                    elif current_action == ACTION_ADD_EX:
                        if result['type'] == 'LIST_ITEM':
                            word.examples.append(result['value'])
                    if result['type'] == 'VERSION':
                        if VERSION != result['value']:
                            raise Exception('Invalid file version')
                    elif result['type'] == 'NEW_ENTRY':
                        word = result['value']
                        game.add_word(word)
                    elif result['type'] == 'KEY_VALUE':
                        key = result['key']
                        if key == 'mn':
                            word.meaning = result['value']
                        elif key == 'pt':
                            word.particles = tuple(map(lambda x: x.strip(), result['value'].split(',')))

        return game
