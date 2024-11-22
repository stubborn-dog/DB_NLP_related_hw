import sqlite3
import pymorphy3
from FileManager import FileManager as fm
from TextPreprocessor import TextPreprocesser as tp


morph = pymorphy3.MorphAnalyzer(lang='uk')

conn = sqlite3.connect('words.db')
cursor = conn.cursor()

corpus = fm('corpus.txt').read_file()
clean_corpus = tp(corpus).get_normalised_text()


def add_inflection_type(inflection_type):
    cursor.execute('SELECT inflection_type FROM inflection_types WHERE inflection_type = ?', (inflection_type,))
    if cursor.fetchone() is None:
        cursor.execute('INSERT INTO inflection_types (inflection_type) VALUES (?)', (inflection_type,))


def add_inflection(word_id, inflected_form, inflected_type):
    cursor.execute(
        '''
        INSERT INTO inflections (word_id, inflected_form, inflected_type)
        VALUES (?, ?, ?)
        ''',
        (word_id, inflected_form, inflected_type),
    )


words = clean_corpus.split()
for word in words:
    if not word.isalpha():
        continue

    parsed = morph.parse(word)[0]
    normal_form = parsed.normal_form
    pos_type = parsed.tag.POS
    if pos_type is None:
        continue

    cursor.execute(
        '''
        INSERT INTO words (meaning, pos_type, spelling)
        VALUES (?, ?, ?)
        ''',
        (f"Слово: {normal_form}", pos_type, word),
    )
    word_id = cursor.lastrowid

    for form in parsed.lexeme:
        inflected_form = form.word
        inflected_type = form.tag.cyr_repr
        add_inflection(word_id, inflected_form, inflected_type)

        inflection_features = inflected_type.split(", ")
        for feature in inflection_features:
            add_inflection_type(feature)

conn.commit()
conn.close()


