# website_monitoring
Cyber Security Assignment

Client-side website monitoring

# Telegram Bot Setup:
1. Create a bot using [BotFather](https://core.telegram.org/bots#botfather).
2. Add your bot token and chat ID in `utils.py`:
   ```python
   TELEGRAM_BOT_TOKEN = 'your_bot_token_here'
   TELEGRAM_CHAT_ID = 'your_chat_id_here'
   ```
3. chat_id can be taken by running ```python bot_helper.py```

# Set up steps:

1. ```pip install -r requirements.txt```
2. edit ```urls_to_care_about``` in const.py, adding your website's permalink to the list
3. register with the system by running ```python register_url.py```

# Detection:
- For testing, you can run Single-time detection by:
```python watcher.py```
- Or you can run Scheduled Detect Task:
```python schedule_watch.py```

Any changes will be messaged to Telegram

