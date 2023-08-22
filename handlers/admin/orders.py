from itertools import zip_longest

from aiogram.types import Message

from loader import dp, db, bot
from handlers.user.menu import orders
from filters import IsAdmin


@dp.message_handler(IsAdmin(), text=orders)
async def process_orders(message: Message):
    
    orders_awaiting = list(db.fetchall('SELECT * FROM orders'))
    photos = [order[3] for order in orders_awaiting]
    photos = [photo.split() for photo in photos]
    titles = [title[-1] for title in orders_awaiting]
    titles = [title.split(';') for title in titles]
    new_photos = []
    photos_orders = []
    for i in photos:
        for j in i:
            new_photos.append(j.split('='))
        photos_orders += [new_photos]
        new_photos = []
    title_joined = ''
    title = []
    for m, n in zip(titles, photos_orders):
        for i, j in zip(m, n):
            title_joined += f'{i} в количестве: {j[-1]} \n'
        title.append(title_joined)
        title_joined = ''
    if len(orders_awaiting) == 0:
        await message.answer('У вас нет заказов.')
    else:
        await order_answer(message, orders_awaiting, title)


async def order_answer(message, orders_awaiting, titles):
    res = ''
    for order, title in zip(orders_awaiting, titles):
        # photo = db.fetchone(f'SELECT photo FROM products WHERE idx = ?', (i[0], ))
        res = f'Заказ: <b>Номер чата {str(order[0])}</b>\n\n' \
              f'Имя: <b>{order[1]}</b>\n\n' \
              f'Адрес: <b>{order[2]}</b>\n\n' \
              f'Пожелание к Заказу: \n<b>{order[4]}</b>\n\n' \
              f'Номер телефона: <b>{order[-2]}</b>\n\n' \
              f'<b>Заказано:\n</b>' \
              f'{title}'
        print('title', title)
        await message.answer(res)

        # TODO: добавить изменение статуса заказа и отправка его пользователю
        # await message.answer_photo(photo=photo[0],
        #                           caption=f'Наименование: {order[-1]}'\
        #                                   f'В количестве: {i[-1]}')
