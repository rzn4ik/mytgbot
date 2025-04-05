from flask import Flask, render_template, request, redirect, url_for
import time
from threading import Lock
import os
from datetime import datetime

app = Flask(__name__)

# Глобальные переменные
winner = None
lock = Lock()
winners_history = []  # Список для хранения истории победителей

@app.route('/')
def index():
    global winner
    with lock:
        return render_template('index.html', winner=winner, history=winners_history)

@app.route('/press', methods=['POST'])
def press():
    global winner, winners_history
    name = request.form.get('name', 'Аноним')
    current_time = datetime.now().strftime('%H:%M:%S')  # Время нажатия

    with lock:
        if winner is None:
            # Первый, кто нажал, становится победителем
            winner = f"{name} (в {current_time})"
            winners_history.insert(0, winner)  # Добавляем в начало списка
            time.sleep(2)  # Задержка 2 секунды
            winner = None  # Сбрасываем для нового раунда
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Render использует PORT, иначе 5000
    app.run(host='0.0.0.0', port=port)