from flask import Flask, render_template, request, redirect, url_for
import time
from threading import Lock
import os  # Добавили импорт os

app = Flask(__name__)

# Глобальная переменная для хранения победителя и блокировка
winner = None
lock = Lock()

@app.route('/')
def index():
    global winner
    with lock:
        if winner is None:
            return render_template('index.html', winner=None)
        else:
            return render_template('index.html', winner=winner)

@app.route('/press', methods=['POST'])
def press():
    global winner
    with lock:
        if winner is None:
            # Первый, кто нажал, становится победителем
            winner = request.form.get('name', 'Аноним')
            time.sleep(2)  # Задержка 2 секунды перед сбросом
            winner = None  # Сбрасываем для нового раунда
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Render использует PORT, иначе 5000
    app.run(host='0.0.0.0', port=port)