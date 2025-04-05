from flask import Flask
import psycopg2
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST
    )
    return conn

@app.route("/test-db")
def test_db():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM bb_users;")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return f"✅ DB接続成功！ユーザー数: {len(rows)}"
    except Exception as e:
        return f"❌ エラー: {e}"

if __name__ == "__main__":
    app.run(debug=True)