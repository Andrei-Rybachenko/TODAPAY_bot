from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_main_menu():
    keyboard = [
        [InlineKeyboardButton(text="📌 Who we are", callback_data="who_we_are")],
        [InlineKeyboardButton(text="👥 Join our team", callback_data="join_team")],
        [InlineKeyboardButton(text="🌐 Social media", callback_data="social_media")],
        [InlineKeyboardButton(text="📞 Hot-line", callback_data="hotline")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
