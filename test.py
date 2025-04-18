import os
from dotenv import load_dotenv
import ptbot
from pytimeparse import parse


def render_progressbar(total, iteration, prefix='', suffix='', length=20, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}".format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return f'{prefix} |{pbar}| {percent}% {suffix}'


def notify_progress(secs_left, total_secs, chat_id, message_id, bot):
    if secs_left > 0:
        progressbar = render_progressbar(total_secs, total_secs - secs_left, prefix="Прогресс:")
        message = f"Осталось {secs_left} секунд.\n{progressbar}"
        bot.update_message(chat_id, message_id, message)
        bot.create_timer(1, lambda: notify_progress(secs_left - 1, total_secs, chat_id, message_id, bot))
    else:
        time_is_up(chat_id, message_id, bot)


def time_is_up(chat_id, message_id, bot):
    message = "Время вышло. Поспеши на кухню!"
    bot.update_message(chat_id, message_id, message)


def wait(chat_id, question, bot):
    seconds = parse(question)

    if seconds is None:
        bot.send_message(chat_id, "Неверный формат времени. Попробуйте, например, '3s' или '1m'.")
        return

    initial_message = "Таймер запущен."
    message_id = bot.send_message(chat_id, initial_message)
    notify_progress(seconds, seconds, chat_id, message_id, bot)


def main():
    load_dotenv()
    tg_token = os.getenv("TELEGRAM_TOKEN")

    bot = ptbot.Bot(tg_token)
    bot.reply_on_message(lambda chat_id, msg: wait(chat_id, msg, bot))
    bot.run_bot()


if __name__ == '__main__':
    main()
