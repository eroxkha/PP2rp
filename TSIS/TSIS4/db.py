import psycopg2

_HOST = "localhost"
_DB   = "snake_game"
_USER = "postgres"
_PASS = "password"   # <-- твой пароль сюда, только латинские символы
_PORT = 5432


def get_connection():
    try:
        conn = psycopg2.connect(
            host=_HOST,
            database=_DB,
            user=_USER,
            password=_PASS,
            port=_PORT,
            options="-c client_encoding=UTF8"
        )
        return conn
    except Exception as e:
        print(f"DB connection error: {e}")
        return None


def init_db():
    conn = get_connection()
    if not conn:
        return
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS game_sessions (
            id SERIAL PRIMARY KEY,
            player_id INTEGER REFERENCES players(id),
            score INTEGER NOT NULL,
            level_reached INTEGER NOT NULL,
            played_at TIMESTAMP DEFAULT NOW()
        )
    """)
    conn.commit()
    cur.close()
    conn.close()


def get_or_create_player(username):
    conn = get_connection()
    if not conn:
        return None
    cur = conn.cursor()
    cur.execute("SELECT id FROM players WHERE username = %s", (username,))
    row = cur.fetchone()
    if row:
        player_id = row[0]
    else:
        cur.execute("INSERT INTO players (username) VALUES (%s) RETURNING id", (username,))
        player_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return player_id


def save_session(player_id, score, level_reached):
    conn = get_connection()
    if not conn:
        return
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO game_sessions (player_id, score, level_reached) VALUES (%s, %s, %s)",
        (player_id, score, level_reached)
    )
    conn.commit()
    cur.close()
    conn.close()


def get_top10():
    conn = get_connection()
    if not conn:
        return []
    cur = conn.cursor()
    cur.execute("""
        SELECT p.username, gs.score, gs.level_reached, gs.played_at
        FROM game_sessions gs
        JOIN players p ON p.id = gs.player_id
        ORDER BY gs.score DESC
        LIMIT 10
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def get_personal_best(player_id):
    conn = get_connection()
    if not conn:
        return 0
    cur = conn.cursor()
    cur.execute(
        "SELECT MAX(score) FROM game_sessions WHERE player_id = %s",
        (player_id,)
    )
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row and row[0]:
        return row[0]
    return 0