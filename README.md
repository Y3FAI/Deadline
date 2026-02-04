# Deadline Bot

Telegram bot for tracking deadlines.

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

## Commands

| Command | Description |
|---------|-------------|
| /list | All deadlines |
| /list Math | Filter by class |
| /list id | Show IDs (admin) |
| /today | Due today |
| /week | Due this week |
| /month | Due this month |
| /add | Add deadline (admin) |
| /delete id | Delete deadline (admin) |

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
