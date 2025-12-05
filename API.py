from telethon import TelegramClient, events, connection
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
import asyncio
import time

api_id = 2040
api_hash = 'b18441a1ff607e10a989891a5462e627'
saved_messages_chat = 'https://t.me/+jbaN8KGTyQMyOWI0'

proxy = ('163.5.31.27', 8443 , 'EERighJJvXrFGRMCIMJdCQRueWVrdGFuZXQuY29tZmFyYWthdi5jb212YW4ubmFqdmEuY29tAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
client = TelegramClient('session_name', api_id, api_hash, connection=connection.ConnectionTcpMTProxyRandomizedIntermediate, proxy=proxy)

MAX_CACHE_SIZE = 6000
messages_cache = {}

@client.on(events.NewMessage())
async def saved(event):
    if event.is_private or event.is_group:
        if len(messages_cache) >= MAX_CACHE_SIZE:
            oldest_id = next(iter(messages_cache))
            messages_cache.pop(oldest_id, None)
        group_name = 'pv'
        sender = await event.get_sender()
        sender_name = sender.username or sender.first_name or "Unknown"
        if event.is_group:
            entity = await client.get_entity(event.chat_id)
            group_name = getattr(entity, "title", "pv")
        messages_cache[event.id] = {
            "message": event.message,
            "sender": sender_name,
            "group_name": group_name,
            "timestamp": time.time()
        }

        for msg_id in list(messages_cache):
            if time.time() - messages_cache[msg_id]["timestamp"] > 24*3600:
                messages_cache.pop(msg_id, None)

@client.on(events.MessageDeleted())
async def handler(event):
    for msg_id in event.deleted_ids:
        msg = messages_cache.pop(msg_id, None)
        if msg:
            try:
                text = msg["message"].message if msg["message"].message else "<media or empty message>"
                await client.send_message(
                    saved_messages_chat,
                    f"this message deletes from : {msg['sender']}\n"
                    f"group name? : {msg['group_name']}\n"
                    f"{text}"
                )
            except Exception as e:
                print(f"[!] Error sending deleted message {msg_id}: {e}")



async def main():
    await client.start()
    print(f"bot is working...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(main())