from create_bot import dp, bot
import hashlib
from aiogram.types import InlineQuery, \
    InputTextMessageContent, InlineQueryResultArticle

async def inline_echo(inline_query: InlineQuery):
    print('sdfdsfdsf')
    # id affects both preview and content,
    # so it has to be unique for each result
    # (Unique identifier for this result, 1-64 Bytes)
    # you can set your unique id's
    # but for example i'll generate it based on text because I know, that
    # only text will be passed in this example
    text = inline_query.query or 'echo'
    input_content = InputTextMessageContent(text)
    result_id: str = hashlib.md5(text.encode()).hexdigest()
    item = InlineQueryResultArticle(
        id=result_id,
        title=f'Result {text!r}',
        input_message_content=input_content,
    )
    # don't forget to set cache_time=1 for testing (default is 300s or 5m)
    await bot.answer_inline_query(inline_query.id, results=[item], cache_time=1)

def register_handlers_inline(dp):
    dp.register_inline_handler(inline_echo)