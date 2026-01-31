from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)
DB = "demo_cloud.db"

def init_db():
    con = sqlite3.connect(DB)
    cur = con.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS dairies (code TEXT, name TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS milk (dairy TEXT, customer TEXT, date TEXT, fat REAL, amount REAL)")

    cur.execute("DELETE FROM dairies")
    cur.execute("DELETE FROM milk")

    cur.execute("INSERT INTO dairies VALUES ('DRY001','Jaipur Dairy')")
    cur.execute("INSERT INTO dairies VALUES ('DRY002','Sikar Dairy')")

    cur.execute("INSERT INTO milk VALUES ('DRY001','1','2026-01-01',4.5,420)")
    cur.execute("INSERT INTO milk VALUES ('DRY001','1','2026-01-02',4.2,380)")
    cur.execute("INSERT INTO milk VALUES ('DRY002','1','2026-01-01',4.6,460)")

    con.commit()
    con.close()

HTML = """
<h3>Multi Dairy Online Passbook (FREE DEMO)</h3>
<form>
Dairy Code: <input name="dairy"><br><br>
Customer Code: <input name="customer"><br><br>
<button>View</button>
</form>
{% if rows %}
<hr>
<table border=1 cellpadding=5>
<tr><th>Date</th><th>Fat</th><th>Amount</th></tr>
{% for r in rows %}
<tr><td>{{r[0]}}</td><td>{{r[1]}}</td><td>{{r[2]}}</td></tr>
{% endfor %}
</table>
{% endif %}
"""

@app.route("/")
def home():
    dairy = request.args.get("dairy")
    customer = request.args.get("customer")
    rows = []

    if dairy and customer:
        con = sqlite3.connect(DB)
        cur = con.cursor()
        cur.execute("SELECT date, fat, amount FROM milk WHERE dairy=? AND customer=?", (dairy, customer))
        rows = cur.fetchall()
        con.close()

    return render_template_string(HTML, rows=rows)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=8080)
