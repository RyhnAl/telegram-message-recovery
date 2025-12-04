# Telegram Deleted Messages Logger
A Python tool built with **Telethon** that logs **deleted Telegram messages** from private chats and groups.
When a user deletes a message, the script retrieves it from the cache and sends the recovered content to a specified chat or channel.

---

## Features
- 🔹 Logs all incoming messages before deletion
- 🔹 Detects deleted messages in private chats and groups
- 🔹 Sends deleted messages to your chosen chat/channel
- 🔹 Includes message metadata:
    - Sender username / name
    - Group title (if any)
- 🔹 24-hour cache system to prevent memory overflow
- 🔹 Proxy support (MTProxy)
- 🔹 Cache size limited to prevent RAM usage issues

---

## Requirements
Install Telethon:
```bash
pip install telethon
```
---

## Installation & Running
1. Clone this repository
```bash
git clone https://github.com/YOUR_USERNAME/telegram-message-recovery.git
cd telegram-message-recovery
```
2. Run the script
```bash
python main.py
```
You should see:
```bash
bot is working...
```

---

## How It Works?
1. Message Caching
```bash
@client.on(events.NewMessage())
async def saved(event):
```
Every new incoming message gets stored in a cache with a timestamp.

2. Detecting Deleted Messages
```bash
@client.on(events.MessageDeleted())
async def handler(event):
```
When Telegram reports a deletion, the script retrieves that message from the cache and forwards it to your chosen chat.

---

## Example Output
```bash
this message deletes from : zahra
group name? : Family Group
Hi
```
