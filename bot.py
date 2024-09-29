import os
import subprocess
import telebot

TOKEN = '7218694009:AAG3KH-Z6SLzZsorYZkGZYvJ_UZ_tTGcoWg'
bot = telebot.TeleBot(TOKEN)

def create_user_folder(user_id):
    user_folder = f"/{user_id}"
    os.makedirs(user_folder, exist_ok=True)
    return user_folder

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    profile_link = f"https://t.me/{message.from_user.username}" if message.from_user.username else "Нет имени пользователя"
    user_folder = create_user_folder(user_id)
    welcome_message = f"*👋 Привет [ {first_name} ]({profile_link})!*\n\n*👨‍💻 Чтобы установить хику себе на аккаунт, напиши* `/hikka`"
    bot.send_message(message.chat.id, welcome_message, parse_mode='Markdown')

@bot.message_handler(commands=['hikka'])
def hikka(message):
    user_id = message.from_user.id
    waiting_message = "*🔃 Ожидайте...*\n*😎 Примерное время ожидания* `1-2` *минуты.*"
    bot.send_message(message.chat.id, waiting_message, parse_mode='Markdown')
    user_folder = create_user_folder(user_id)
    hikka_link = create_hikka_session(user_folder)
    if hikka_link:
        bot.send_message(message.chat.id, f"*Hikka успешно установлен и запущен. Ссылка на Hikka:* {hikka_link}", parse_mode='Markdown')

def create_hikka_session(user_folder):
    try:
        result = subprocess.run(['bash', 'install_hikka.sh', user_folder], capture_output=True, text=True, check=True)
        return result.stdout.strip().split('Ссылка на Hikka: ')[-1]
    except subprocess.CalledProcessError:
        return None

@bot.message_handler(commands=['stop'])
def stop(message):
    user_id = message.from_user.id
    try:
        subprocess.run(['pkill', '-f', 'hikka'], check=True)
        bot.send_message(message.chat.id, "*Hikka остановлен.*", parse_mode='Markdown')
    except subprocess.CalledProcessError:
        bot.send_message(message.chat.id, "*Не удалось остановить Hikka.*", parse_mode='Markdown')

@bot.message_handler(commands=['uninstall'])
def uninstall(message):
    user_id = message.from_user.id
    user_folder = f"/{user_id}"
    try:
        subprocess.run(['rm', '-rf', user_folder], check=True)
        bot.send_message(message.chat.id, "*Hikka удалён.*", parse_mode='Markdown')
    except subprocess.CalledProcessError:
        bot.send_message(message.chat.id, "*Не удалось удалить Hikka.*", parse_mode='Markdown')

bot.polling()
