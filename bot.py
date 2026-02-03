import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import dateparser
from db import init_db, add_deadline, get_all_deadlines, delete_deadline

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = 5909931243


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
    link = parts[4] if len(parts) > 4 else None

    if not start:
        await update.message.reply_text("Couldn't understand start date.")
        return

    if not due:
        await update.message.reply_text("Couldn't understand due date.")
        return

    add_deadline(name, class_name, start, due, link)
    await update.message.reply_text(
        f"Got it ✓\n{class_name} — {name}\n🟢 {start.strftime('%b %d %I:%M %p')}\n🔴 {due.strftime('%b %d %I:%M %p')}"
    )


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
            for id, name, class_name, start, due, link in deadlines:
                start_formatted = dateparser.parse(start).strftime("%b %d, %I:%M %p")
                due_formatted = dateparser.parse(due).strftime("%b %d, %I:%M %p")
                line = f"ID: {id}\n  📝 {name}\n  🟢 {start_formatted}\n  🔴 {due_formatted}"
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
    for id, name, class_name, start, due, link in deadlines:
        if class_name not in grouped:
            grouped[class_name] = []
        grouped[class_name].append((id, name, start, due, link))

    lines = []
    for class_name, items in grouped.items():
        lines.append(f"📚 {class_name}\n")
        for id, name, start, due, link in items:
            start_formatted = dateparser.parse(start).strftime("%b %d, %I:%M %p")
            due_formatted = dateparser.parse(due).strftime("%b %d, %I:%M %p")
            line = f"  📝 {name}\n  🟢 {start_formatted}\n  🔴 {due_formatted}"
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
