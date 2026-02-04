# Deadline Bot

I built this because I kept worrying about assignment deadlines while studying at university. When you have 6 classes with quizzes, assignments, and projects, keeping track of everything is a nightmare.

So I made a simple Telegram bot that lives in my university group chat. I add deadlines once, and it handles the rest. It reminds me 24 hours before something is due, again at 1 hour, and sends a weekly summary every Saturday so I can plan ahead.

Nothing fancy. It just works.

## Features

- Auto reminders sent to group chat (24h and 1h before due)
- Auto weekly summary every Saturday
- Convenient commands to see what's due today, this week, or upcoming
- Academic holidays calendar
- Easy admin commands to add/delete deadlines
- Flexible date parsing ("Mon 9am", "next Friday", etc.)
- Auto server deployment with GitHub Actions

## Setup

```bash
uv sync
```

Create `.env`:
```
BOT_TOKEN=your_token_here
OWNER_ID=123456789
CHAT_ID=123456789
TOPIC_ID=
```

Run:
```bash
uv run python bot.py
```

## Server Deployment

```bash
sudo cp deadline-bot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable deadline-bot
sudo systemctl start deadline-bot
```

**Commands:**
- Status: `sudo systemctl status deadline-bot`
- Logs: `sudo journalctl -u deadline-bot -f`
- Restart: `sudo systemctl restart deadline-bot`
- Stop: `sudo systemctl stop deadline-bot`

## Auto Deploy

Pushes to `main` auto-deploy via GitHub Actions.

Add these secrets to your repo (Settings → Secrets → Actions):
- `SERVER_IP`
- `SERVER_USER`
- `SSH_KEY`

## Commands

| Command | Description |
|---------|-------------|
| /list | All deadlines |
| /list Math | Filter by class |
| /list id | Show IDs (admin) |
| /today | Due today |
| /week | Due this week |
| /month | Due this month |
| /upcoming | Next 3 deadlines |
| /holidays | Academic holidays |
| /add | Add deadline (admin) |
| /delete id | Delete deadline (admin) |
| /test | Test notification (admin) |

### Add examples

```
/add Math | HW 5 | Mon 9am | Fri 11pm
/add Math | HW 5 | Mon 9am | Fri 11pm | https://link.com
/add Math | HW 5 | Mon 9am | Fri 11pm | | weekly
```

## Auto Reminders

- 24h and 1h before due dates
- Weekly summary every Saturday at 5pm

---

Developed by [@y3fai](https://t.me/y3fai)
