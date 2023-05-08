from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Veritabanı bağlantısı
conn = sqlite3.connect('sozluk.db')
c = conn.cursor()

# Sözlük tablosunu oluşturma
c.execute('''CREATE TABLE IF NOT EXISTS sozluk
             (kelime TEXT PRIMARY KEY, tanim TEXT)''')

# Ana sayfa
@app.route('/')
def home():
    return render_template('home.html')

# Kelime arama
@app.route('/arama', methods=['GET', 'POST'])
def arama():
    if request.method == 'POST':
        kelime = request.form['kelime']
        c.execute("SELECT tanim FROM sozluk WHERE kelime=?", (kelime,))
        tanim = c.fetchone()
        if tanim is not None:
            return render_template('arama.html', kelime=kelime, tanim=tanim[0])
        else:
            return render_template('arama.html', kelime=kelime, tanim="Kelime bulunamadı")
    return render_template('arama.html')

# Yeni kelime ekleme
@app.route('/ekle', methods=['GET', 'POST'])
def ekle():
    if request.method == 'POST':
        kelime = request.form['kelime']
        tanim = request.form['tanim']
        c.execute("INSERT INTO sozluk (kelime, tanim) VALUES (?, ?)", (kelime, tanim))
        conn.commit()
        return render_template('ekle.html', kelime=kelime, tanim=tanim)
    return render_template('ekle.html')

if __name__ == '__main__':
    app.run()

