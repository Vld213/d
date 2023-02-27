import sqlite3

db = sqlite3.connect('data.db')
cur = db.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS prefixes (
    prefix TEXT,
    guild_id INTEGER
)""")
db.commit()

cur.execute("""CREATE TABLE IF NOT EXISTS whitelist (
    guild_id INTEGER,
    user_id INTEGER,
    action TEXT
)""")
db.commit()

cur.execute("""CREATE TABLE IF NOT EXISTS antibot (
    guild_id INTEGER
)""")
db.commit()

cur.execute("""CREATE TABLE IF NOT EXISTS anticrash (
    guild_id INTEGER,
    action TEXT
)""")
db.commit()

cur.execute("""CREATE TABLE IF NOT EXISTS blacklist (
    user_id INTEGER,
    reason TEXT
)""")
db.commit()

cur.execute("""CREATE TABLE IF NOT EXISTS text_channels (
    guild_id INTEGER,
    name TEXT,
    perms TEXT,
    postion INTEGER,
    category TEXT,
    nsfw TEXT,
    slowmode INTEGER
)""")
db.commit()

cur.execute("""CREATE TABLE IF NOT EXISTS voice_channels (
    guild_id INTEGER,
    name TEXT,
    perms TEXT,
    postion INTEGER,
    category TEXT
)""")
db.commit()

cur.execute("""CREATE TABLE IF NOT EXISTS categories (
    guild_id INTEGER,
    name TEXT,
    perms TEXT,
    postion INTEGER
)""")
db.commit()

cur.execute("""CREATE TABLE IF NOT EXISTS roles (
    guild_id INTEGER,
    name TEXT,
    perms INTEGER,
    position INTEGER,
    hoist TEXT,
    mentionable TEXT,
    color TEXT
)""")

db.commit()

cur.execute("""CREATE TABLE IF NOT EXISTS serversNames (
    guild_id INTEGER,
    name TEXT
)""")

db.commit()