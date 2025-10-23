import json
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8492419619:AAHwjD2yCOi3ifoTajrOto2ryb1L9tti010"

# Данные о подписках
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

main_reply_markup = ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)
subscriptions_reply_markup = ReplyKeyboardMarkup(subscriptions_keyboard, resize_keyboard=True)
support_reply_markup = ReplyKeyboardMarkup(support_keyboard, resize_keyboard=True)

# Файл для хранения покупок (если нужно)
PURCHASES_FILE = 'purchases.json'

def load_purchases():
    """Загрузка данных о покупках"""
    try:
        with open(PURCHASES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_purchases(purchases):
    """Сохранение данных о покупках"""
    with open(PURCHASES_FILE, 'w', encoding='utf-8') as f:
        json.dump(purchases, f, ensure_ascii=False, indent=2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    welcome_text = """
Привет! 🤙 Вы активировали Joule Bot. 

Здесь вы получите помощь с задачами связанными с электросхемами. Мы используем ИИ модели, обученные на обширных источинках данных.

Просто отправь свою проблему и получи леща ответ😊
    """
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=main_reply_markup
    )

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать главное меню (без приветственного сообщения)"""
    menu_text = "Выберите действие в меню ниже 👇"
    
    await update.message.reply_text(
        menu_text,
        reply_markup=main_reply_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик текстовых сообщений"""
    text = update.message.text
    user_id = update.message.from_user.id
    
    if text == '💎 Подписки':
        await show_subscriptions(update, context)
    elif text == '🆘 Поддержка':
        await show_support(update, context)
    elif text == '📊 Мой аккаунт':
        await show_my_account(update, context)
    elif text == 'ℹ️ О продукте':
        await show_about(update, context)
    elif text == '🎯 Базовый':
        await show_subscription_details(update, context, 'standart')
    elif text == '🌟 Студент':
        await show_subscription_details(update, context, 'premium')
    elif text == '🚀 Профессионал':
        await show_subscription_details(update, context, 'premium_plus')
    elif text == '💬 Написать в поддержку':
        await contact_support(update, context)
    elif text == '📞 Контакты':
        await show_contacts(update, context)
    elif text == '🔙 Назад':
        await show_main_menu(update, context)  # Используем новую функцию вместо start
    else:
        await update.message.reply_text(
            "Используйте кнопки для навигации 👇",
            reply_markup=main_reply_markup
        )

async def show_subscriptions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать доступные подписки"""
    subscriptions_text = """
💎 **Доступные подписки:**

🎯 **Базовый** - Бесплатно
• Базовые функции
• Ограниченный доступ
• Стандартная поддержка

🌟 **Студент** - 199₽/месяц  
• Все функции подписки Базовый
• Неограниченное количество текстовых запросов
• Расширенные пошаговые решения задач с комментариями
• Доступ к базе данных компонентов и их аналогов

🚀 **Профессионал** - 499₽/месяц
• Все функции подписки Студент
• Распознавание изображений и анализ схем
• Доступ к модулю диагностики неисправностей
• Самый высокий приоритет обработки и техническая поддержка

Выберите подписку для подробной информации 👇
    """
    
    await update.message.reply_text(
        subscriptions_text,
        reply_markup=subscriptions_reply_markup,
        parse_mode='Markdown'
    )

async def show_subscription_details(update: Update, context: ContextTypes.DEFAULT_TYPE, subscription_type: str):
    """Показать детали подписки и кнопку покупки"""
    sub = SUBSCRIPTIONS[subscription_type]
    
    # Формируем текст с деталями подписки
    features_text = "\n".join(sub['features'])
    
    if sub['price'] == 0:
        price_text = "Бесплатно"
    else:
        price_text = f"{sub['price']}₽ {sub['period']}"
    
    subscription_text = f"""
{sub['name']}

💵 Стоимость: {price_text}

📋 Возможности:
{features_text}

🎁 После оплаты вы мгновенно получите доступ к функциям подписки!
    """
    
    # Создаем инлайн-кнопку для оплаты
    if sub['price'] > 0:
        keyboard = [
            [InlineKeyboardButton("💳 Купить подписку", url=sub['payment_url'])],
            [InlineKeyboardButton("✅ Я оплатил", callback_data=f"paid_{subscription_type}")]
        ]
    else:
        keyboard = [
            [InlineKeyboardButton("🎁 Получить бесплатно", callback_data=f"get_free_{subscription_type}")]
        ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        subscription_text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def show_support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать раздел поддержки"""
    support_text = """
🆘 **Служба поддержки**

Здесь вы можете получить помощь по любым вопросам:
    """
    
    await update.message.reply_text(
        support_text,
        reply_markup=support_reply_markup
    )

async def contact_support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Связаться с поддержкой"""
    contact_text = """
💬 **Написать в поддержку**

Для быстрой помощи:
• Напишите нам: @support_username
• Или задайте вопрос прямо здесь

Мы ответим в течение 15 минут в рабочее время (9:00-21:00 МСК)
    """
    
    await update.message.reply_text(
        contact_text,
        reply_markup=support_reply_markup
    )

async def show_contacts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать контакты"""
    contacts_text = """
📞 **Контакты**

• Техническая поддержка: @support_username
• Email: support@example.com
• Сайт: example.com

⏰ Время работы поддержки: 
Пн-Пт: 9:00-21:00 МСК
Сб-Вс: 10:00-18:00 МСК
    """
    
    await update.message.reply_text(
        contacts_text,
        reply_markup=support_reply_markup
    )

async def show_my_account(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать информацию об аккаунте"""
    user = update.message.from_user
    user_id = user.id
    
    purchases = load_purchases()
    user_purchases = purchases.get(str(user_id), {})
    
    if user_purchases:
        current_sub = user_purchases.get('current_subscription', 'Standart')
        expires = user_purchases.get('expires', 'Не ограничено')
        
        account_text = f"""
📊 **Ваш аккаунт**

👤 Имя: {user.first_name}
🆔 ID: {user_id}
💎 Текущая подписка: {current_sub}
📅 Действует до: {expires}

Хотите продлить или сменить подписку? 
Выберите "💎 Подписки" в меню!
        """
    else:
        account_text = f"""
📊 **Ваш аккаунт**

👤 Имя: {user.first_name}
🆔 ID: {user_id}
💎 Текущая подписка: Базовый (бесплатная)

🎁 Для доступа к расширенным функциям 
выберите "💎 Подписки" в меню!
        """
    
    await update.message.reply_text(
        account_text,
        reply_markup=main_reply_markup,
        parse_mode='Markdown'
    )

async def show_about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать информацию о продукте"""
    about_text = """
ℹ️ **О продукте**

Joule-Bot - помощник в решении инженерных задач по электротехнике и электронике.

🌟 **Наши преимущества:**
• Простота использования
• Быстрые запросы
• Постоянные обновления

💡 Наша миссия - оперативно и точно помочь студентам технических специальностей в освоении ключевых дисциплин, таких как Электроника, Схемотехника, Физика, Цифровая схемотехника и смежные инженерные предметы!
    """
    
    await update.message.reply_text(
        about_text,
        reply_markup=main_reply_markup
    )

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик нажатий на инлайн-кнопки"""
    query = update.callback_query
    await query.answer()
    
    callback_data = query.data
    user_id = query.from_user.id
    
    if callback_data.startswith('paid_'):
        # Пользователь нажал "Я оплатил"
        subscription_type = callback_data.replace('paid_', '')
        await query.edit_message_text(
            f"✅ Заявка принята! Проверяем оплату подписки {SUBSCRIPTIONS[subscription_type]['name']}...\n\n"
            "Обычно это занимает несколько минут. Вы получите уведомление, когда оплата будет подтверждена.",
            parse_mode='Markdown'
        )
        
    elif callback_data.startswith('get_free_'):
        # Пользователь нажал "Получить бесплатно"
        subscription_type = callback_data.replace('get_free_', '')
        
        # Сохраняем информацию о "покупке"
        purchases = load_purchases()
        if str(user_id) not in purchases:
            purchases[str(user_id)] = {}
        
        purchases[str(user_id)]['current_subscription'] = SUBSCRIPTIONS[subscription_type]['name']
        purchases[str(user_id)]['expires'] = 'Не ограничено'
        save_purchases(purchases)
        
        await query.edit_message_text(
            f"🎉 Поздравляем! Вы получили подписку {SUBSCRIPTIONS[subscription_type]['name']}!\n\n"
            "Теперь вам доступны все функции этой подписки. "
            "Для управления подпиской зайдите в раздел '📊 Мой аккаунт'.",
            parse_mode='Markdown'
        )

def main():
    """Основная функция запуска бота"""
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Добавляем обработчики
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Обработчик инлайн-кнопок
    from telegram.ext import CallbackQueryHandler
    app.add_handler(CallbackQueryHandler(handle_callback))
    
    print("Joule Bot запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()