from flask import Flask, render_template, request, redirect, url_for
import time
from threading import Lock
import os
from datetime import datetime

app = Flask(__name__)

# Глобальные переменные
winner = None
lock = Lock()
winners_history = []  # Список для хранения победителей с временем в секундах

@app.route('/')
def index():
    global winner
    with lock:
        # Группируем победителей по раундам
        rounds = []
        current_round = []
        for entry in winners_history:
            if not current_round:
                current_round.append(entry)
            else:
                # Сравниваем время с последним победителем
                last_time = current_round[-1]['timestamp']
                current_time = entry['timestamp']
                if current_time - last_time > 30:  # Новый раунд, если больше 30 секунд
                    rounds.append(current_round)
                    current_round = [entry]
                else:
                    current_round.append(entry)
        if current_round:
            rounds.append(current_round)

        return render_template('index.html', winner=winner, rounds=rounds)

@app.route('/press', methods=['POST'])
def press():
    global winner, winners_history
    name = request.form.get('name', 'Аноним')
    current_time_str = datetime.now().strftime('%H:%M:%S')  # Время в формате ЧЧ:ММ:СС
    current_time_sec = time.time()  # Время в секундах для сравнения

    with lock:
        if winner is None:
            # Первый, кто нажал, становится победителем
            winner = f"{name} (в {current_time_str})"
            winners_history.insert(0, {'name': winner, 'timestamp': current_time_sec})
            time.sleep(2)  # Задержка 2 секунды
            winner = None  # Сбрасываем для нового раунда
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Render использует PORT, иначе 5000
    app.run(host='0.0.0.0', port=port)