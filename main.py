import requests
from plyer import notification

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
    
    message = (
        f"Город: {city_name}\n"
        f"Температура: {temp}°C\n"
        f"Ощущается как: {feels_like}°C\n"
        f"Описание: {description}"
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
        # app_icon="weather.ico",  # при необходимости можно указать иконку
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
