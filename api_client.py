import requests
import time

from Task import Task


def get_motivation():
    try:
        url = "https://api.adviceslip.com/advice"
        response = requests.get(url, timeout=5)
        print(f"Статус-код: {response.status_code}")

        data = response.json()
        return data["slip"]["advice"]

    except requests.exceptions.RequestException:
        return "Не удалось получить совет"

def sync_task_to_server(task):
    MAX_ATTEMPTS = 3
    url = "https://jsonplaceholder.typicode.com/posts"
    payload = {
        "title": task.title,
        "body": task.priority,
        "userId": 1
    }
    for attempt in range(1, MAX_ATTEMPTS+1):
        print(f"Попытка {attempt} из {MAX_ATTEMPTS}...")
        try:
            response = requests.post(url, json = payload, timeout=5)
            status = response.status_code
            if status >= 500:
                print(f"Сервер вернул {response.status_code}. Повторяем...")
                time.sleep(2)
                continue

            if 200<= status <= 299:
                print(f"Задача «{task.title}» синхронизирована ✅")
                return True
            else:
                print(f"Ошибка: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"Сетевая ошибка: {e}")
            time.sleep(2)
            continue
    print("Не удалось синхронизировать задачу после 3 попыток")
    return False