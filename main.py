import requests
from aiogram import Bot, Dispatcher
from aiogram import Router
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram import F
import asyncio

TOKEN = '6876577233:AAF9iFt6iRrsZV3SrJRiQIS9Ulr8CLduE8k'

WEATHER_API_KEY = 'c69dcb9370afbb89810c903cc1add55a'

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

router = Router()
dp.include_router(router)


def get_weather(city_name):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city_name,
        'appid': WEATHER_API_KEY,
        'units': 'metric',
        'lang': 'ru',
    }

    try:
        response = requests.get(base_url, params=params, timeout=10)
        data = response.json()
        #print(data)
        if data['cod'] == 200:
            main = data['main']
            weather_desc = data['weather'][0]['description']
            temperature = main['temp']
            humidity = main['humidity']

            return f"Погода в {city_name}:\n" \
                   f"Температура: {temperature}°C\n" \
                   f"Влажность: {humidity}%\n" \
                   f"Описание: {weather_desc.capitalize()}"
        else:
            return "Город не найден, попробуйте еще раз."

    except requests.exceptions.ReadTimeout:
        return "Превышено время ожидания ответа от сервера. Попробуйте позже."
    except requests.exceptions.ConnectionError:
        return "Ошибка соединения. Проверьте подключение к интернету."
    except Exception as error:
        return f"Произошла ошибка: {error}"


@router.message(F.text == "/start")
async def send_welcome(message: Message):
    await message.answer("Привет! Напиши название города, чтобы узнать текущую погоду.")


@router.message()
async def weather_info(message: Message):
    city = message.text
    weather_report = get_weather(city)
    await message.answer(weather_report)


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())