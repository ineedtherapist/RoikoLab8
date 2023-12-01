from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, func
from sqlalchemy.orm import declarative_base, Session, relationship

# Підключення до бази даних
engine = create_engine('sqlite:///lab8.db', echo=False)
Base = declarative_base()


# Оголошення класів моделей

class User(Base):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True)
    user_name = Column(String)


class Message(Base):
    __tablename__ = 'messages'

    mes_id = Column(Integer, primary_key=True, autoincrement=True)
    sender_id = Column(Integer, ForeignKey('user.user_id'), nullable=False)
    receiver_id = Column(Integer, ForeignKey('user.user_id'), nullable=False)
    text = Column(String, nullable=False)

    sender = relationship("User", foreign_keys=[sender_id])
    receiver = relationship("User", foreign_keys=[receiver_id])


# Створення таблиць
Base.metadata.create_all(engine)


# Створення сесії
def create_session():
    return Session(engine)


# Функція для створення нового користувача
def create_user(session, name):
    new_user = User(user_name=name)
    session.add(new_user)
    session.commit()


# Функція для відправки повідомлення
def send_message(session, sender_id, receiver_id, text):
    new_message = Message(sender_id=sender_id, receiver_id=receiver_id, text=text)
    session.add(new_message)
    session.commit()


# Функція для отримання всіх повідомлень
def get_all_messages(session):
    return session.query(Message).all()


# Функція для отримання повідомлень для конкретного користувача
def get_user_messages(session, user_id):
    return session.query(Message).filter(
        (Message.sender_id == user_id) | (Message.receiver_id == user_id)
    ).all()


# Функція для отримання останніх N повідомлень
def get_latest_messages(session, n):
    return session.query(Message).order_by(Message.mes_id.desc()).limit(n).all()


# Закриття сесії
def close_session(session):
    session.close()


# Приклад використання:
session = create_session()

# Створення користувачів
create_user(session, "John")
create_user(session, "Jane")

# Відправка повідомлення
send_message(session, 1, 2, "Hello!")

# Отримання всіх повідомлень
all_messages = get_all_messages(session)
print("Всі повідомлення:")
for message in all_messages:
    sender_name = message.sender.user_name if message.sender else "Unknown Sender"
    receiver_name = message.receiver.user_name if message.receiver else "Unknown Receiver"
    print(f"{sender_name} -> {receiver_name}: {message.text}")

# Отримання повідомлень для Джона
john_messages = get_user_messages(session, 3)
print("\nПовідомлення Джона:")
for message in john_messages:
    sender_name = message.sender.user_name if message.sender else "Unknown Sender"
    receiver_name = message.receiver.user_name if message.receiver else "Unknown Receiver"
    print(f"{sender_name} -> {receiver_name}: {message.text}")

# Отримання останніх 3 повідомлень
latest_messages = get_latest_messages(session, 3)
print("\nОстанні 3 повідомлення:")
for message in latest_messages:
    sender_name = message.sender.user_name if message.sender else "Unknown Sender"
    receiver_name = message.receiver.user_name if message.receiver else "Unknown Receiver"
    print(f"{sender_name} -> {receiver_name}: {message.text}")

# Закриття сесії
close_session(session)
