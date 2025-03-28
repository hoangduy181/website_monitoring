from telegram import Bot
from utils import TELEGRAM_BOT_TOKEN
import asyncio
bot = Bot(token=TELEGRAM_BOT_TOKEN)

async def get_conversations():
    conversations = await bot.get_updates()
    conversation_ids = []
    conversation_unique = []
    for conversation in conversations:
        if conversation.message.chat.id not in conversation_ids:
            conversation_ids.append(conversation.message.chat.id)
            conversation_unique.append({
                "id":conversation.message.chat.id,
                "username":conversation.message.chat.username
            })
    return conversation_unique

if __name__ == '__main__':
    print(asyncio.run(get_conversations()))
