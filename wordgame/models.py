import re

VERSION = '1.0.0'

WORD_DELIMITER = '\n'
RGX_VERSION = re.compile(r'^@version (\d+\.\d+\.\d+)$')
RGX_ENTRY = re.compile(r'^(.+), (der|die|das)')
RGX_LIST_ITEM = re.compile(r'^- (.+)')
RGX_KEY_STR_VALUE = re.compile(r'$(.+): (.+)^')
RGX_KEY_LIST_VALUE = re.compile('^ex:$')
RGX_EX = 'ex:'

ACTION_ADD_EX = 'add-ex'

class Word(object):
    def __init__(self, text=None, category=None, gender=None):
        self.text = text
        self.category = category
        self.gender = gender
        self.examples = []

    def __str__(self):
        return 'word({} {})'.format(self.gender, self.text)


class Game(object):
    def __init__(self):
        self.words = []
        self.results = []

    def add_word(self, word):
        self.words.append(word)

    def collect_result(self, word_text, correct):
        self.results.append((word_text, correct))

    @staticmethod
    def parse_line(line):
        match = RGX_LIST_ITEM.match(line)

        if match is not None:
            return {
                'type': 'LIST_ITEM',
                'value': match[1]
            }
        else:
            match = RGX_ENTRY.match(line)
            if match is not None:
                word = Word()
                word.text = match[1]
                word.gender = match[2]
                return {
                    'type': 'NEW_ENTRY',
                    'value': word
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

        return game
