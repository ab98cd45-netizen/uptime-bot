from config import TG_TOKEN, TG_CHAT_ID, URL, CHECK_INTERVAL, REQ_TIMEOUT
import time
import logging
from datetime import datetime
import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

state = {url: True for url in URL}
stats = {url: {"total": 0, "success": 0} for url in URL}

def send_messg(message: str):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    payload = {"chat_id": TG_CHAT_ID, "text": message}

    try:
        response = requests.post(url, json=payload, timeout=5)
        response.raise_for_status()
        logging.info("Сообщение отправлено")
    except Exception as e:
        logging.error(f"Не удалось отправить сообщение: {e}")

def check_url(url:str) -> bool:
    try:
        start = time.monotonic()
        response = requests.get(url, timeout=REQ_TIMEOUT)
        elapsed = time.monotonic() - start
        is_ok = response.status_code < 300
        logging.info(f"{url} - код {response.status_code}, время {elapsed:.2f}sec")
        return is_ok
    except requests.RequestException as e:
        logging.warning(f"{url} - ошибка запроса: {e}")
        return False

def format_uptime(url: str) -> str:
    s = stats[url]
    if s["total"] == 0:
        return "0%"
    percent = (s["success"] / s["total"] * 100)
    return f"{percent:.2f}% за {s["total"]} проверок"

def main():
    if not URL:
        logging.error("Не заданы ссылки для мониторинга, проверьте переменную URL")
        return

    logging.info(f"Запуск бота, проверка {', '.join(URL)}")
    logging.info(f"Интервал проверки: {CHECK_INTERVAL}sec")

    while True:
        for urls in URL:
            was_up = state[urls]
            now_up = check_url(urls)

            stats[urls]["total"] += 1
            if now_up:
                stats[urls]["success"] += 1

            if was_up and not now_up:
                msg = (
                    f"**Сервис недоступен!**\n"
                    f"URL: {urls}\n"
                    f"Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                    f"Текущее состояние: {format_uptime(urls)}"
                )
                send_messg(msg)
                logging.warning(f"Alert о падении {urls} отправлен на {TG_CHAT_ID}")

            elif not was_up and now_up:
                msg = (
                    f"**Сервис восстановлен!**\n"
                    f"URL: {urls}\n"
                    f"Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                    f"Текущее состояние: {format_uptime(urls)}"
                )
                send_messg(msg)
                logging.info(f"Отправлено уведомление о восстановлении {urls}")
            state[urls] = now_up

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()