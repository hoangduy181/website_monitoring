# Website Monitoring System

A Python-based system that monitors websites for changes and sends notifications via Telegram. This project is part of a Cyber Security Assignment.

## Features

- Real-time website monitoring
- Detection of website content changes
- Multiple website monitoring support
- Telegram notifications for all detected changes
- Scheduled checks
- Baseline website state tracking

## Prerequisites

- Python 3.x
- Telegram Bot Token
- Telegram Chat ID
- List of websites to monitor

## Installation

1. Clone the repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Set up your Telegram Bot:
   - Create a new bot using [@BotFather](https://t.me/botfather) on Telegram
   - Get your bot token
   - Get your chat ID by running:
     ```bash
     python bot_helper.py
     ```
   - Update the following variables in `utils.py`:
     ```python
     TELEGRAM_BOT_TOKEN = 'your_bot_token_here'
     TELEGRAM_CHAT_ID = 'your_chat_id_here'
     ```

2. Configure websites to monitor:
   - Edit `urls_to_care_about` in `const.py`
   - Add your website's permalink to the list
   - Example:
     ```python
     urls_to_care_about = [
         'https://example.com',
         'https://another-example.com'
     ]
     ```

## Usage

1. Register websites with the system:
   ```bash
   python register_url.py
   ```
   This will create baseline data for all configured websites.

2. Choose your monitoring method:

   a. Single-time detection (for testing):
   ```bash
   python watcher.py
   ```

   b. Scheduled monitoring:
   ```bash
   python schedule_watch.py
   ```

## File Structure

- `const.py`: Contains configuration constants and URLs to monitor
- `utils.py`: Utility functions and Telegram bot configuration
- `bot_helper.py`: Helper script to get Telegram chat ID
- `register_url.py`: Generates initial baseline for websites
- `watcher.py`: Core website monitoring logic
- `schedule_watch.py`: Handles scheduled monitoring tasks
- `requirements.txt`: Lists all project dependencies

## Notifications

The system sends notifications via Telegram when changes are detected on any monitored website. The notification includes:
- Timestamp of detection
- Website URL where changes were detected
- Type of changes detected

## Security Features

- Secure website content comparison
- Error handling for website access issues
- Safe storage of baseline data
- Protected Telegram bot communication

## Error Handling

The system includes error handling for:
- Website connection issues
- Invalid URLs
- Telegram API communication problems
- Network timeouts
- Invalid response formats

## Contributing

Feel free to submit issues and enhancement requests!

