import sqlite3

conn = sqlite3.connect('words.db')
cursor = conn.cursor()


cursor.execute('''
CREATE TABLE "words" (
    "word_id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "meaning" TEXT,
    "pos_type" TEXT,
    "examples" TEXT,
    "spelling" TEXT,
    FOREIGN KEY ("pos_type") REFERENCES "pos"("pos_type")
);
''')

cursor.execute('''
CREATE TABLE "pos" (
    "pos_type" TEXT PRIMARY KEY
);
''')


cursor.execute('''
CREATE TABLE "inflections" (
    "word_id" INTEGER,
    "inflected_form" TEXT,
    "inflected_type" TEXT,
    FOREIGN KEY ("word_id") REFERENCES "words"("word_id"),
    FOREIGN KEY ("inflected_type") REFERENCES "inflection_types"("inflection_type")
);
''')


cursor.execute('''
CREATE TABLE IF NOT EXISTS "inflection_types" (
    "inflection_type" TEXT PRIMARY KEY
);
''')
conn.commit()
conn.close()