# Deadline Bot

Telegram bot for tracking deadlines.

## Setup

```bash
uv sync
```

Create `.env`:
```
BOT_TOKEN=your_token_here
```

Run:
```bash
python bot.py
```

## Commands

```
/add Math | HW 5 | Mon 9am | Fri 11pm
/add Math | HW 5 | Mon 9am | Fri 11pm | https://link.com
/add Math | HW 5 | Mon 9am | Fri 11pm | | weekly
/list
/list Math
/list id
/today
/soon
/delete id
```
