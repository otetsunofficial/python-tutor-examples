import psycopg2
from config import DB_CONFIG

class DB:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(**DB_CONFIG)
            self.cur = self.conn.cursor()
            # Фикс прав для схемы public
            self.cur.execute("GRANT ALL ON SCHEMA public TO robloxgod;")
            self._create_tables()
        except Exception as e:
            print(f"DB Error: {e}")
            exit(1)

    def _create_tables(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL
            );
            CREATE TABLE IF NOT EXISTS game_sessions (
                id SERIAL PRIMARY KEY, player_id INTEGER REFERENCES players(id),
                score INTEGER NOT NULL, level_reached INTEGER NOT NULL,
                played_at TIMESTAMP DEFAULT NOW()
            );
        """)
        self.conn.commit()

    def get_player_id(self, username):
        self.cur.execute("INSERT INTO players (username) VALUES (%s) ON CONFLICT (username) DO NOTHING", (username,))
        self.cur.execute("SELECT id FROM players WHERE username = %s", (username,))
        self.conn.commit()
        return self.cur.fetchone()[0]

    def save_result(self, p_id, score, level):
        if p_id:
            self.cur.execute("INSERT INTO game_sessions (player_id, score, level_reached) VALUES (%s, %s, %s)", (p_id, score, level))
            self.conn.commit()

    def get_best(self, p_id):
        self.cur.execute("SELECT MAX(score) FROM game_sessions WHERE player_id = %s", (p_id,))
        res = self.cur.fetchone()[0]
        return res if res else 0

    def get_top_10(self):
        self.cur.execute("""
            SELECT p.username, s.score, s.level_reached, TO_CHAR(s.played_at, 'DD-MM') 
            FROM game_sessions s JOIN players p ON s.player_id = p.id 
            ORDER BY s.score DESC LIMIT 10
        """)
        return self.cur.fetchall()