from aiogram.dispatcher.filters.state import StatesGroup, State


class ProductStateEdited(StatesGroup):
    title_edited = State()
    body_edited = State()
    image_edited = State()
    price_edited = State()
