from datetime import datetime
import json
from flask import Flask, render_template, request

# json.dump - загрузка в файл
# json.load - чтение из файла
# json.dumps - загрузка в json-строку
# json.loads - чтение json строки


def save_messages():
    """Saves messages."""
    data = {
        "messages": all_messages,
    }
    with open("db.json", "w", encoding="utf8") as file:  # We open this file for write. Энкод кириллицы
        json.dump(data, file, ensure_ascii=False)  # It loads in file.


def load_messages():
    """Loads file."""
    with open("db.json", "r") as file:
        data = json.load(file)  # It reads from file.
    return data["messages"]


def add_message(author, text):
    """Adds a message in the list."""
    message = {
        "author": author,
        "text": text,
        "time": datetime.now().strftime("%H:%M:%S"),
    }
    all_messages.append(message)
    save_messages()


def print_message(msg):
    """Prints a message."""
    print(f"[{msg['author']}]: {msg['text']} / {msg['time']}")


def print_all_messages():
    """Prints all messages."""
    for message in all_messages:
        print_message(message)


def users_count():
    """Counts user amount on our chat."""
    users = set()
    for user in all_messages:
        users.add(user['author'])
    return len(users)


def status():
    """Outputs info an user amount and messages in our chat."""
    return {"users_count": users_count(), "messages_count": len(all_messages)}


all_messages = load_messages()
print(status())

app = Flask(__name__)


@app.route("/")  # Объявили первый эндпоинт
def main_paige():
    return "Hello Skillbox"


@app.route("/chat")  # основная страница с использованием темплейта form.html
def chat_page():
    return render_template("form.html")


@app.route("/get_messages")  # Получаем все сообщения
def get_messages():
    return {"messages": all_messages, "status": status()}


@app.route("/send_message")  # Сохраняем сообщение
def send_message():
    name = request.args.get("name", "")
    text = request.args.get("text", "")
    add_message(name, text)

    return "ok"


app.run(host='0.0.0.0', port=8080)
