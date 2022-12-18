from create_bot import dp, bot
import random
import hashlib
from aiogram.types import InlineQuery, \
    InputTextMessageContent, InlineQueryResultArticle
epithets = ['ёлочки 🌲', 'сосульки 🧊', 'колокольчика 🔔', 'мишуры 🎊', 'морковки ⛄️','имбирного пряника 🥮','петарды 🧨','фейерверка 🎆','бенгальского огонька 🎇','игрушки 🐰','волшебства 🪄', 'подарочка 🎁', 'мандаринки 🍊', 'гирлянды 💡', 'леденца 🍭']
async def inline_echo(inline_query: InlineQuery):
    print('отработала инлайн функция')
    cocksize_len = random.randint(1, 50)
    epithet = random.choice(epithets)
    text = 'Мой размер ' + epithet + ': ' + str(cocksize_len) + ' см'
    # text = str(cocksize_len) or 'Не могу разглядеть'
    input_content = InputTextMessageContent(text)
    result_id: str = hashlib.md5(text.encode()).hexdigest()
    item = InlineQueryResultArticle(
        id=result_id,
        title=f'Ну давай, покажи свой размер {epithet}',
        input_message_content=input_content,
    )
    # don't forget to set cache_time=1 for testing (default is 300s or 5m)
    await bot.answer_inline_query(inline_query.id, results=[item], cache_time=1)

def register_handlers_inline(dp):
    dp.register_inline_handler(inline_echo)