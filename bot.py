import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import dateparser
from db import init_db, add_deadline, get_all_deadlines, delete_deadline

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = 5909931243


def get_next_weekday_occurrence(dt):
    """Get the next occurrence of a weekday-based datetime."""
    now = datetime.now()
    target_weekday = dt.weekday()
    days_ahead = target_weekday - now.weekday()
    if days_ahead < 0:
        days_ahead += 7
    elif days_ahead == 0:
        target_time = dt.replace(year=now.year, month=now.month, day=now.day)
        if target_time <= now:
            days_ahead = 7
    next_date = now + timedelta(days=days_ahead)
    return next_date.replace(hour=dt.hour, minute=dt.minute, second=0, microsecond=0)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I track deadlines.")


async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != OWNER_ID:
        await update.message.reply_text("Only admin can add deadlines.")
        return

    text = update.message.text.replace("/add ", "")
    parts = [p.strip() for p in text.split("|")]

    if len(parts) < 4:
        await update.message.reply_text(
            "Format: /add class | name | start | due | link (optional)"
        )
        return

    class_name = parts[0]
    name = parts[1]
    start = dateparser.parse(parts[2])
    due = dateparser.parse(parts[3])
    link = parts[4].strip() if len(parts) > 4 and parts[4].strip() else None
    recurring = parts[5].strip().lower() if len(parts) > 5 and parts[5].strip() else None

    if recurring and recurring != "weekly":
        await update.message.reply_text("Only 'weekly' recurring is supported.")
        return

    if not start:
        await update.message.reply_text("Couldn't understand start date.")
        return

    if not due:
        await update.message.reply_text("Couldn't understand due date.")
        return

    add_deadline(name, class_name, start, due, link, recurring)
    msg = f"Got it ✓\n{class_name} — {name}\n🟢 {start.strftime('%b %d %I:%M %p')}\n🔴 {due.strftime('%b %d %I:%M %p')}"
    if recurring:
        msg += f"\n🔁 {recurring}"
    await update.message.reply_text(msg)


async def list_deadlines(update: Update, context: ContextTypes.DEFAULT_TYPE):
    deadlines = get_all_deadlines()

    if not deadlines:
        await update.message.reply_text("No deadlines 🎉")
        return

    text = update.message.text.replace("/list", "").strip()
    is_owner = update.message.from_user.id == OWNER_ID

    if text:
        if text == "id" and is_owner:
            lines = ["Deadlines with IDs:\n"]
            for id, name, class_name, start, due, link, recurring in deadlines:
                start_dt = dateparser.parse(start)
                due_dt = dateparser.parse(due)
                if recurring == "weekly":
                    start_dt = get_next_weekday_occurrence(start_dt)
                    due_dt = get_next_weekday_occurrence(due_dt)
                start_formatted = start_dt.strftime("%b %d, %I:%M %p")
                due_formatted = due_dt.strftime("%b %d, %I:%M %p")
                line = f"ID: {id}\n  📝 {name}"
                if recurring:
                    line += " 🔁"
                line += f"\n  🟢 {start_formatted}\n  🔴 {due_formatted}"
                if link:
                    line += f"\n  🔗 {link}"
                lines.append(line)
                lines.append("")
            await update.message.reply_text("\n".join(lines))
            return

        deadlines = [d for d in deadlines if d[2].lower() == text.lower()]
        if not deadlines:
            await update.message.reply_text(f"No deadlines for {text}")
            return

    grouped = {}
    for id, name, class_name, start, due, link, recurring in deadlines:
        if class_name not in grouped:
            grouped[class_name] = []
        grouped[class_name].append((id, name, start, due, link, recurring))

    lines = []
    for class_name, items in grouped.items():
        lines.append(f"📚 {class_name}\n")
        for id, name, start, due, link, recurring in items:
            start_dt = dateparser.parse(start)
            due_dt = dateparser.parse(due)
            if recurring == "weekly":
                start_dt = get_next_weekday_occurrence(start_dt)
                due_dt = get_next_weekday_occurrence(due_dt)
            start_formatted = start_dt.strftime("%b %d, %I:%M %p")
            due_formatted = due_dt.strftime("%b %d, %I:%M %p")
            line = f"  📝 {name}"
            if recurring:
                line += " 🔁"
            line += f"\n  🟢 {start_formatted}\n  🔴 {due_formatted}"
            if link:
                line += f"\n  🔗 {link}"
            lines.append(line)
            lines.append("")
        lines.append("━━━━━━━━━━━━━━━\n")

    lines = lines[:-1]

    await update.message.reply_text("\n".join(lines))


async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != OWNER_ID:
        await update.message.reply_text("Only admin can delete deadlines.")
        return

    text = update.message.text.replace("/delete", "").strip()

    if not text:
        await update.message.reply_text("Format: /delete id\n\nUse /list to see IDs.")
        return

    try:
        id = int(text)
    except ValueError:
        await update.message.reply_text("ID must be a number.")
        return

    delete_deadline(id)
    await update.message.reply_text("Deleted ✓")


def main():
    init_db()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add))
    app.add_handler(CommandHandler("list", list_deadlines))
    app.add_handler(CommandHandler("delete", delete))
    app.run_polling()


if __name__ == "__main__":
    main()
