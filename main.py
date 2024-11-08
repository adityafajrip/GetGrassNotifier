import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from handlers import start, add_authorization, view_authorization, check_earning, handle_authorization, change_authorization, remove_authorization, user_tokens
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import asyncio
from utils.get_data import get_earning_data
from handlers import format_date
from handlers import convert_uptime_seconds
from config import TELEGRAM_BOT_TOKEN
from handlers import help


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Send notif
async def send_earning_notification(application):
    logger.info("Sending notification to user")
    for chat_id in user_tokens:
        authorization_token = user_tokens[chat_id]
        total_earning, today_earning, start_date, end_date, epoch_name, total_uptime = get_earning_data(authorization_token)
        
        if total_earning is not None and today_earning is not None:
            formatted_start_date = format_date(start_date)
            formatted_end_date = format_date(end_date)

            formatted_uptime = convert_uptime_seconds(total_uptime)
            message = (
                f"🚨 <b>Your GetGrass Points have been updated!!!</b>🚨\n"
                f"🔮 <b>Stage 2:</b> <code>{epoch_name}</code>\n"
                f"📆 <b>Period:</b> <code>{formatted_start_date} - {formatted_end_date}</code>\n"
                f"\n"
                f"💰 <b>Today's Earning:</b> <code>{today_earning}</code>\n"
                f"📊 <b>Total Earning:</b> <code>{total_earning}</code>\n"
                f"⏱️ <b>Total Uptime:</b> <code>{formatted_uptime}</code>\n"
                f"\n"
                f"<i>🔔 Stay tuned for your next earning update!</i>"
            )
            await application.bot.send_message(chat_id=chat_id, text=message, parse_mode="HTML")
        else:
            await update.message.reply_text(
        "<b>Unable to fetch earnings data at this time:</b>\n"
        "<b>- Invalid token</b>\n"
        "<b>- Network issues</b>\n"
        "<b>- Server maintenance</b>\n"
        "<b>Please double-check and try again later.</b>",
        parse_mode='HTML'
)

# Scheduler
def schedule_notifications(application):
    scheduler = AsyncIOScheduler(timezone='Asia/Jakarta') #Change timezone
    loop = asyncio.get_event_loop()

    scheduler.add_job(
        lambda: loop.create_task(send_earning_notification(application)),
        CronTrigger(hour=7, minute=0
        ) 
    )
    
    scheduler.add_job(
        lambda: loop.create_task(send_earning_notification(application)),
        CronTrigger(hour=19, minute=0) 
    )
    
    scheduler.start()

def main():
    """Start the bot."""
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("authorization", add_authorization))
    application.add_handler(CommandHandler("viewauthorization", view_authorization))
    application.add_handler(CommandHandler("changeauthorization", change_authorization))
    application.add_handler(CommandHandler("removeauthorization", remove_authorization))
    application.add_handler(CommandHandler("checkearning", check_earning))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_authorization))

    schedule_notifications(application)
    application.run_polling()

if __name__ == '__main__':
    main()
