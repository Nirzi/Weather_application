import requests
from plyer import notification
from datetime import datetime

API_KEY = "ef209120327b90dd8e685562d563a3a5"  # Ваш API ключ
DEFAULT_CITY = "Москва"  # Город по умолчанию

def get_weather(city: str, api_key: str) -> dict:
    """
    Выполняет запрос к API OpenWeatherMap и возвращает данные о погоде в виде словаря.
    """
    url = (
        f"https://api.openweathermap.org/data/2.5/weather?"
        f"q={city}&appid={api_key}&units=metric&lang=ru"
    )
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Ошибка получения погоды: статус {response.status_code}")

def format_weather_message(weather_dict: dict) -> str:
    """
    Форматирует полученные данные о погоде в удобочитаемое сообщение.
    """
    temp = weather_dict['main']['temp']
    feels_like = weather_dict['main']['feels_like']
    description = weather_dict['weather'][0]['description']
    city_name = weather_dict['name']
    humidity = weather_dict['main']['humidity']
    pressure = weather_dict['main']['pressure']
    wind_speed = weather_dict['wind']['speed']
    
    # Данные о восходе и закате
    sunrise_unix = weather_dict['sys']['sunrise']
    sunset_unix = weather_dict['sys']['sunset']
    # Конвертация Unix времени в локальное время
    sunrise_time = datetime.fromtimestamp(sunrise_unix).strftime('%H:%M:%S')
    sunset_time = datetime.fromtimestamp(sunset_unix).strftime('%H:%M:%S')
    
    message = (
        f"Город: {city_name}\n"
        f"Температура: {temp}°C\n"
        f"Ощущается как: {feels_like}°C\n"
        f"Описание: {description}\n"
        f"Влажность: {humidity}%\n"
        f"Давление: {pressure} гПа\n"
        f"Скорость ветра: {wind_speed} м/с\n"
        f"Восход: {sunrise_time}\n"
        f"Закат: {sunset_time}"
    )
    return message

def notify_weather(message: str) -> None:
    """
    Отправляет системное уведомление с информацией о погоде.
    """
    notification.notify(
        title="Прогноз погоды",
        message=message,
        app_name="Weather App",
        timeout=10
    )

def main():
    try:
        city = input(f"Введите название города (по умолчанию '{DEFAULT_CITY}'): ") or DEFAULT_CITY
        weather_data = get_weather(city, API_KEY)
        weather_message = format_weather_message(weather_data)
        print(weather_message)  # Отобразим в консоли
        notify_weather(weather_message)  # Отправим уведомление
    except Exception as e:
        error_message = f"Произошла ошибка: {e}"
        print(error_message)
        with open("error_log.txt", "w", encoding="utf-8") as f:
            f.write(error_message)
    finally:
        input("Нажмите Enter для выхода...")

if __name__ == "__main__":
    main()
