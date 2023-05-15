from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

# =========================================================================

button_help = KeyboardButton('/help')
button_voda = KeyboardButton('/voda')

button_row = ReplyKeyboardMarkup(resize_keyboard=True).row(
    button_help, button_voda
)

# Затравка на будущее
# inline_btn_1 = InlineKeyboardButton('Первая кнопка!', callback_data='button1')
# inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)


# =========================================================================
