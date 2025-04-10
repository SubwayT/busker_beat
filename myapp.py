from flask import Flask, render_template, request, redirect, jsonify
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

#ルートURLにアクセスしたときの処理
@app.route("/")
def home():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, artist_name, lat, lng, amount, event_date, setlist FROM bb_posts;")
        posts = cur.fetchall()
        cur.close()
        conn.close()
        return render_template("index.html", posts=posts)  
    except Exception as e:
        return f"❌ 地図用データの読み込みに失敗しました: {e}"

#テスト用のDB接続
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

#投稿処理
@app.route("/posting", methods=["POST"])
def posting():
    try:
        artist_name = request.form["artist_name"]
        audience = request.form["audience"]
        amount = request.form["amount"]
        setlist = request.form["setlist"]
        lat = request.form["lat"]
        lng = request.form["lng"]
        event_date = request.form["event_date"]

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO bb_posts (user_id, artist_name, lat, lng, audience, setlist, amount, event_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (1, artist_name, lat, lng, audience, setlist, amount, event_date))
        conn.commit()
        cur.close()
        conn.close()

        # 成功時に投稿情報をJSONで返す
        return jsonify({
            "success": True,
            "artist_name": artist_name,
            "lat": float(lat),
            "lng": float(lng),
            "amount": amount,
            "event_date": event_date,
            "setlist": setlist
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)