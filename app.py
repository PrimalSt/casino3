from flask import Flask, render_template, request, jsonify
from database import SessionLocal, init_db
from models import User, Transaction, Item
from datetime import datetime
import random
import config
import hmac
import hashlib
from sqlalchemy import select

app = Flask(__name__)
init_db()  # Создаем таблицы при запуске

@app.route('/')
def index():
    return render_template('main.html')

def validate_telegram_data(telegram_data):
    # TODO: Реализуйте проверку данных согласно документации Telegram Web Apps.
    # Пока оставляем упрощенную версию, которая всегда возвращает True.
    return True

@app.route('/api/play', methods=['POST'])
def play():
    data = request.get_json()
    telegram_data = data.get("telegramData")
    
    if not telegram_data or not validate_telegram_data(telegram_data):
        return jsonify({"error": "Неверные данные"}), 400

    telegram_id = telegram_data.get("id")
    if not telegram_id:
        return jsonify({"error": "Нет идентификатора Telegram"}), 400

    # Простейшая игровая логика: случайный выбор между выигрышем и проигрышем
    outcome = random.choice(["win", "lose"])
    if outcome == "win":
        win_amount = round(random.uniform(10, 100), 2)
        change = win_amount
        message = f"Поздравляем, вы выиграли {win_amount} единиц!"
    else:
        loss_amount = round(random.uniform(5, 50), 2)
        change = -loss_amount
        message = f"К сожалению, вы проиграли {loss_amount} единиц."

    # Работа с базой данных
    with SessionLocal() as session:
        # Используем SQLAlchemy 2.0 стиль запроса
        stmt = select(User).filter_by(telegram_id=telegram_id)
        user = session.scalars(stmt).first()
        if not user:
            user = User(
                telegram_id=telegram_id,
                username=telegram_data.get("first_name", "Unknown"),
                balance=0.0,
                registered_at=datetime.utcnow()
            )
            session.add(user)
            session.commit()  # Чтобы зафиксировать и получить ID
            session.refresh(user)
        
        # Обновляем баланс (не допускаем отрицательного значения)
        user.balance = max(user.balance + change, 0)
        
        # Записываем транзакцию
        transaction = Transaction(
            user_id=user.id,
            transaction_type="play",
            amount=change,
            timestamp=datetime.utcnow()
        )
        session.add(transaction)
        session.commit()

        balance = user.balance

    return jsonify({"result": outcome, "message": message, "balance": balance})

if __name__ == '__main__':
    app.run(debug=True)