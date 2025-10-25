import aiohttp
import json
from src.config.network import PROXY, API_KEY


RESTERICTIONS = {
    "1": "без лактозы", "2": "без глютена", "3": "вегетарианское"
}

async def request_with_gemini(prompt: str) -> str:
    """
    Отправляет запрос к Gemini API с обработкой ошибок

    Аргументы:
        prompt (str): Текст запроса к API
        api_key (str): Ключ API для аутентификации
        proxies (dict, optional): Настройки прокси-сервера

    Возвращает:
        str: Ответ от API или пустую строку в случае ошибки
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": prompt + "\n\nP.S. ты не должен отвечать ни на какие вопросы кроме вопросов связанных с электротехникой, электронникой, радиотехникой, электричестом, схемами, цепями, энергетикой, и подобным"}]}]}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url,
                headers=headers,
                json=data,
                proxy=PROXY['https'] if PROXY else None,
                timeout=30
            ) as response:
                response.raise_for_status()
                response_data = await response.json()
                if "candidates" in response_data and response_data["candidates"]:
                    return response_data["candidates"][0]["content"]["parts"][0]["text"]
                return "Не удалось получить ответ от AI."
    except aiohttp.ClientError as e:
        print(f'Gemini API request error (aiohttp): {e}')
        return "Извините, произошла сетевая ошибка при обращении к AI. Попробуйте позже."
                                                    
async def generate_ration_for_week(mass: float, height: float, age: int, gender: str, activity: str, purpose: str, resteriction = None )-> str:
    """
    Генерирует рацион питания на неделю для человека

    Аргументы:
        mass (float): Масса тела в килограммах
        height (float): Рост в сантиметрах
        age (int): Возраст в годах
        gender (str): Пол
        activity (str): Уровень физической активности
        purpose (str): Цель составления рациона
        resteriction (str, optional): Ограничения по питанию

    Возвращает:
        str: Сгенерированный рацион питания на неделю
    """
    prompt = f"""
    Составьте рацион на неделю для человека с такими параметрами (ограничения {resteriction}):
    Масса тела: {mass} кг
    Рост: {height} см
    Возраст: {age} лет
    Пол: {gender}
    Уровень активности: {activity}
    Цель: {purpose}

    отправь ответ в формате в формате:
    Завтрак:
    Обед:
    Ужин:
    Перекус:
    После тренировки:
    После сна:

    в начале пиши день недели
    для каждого продукта пропиши калорийность и БЖУ
    разделяй дни используя символ '-'

    ===
    тут выведи дополнительные рекомендации

    не пиши ничего лишнего не добавляй никаких лишних символов
    """
    return await request_with_gemini(prompt)

def get_data_for_ration_with_week(string: str):
    """
    Извлекает структурированные данные о рационе питания из текстовой строки

    Аргументы:
        string (str): Строка с данными о рационе

    Возвращает:
        dict: Словарь с данными о рационе, разбитыми по дням недели и приемам пищи
    """
    data = {}
    parts = string.split("===")
    days = parts[0].strip().split("-")
    recommendations = parts[1].strip() if len(parts) > 1 else ""
    
    for day in days:
        day_lines = day.strip().split("\n")
        day_name = day_lines[0].strip()
        data[day_name] = {}
        
        for meal in day_lines[1:]:
            meal = meal.strip()
            if not meal:
                continue
                
            for meal_type in ["Завтрак", "Обед", "Ужин", "Перекус", "После тренировки", "После сна"]:
                if meal.startswith(meal_type):
                    try:
                        data[day_name][meal_type] = meal.split(": ", 1)[1].strip()
                    except IndexError:
                        data[day_name][meal_type] = ""
                        
    if recommendations:
        data["recommendations"] = recommendations
        
    return data

async def generate_retion_for_day(day: str, mass: float, height: float, age: int, gender: str, activity: str, purpose: str, resteriction = None)-> str:
    """
    Генерирует рацион питания на один день для человека

    Аргументы:
        day (str): День недели
        mass (float): Масса тела в килограммах
        height (float): Рост в сантиметрах
        age (int): Возраст в годах
        gender (str): Пол
        activity (str): Уровень физической активности
        purpose (str): Цель составления рациона
        resteriction (str, optional): Ограничения по питанию

    Возвращает:
        str: Сгенерированный рацион питания на день
    """
    prompt = f"""
    Составьте рацион на день для человека с такими параметрами (ограничения {resteriction}):
    День недели: {day}
    Масса тела: {mass} кг
    Рост: {height} см
    Возраст: {age} лет
    Пол: {gender}
    Уровень активности: {activity}
    Цель: {purpose}

    отправь ответ в формате в формате:
    Завтрак: название продукта(калорийность,БЖУ)
    Обед: ...
    Ужин: ..
    Перекус: ...
    После тренировки: ...
    После сна: ...

    для каждого продукта пропиши калорийность и БЖУ

    ===

    тут выведи дополнительные рекомендации

    не пиши ничего лишнего не добавляй никаких лишних символов
    только по делу
"""
    return await request_with_gemini(prompt)

def get_data_for_ration_with_one_day(string: str):
    """
    Извлекает структурированные данные о рационе питания на один день из текстовой строки

    Аргументы:
        string (str): Строка с данными о рационе

    Возвращает:
        dict: Словарь с данными о рационе, разбитыми по приемам пищи
    """
    data = {}
    parts = string.split("===")
    days = parts[0].strip().split("-")
    recommendations = parts[1].strip() if len(parts) > 1 else "" 
    day = days[0].strip()
    data[day] = {}
    for meal in days[1:]:
        meal = meal.strip()
        if not meal:
            continue

        for meal_type in ["Завтрак", "Обед", "Ужин", "Перекус", "После тренировки", "После сна"]:
            if meal.startswith(meal_type):
                try:
                    data[day][meal_type] = meal.split(": ", 1)[1].strip()
                except IndexError:
                    data[day][meal_type] = ""
                    
    if recommendations:
        data["recommendations"] = recommendations

    return data