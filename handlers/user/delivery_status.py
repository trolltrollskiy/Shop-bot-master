
from aiogram.types import Message
from loader import dp, db
from .menu import delivery_status
from filters import IsUser


@dp.message_handler(IsUser(), text=delivery_status)
async def process_delivery_status(message: Message):
    
    orders = db.fetchall('SELECT * FROM orders WHERE cid=?', (message.chat.id,))
    
    if len(orders) == 0:
        await message.answer('У вас нет активных заказов.')
    else:
        await delivery_status_answer(message, orders)


async def delivery_status_answer(message, orders):

    res = ''
    photos = [order[3] for order in orders]
    photos = [photo.split() for photo in photos]
    titles = [title[-1] for title in orders]
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
    for i in title:

        res += f'Заказ <b>\n{i}</b>'
        answer = [
            'лежит на складе.',
            'уже в пути!',
            'прибыл и ждет вас на почте!'
        ]
        # TODO: Добавить цену заказа в конечный итог и вывести
        res += answer[0]
        res += '\n\n'

    await message.answer(res)
