import dotenv
import os

dotenv.load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))

SUBSCRIPTIONS = {
    'standart': {
        'name': '🎯 Базовый',
        'price': 0,
        'period': 'навсегда',
        'features': [
            '✓ Базовые функции',
            '✓ Ограниченный доступ',
            '✓ Стандартная поддержка'
        ],
        'payment_url': 'https://example.com/pay/standart'
    },
    'premium': {
        'name': '🌟 Студент',
        'price': 199,
        'period': 'в месяц',
        'features': [
            '✓ Все функции Standart',
            '✓ Неограниченное количество текстовых запросов',
            '✓ Расширенные пошаговые решения задач с комментариями',
            '✓ Доступ к базе данных компонентов и их аналогов'
        ],
        'payment_url': 'https://example.com/pay/premium'
    },
    'premium_plus': {
        'name': '🚀 Профессионал',
        'price': 499,
        'period': 'в месяц',
        'features': [
            '✓ Все функции Premium',
            '✓ Распознавание изображений и анализ схем',
            '✓ Доступ к модулю диагностики неисправностей',
            '✓ Самый высокий приоритет обработки и техническая поддержка'
        ],
        'payment_url': 'https://example.com/pay/premium_plus'
    }
}

# Клавиатуры
main_keyboard = [
    ['💎 Подписки', '🆘 Поддержка'],
    ['📊 Мой аккаунт', 'ℹ️ О продукте']
]

subscriptions_keyboard = [
    ['🎯 Базовый', '🌟 Студент'],
    ['🚀 Профессионал', '🔙 Назад'],
]

support_keyboard = [
    ['💬 Написать в поддержку', '📞 Контакты'],
    ['🔙 Назад']
]

PURCHASES_FILE = 'purchases.json'