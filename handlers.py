from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from utils.get_data import get_earning_data, get_total_ips
from datetime import datetime

user_tokens = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [KeyboardButton("/authorization"), KeyboardButton("/viewauthorization")],
        [KeyboardButton("/changeauthorization"), KeyboardButton("/removeauthorization")],
        [KeyboardButton("/checkearning")], [KeyboardButton("/help")]
    ]
    
    await update.message.reply_text(
        "Sup! This is a notification bot for app.getgrass.io\n\n"
        "This bot provides real-time earnings updates for your GRASS account. Here's how it works:\n\n"
        "💼 Add Your Authorization Token: You can link your GRASS account by adding your authorization token. "
        "This token allows the bot to fetch your earnings data directly from https://app.getgrass.io/.\n\n"
        "📊 Get Earnings Updates: Once your token is added, the bot will send you regular earnings updates. "
        "You will receive notifications twice a day at 12:00 AM and 12:00 PM (UTC).\n\n"
        "🔄 Change or Remove Token: You can easily update or remove your token if necessary. Just use the /changeauthorization or /removeauthorization commands.\n\n"
        "📑 View Your Token: Want to see which token is linked? Use the /viewauthorization command to check your current token.\n\n"
        "Let's get started! 🚀 , /help"
        "\n\nhttps://github.com/adityafajrip",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

async def add_authorization(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    if chat_id in user_tokens:
        await update.message.reply_text("You have already added an Authorization Token.")
    else:
        await update.message.reply_text("Please enter your Authorization Token:")
        context.user_data["waiting_for_token"] = True

async def handle_authorization(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    
    # Checking
    if "waiting_for_token" in context.user_data and context.user_data["waiting_for_token"]:
        authorization_token = update.message.text
        user_tokens[chat_id] = authorization_token
        context.user_data["waiting_for_token"] = False
        await update.message.reply_text("Authorization Token received and saved.")
    else:
        await update.message.reply_text(
            "Bruh really? check your token now!. Please use /authorization to add your token."
        )

async def view_authorization(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    if chat_id in user_tokens:
        await update.message.reply_text(f"Your saved Authorization Token is: {user_tokens[chat_id]}")
    else:
        await update.message.reply_text("You have not saved an Authorization Token yet. Use /authorization to add one.")

async def change_authorization(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    if chat_id in user_tokens:
        await update.message.reply_text("Please enter your new Authorization Token:")
        context.user_data["waiting_for_token"] = True
    else:
        await update.message.reply_text("No Authorization Token found. Use /authorization to add one.")

async def remove_authorization(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    if chat_id in user_tokens:
        del user_tokens[chat_id]
        await update.message.reply_text("Your Authorization Token has been removed.")
    else:
        await update.message.reply_text("No Authorization Token found to remove.")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    gif_path = 'assets/tutorial.gif'
    
    await update.message.reply_text(
        "Please wait while I send you the tutorial GIF. It may take a few moments."
    )
    await update.message.reply_animation(
        animation=open('assets/tutorial.gif', 'rb'),
        caption="Here's the tutorial on how to get your token."
    )

def convert_uptime_seconds(total_uptime_seconds):
    days = total_uptime_seconds // 86400
    hours = (total_uptime_seconds % 86400) // 3600
    minutes = (total_uptime_seconds % 3600) // 60
    seconds = total_uptime_seconds % 60

    return f"{days}d {hours}h {minutes}m {seconds}s"

# Format Date
def format_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%d %B %Y") 
    except ValueError:
        return date_str

async def check_earning(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    user_name = update.message.from_user.username

    print(f"Fetching data for user with chat_id: {chat_id} ({user_name})") 

    if chat_id in user_tokens:
        print(f"Token found for user {chat_id}. Retrieving earnings data...")
        authorization_token = user_tokens[chat_id]
        print(f"Fetching data with authorization token for user {chat_id}.")

        total_earning, today_earning, start_date, end_date, epoch_name, total_uptime = get_earning_data(authorization_token)
        total_ips = get_total_ips(authorization_token)

        if total_earning is not None:
            print(f"Earnings fetched for user {chat_id}: Total earnings: {total_earning}, Today's earnings: {today_earning}")
            start_date = format_date(start_date)
            end_date = format_date(end_date)
            formatted_uptime = convert_uptime_seconds(total_uptime)
            message = (
                f"<b>🔮 Stage 2:</b> <code>{epoch_name}</code>\n"
                f"<b>🗓️ Period:</b> <code>{start_date} - {end_date}</code>\n"
                f"\n"
                f"<b>💰 Today's Earning:</b> <code>{today_earning}</code>\n"
                f"<b>📊 Total Earning:</b> <code>{total_earning}</code>\n"
                f"<b>⏱️ Total Uptime:</b> <code>{formatted_uptime}</code>\n"
            )
        else:
            print(f"No earnings data found for user {chat_id}.") 
            message = (
                "<b>Unable to fetch earnings data at this time:</b>\n"
                "<b>- Invalid token</b>\n"
                "<b>- Network issues</b>\n"
                "<b>- Server maintenance</b>\n"
                "<b>Please double-check and try again later.</b>"
            )
        if total_ips:
            print(f"Found {len(total_ips)} active networks for user {chat_id}.")
            message += f"\n<b>🌐 Total Active Networks:</b> <code>{len(total_ips)}</code>"
        else:
            print(f"No active networks found for user {chat_id}.")
            message += "\n<b>No active Networks found or unable to fetch data.</b>"

        if total_ips:
            ips_with_zero_score = [
                ip_data for ip_data in total_ips if ip_data.get('ipScore') == 0
            ]
            if ips_with_zero_score:
                print(f"Found {len(ips_with_zero_score)} IPs with 0 network score for user {chat_id}.")
                message += "\n⚠️ <b>IPs with 0 Network Score :</b>\n"
                for ip in ips_with_zero_score:
                    message += f"<code>{ip['ipAddress']}</code>\n"
            else:
                print(f"No IPs with score 0 for user {chat_id}.")

        await update.message.reply_text(message, parse_mode="HTML")
    else:
        print(f"Token not found for user {chat_id}.")
        await update.message.reply_text("Please save your Authorization Token first using /authorization.")