import telebot
import threading
import time
import random
import sys

# Mã thông báo bot Telegram (Thay thế bằng mã thông báo thực tế của bạn)
TOKEN = "6340884614:AAGe91rsyvWDzEsmjYMiP7QLcn4dGLLXEqw"

# Đường dẫn đến tệp tin chứa danh sách proxy
PROXY_FILE = "a.txt"

# Danh sách Referer (ref)
ref = [
    'https://duckduckgo.com/', 'https://www.google.com/',
    'https://www.bing.com/', 'https://www.yandex.ru/',
    'https://search.yahoo.com/', 'https://www.facebook.com/',
    'https://twitter.com/', 'https://www.youtube.com/'
]

# Danh sách User-Agent (ua)
ua = [
    "Mozilla/5.0 (Android; Linux armv7l; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 Fennec/10.0.1",
]

# Số lượng luồng tối đa
MAX_THREADS = 600

# Biến toàn cục
N = 0

# Khởi tạo bot Telegram
bot = telebot.TeleBot(TOKEN)

# Lưu trạng thái tạm thời của người dùng
user_data = {}


# Lắng nghe lệnh /start từ người dùng
@bot.message_handler(commands=['start'])
def handle_start(message):
    # Yêu cầu người dùng nhập liên kết web
    msg = bot.reply_to(message, "Nhập liên kết web:")
    bot.register_next_step_handler(msg, handle_website_input)


# Hàm xử lý nhập liên kết web
def handle_website_input(message):
    website_link = message.text

    # Kiểm tra xem liên kết có đúng định dạng không
    if not website_link.startswith("https://"):
        msg = bot.reply_to(message, "Liên kết không hợp lệ. Vui lòng nhập lại với định dạng 'https://example.com'.")
        bot.register_next_step_handler(msg, handle_website_input)
        return

    # Lưu trạng thái tạm thời của người dùng
    user_id = message.from_user.id
    user_data[user_id] = {'website_link': website_link}

    # Yêu cầu người dùng chọn phương thức tấn công
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('TCP', 'SYN', 'UDP', 'Cloudflare', 'IP Flood', 'Proxy/socks5')
    msg = bot.reply_to(message, "Chọn phương thức tấn công:", reply_markup=markup)
    bot.register_next_step_handler(msg, handle_attack_method)


# Hàm xử lý chọn phương thức tấn công
def handle_attack_method(message):
    user_id = message.from_user.id
    attack_method = message.text

    if attack_method not in ['TCP', 'SYN', 'UDP', 'Cloudflare', 'IP Flood', 'Proxy/socks5']:
        msg = bot.reply_to(message, "Phương thức không hợp lệ. Vui lòng chọn từ danh sách.")
        bot.register_next_step_handler(msg, handle_attack_method)
        return

    # Lưu trạng thái tạm thời của người dùng
    user_data[user_id]['attack_method'] = attack_method

    # Yêu cầu người dùng nhập thời gian
    msg = bot.reply_to(message, "Nhập thời gian (tối đa 600 giây):")
    bot.register_next_step_handler(msg, handle_attack_duration)


# Hàm xử lý nhập thời gian
def handle_attack_duration(message):
    user_id = message.from_user.id
    attack_duration = message.text

    # Kiểm tra xem attack_duration có phải là số không
    if not attack_duration.isdigit():
        msg = bot.reply_to(message, "Thời gian không hợp lệ. Vui lòng nhập lại bằng số.")
        bot.register_next_step_handler(msg, handle_attack_duration)
        return

    # Chuyển đổi attack_duration thành số nguyên
    attack_duration = int(attack_duration)

    # Kiểm tra xem thời gian có lớn hơn hoặc bằng 600 không
    if attack_duration > 600:
        msg = bot.reply_to(message, "Thời gian phải nhỏ hơn hoặc bằng 600 giây. Vui lòng nhập lại.")
        bot.register_next_step_handler(msg, handle_attack_duration)
        return

    # Lưu trạng thái tạm thời của người dùng
    user_data[user_id]['attack_duration'] = attack_duration

    # Tiến hành tấn công liên kết web ở đây sử dụng thông tin từ user_data

    website_link = user_data[user_id]['website_link']
    attack_method = user_data[user_id]['attack_method']
    attack_duration = user_data[user_id]['attack_duration']

    bot.reply_to(
        message,
        f"Đang tấn công : {website_link}\nPhương thức:{attack_method}\nThời gian: {attack_duration} giây.\nAttack Proxy By : Hieu Henry\nThis software needs Listings Proxy Or Sock 5\nEdit And Upgrade Version By Henry"
    )


# (Các phần khác giữ nguyên như trong mã nguồn trước đó)

# Khởi động bot Telegram
bot.polling()
