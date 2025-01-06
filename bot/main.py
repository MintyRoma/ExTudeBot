import logging
from telegram import Update
from telegram.ext import *
from config import Config
from handlers import *

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

def main():
    calls.initdb()
    app = Application.builder().token(Config.TELEGRAM_TOKEN).build()
    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            DialogState.INIT:[
                CallbackQueryHandler(start_choose_callback)
            ],
            DialogState.LIST_ALL:[
                CallbackQueryHandler(list_all_callback)
            ],
            DialogState.CREATE_ETUDE:[
                CallbackQueryHandler(create_etude_callback),
                MessageHandler(filters=filters.TEXT,callback=create_etude_message_callback)
            ],
            DialogState.ADD_ROLES:[
                CallbackQueryHandler(addroles_callback),
                MessageHandler(filters=filters.TEXT,callback=addroles_message_callback)
            ]
        },
        fallbacks=[CommandHandler("start", start)],
    )
    app.add_handler(conv)
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()