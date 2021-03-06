import logging      # Ayuda a ver lo que sucede con el bot y mostrarlo en consola
import telegram
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters

# Variables
TOKEN = '1862455246:AAHDE6lLYMHHYk7-p_rBSgf_L3CYRkO4IYA'

# Configuracion de logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s,"
)
logger = logging.getLogger()

# Funciones para comandos
def start(update, context):
    bot = context.bot
    # chat_Id = update.message.chat_id
    user_Name = update.effective_user["first_name"]
    logger.info(f'El usuario {user_Name} ha iniciado(/start) el bot')   # Consola

    # Botones
    btn_contacto = InlineKeyboardButton(
        text='鉁夛笍 Contacto de EPCC',
        callback_data="contacto"
    )
    btn_tramites = InlineKeyboardButton(
        text='馃帗 Informaci贸n de tr谩mites',
        callback_data="tramite"
    )

    # Lo que se muestra al ejecutar el comando /start
    update.message.reply_text(
        text=f'Hola {user_Name} 鈽猴笍.\nGracias por usar nuestro bot 馃. '
             f'A continuaci贸n te mostramos los tipos de informaci贸n que podemos darte.\n'
             f'S贸lo toca la opci贸n que te interesa.',
        reply_markup=InlineKeyboardMarkup([
            [btn_contacto],
            [btn_tramites]
        ])
    )

def getBotInfo(update, context):
    bot = context.bot
    chat_Id= update.message.chat_id
    user_Name = update.effective_user["first_name"]
    logger.info(f'El usuario {user_Name} ha solicitado informaci贸n sobre el bot')
    bot.sendMessage(
        chat_id=chat_Id,
        parse_mode="HTML",
        text=f'Hola soy el bot 馃 de la <b>Escuela Profesional de Ciencia de la Computaci贸n - UNSA</b>.'
             f'Si necesitas informaci贸n sobre tr谩mites de Bachiller y T铆tulo Profesional '
             f'puedo ayudarte. Comienza escribiendo /start.' # 2da manera de responder
    )

# Callbacks functions
def tramites_callback_handler(update, context):
    # print(update.callback_query)
    query = update.callback_query   # Recibe el mensaje
    query.answer()  # Requerido. Responde silenciosamente

    query.edit_message_text(
        parse_mode='HTML',
        text=' <b>INFORMACI脫N DE CONTACTO DE LA EPCC</b>\n'
    )

# Main Function
if __name__ == '__main__':
    mybot = telegram.Bot(token=TOKEN)
    print(mybot.getMe())  # Muestra en consola informaci贸n sobre el bot

    # Updater: se conecta y recibe los mensajes
    updater = Updater(mybot.token, use_context=True)

    # Crear el 'despachador'
    dp = updater.dispatcher

    # Crear comando y el m茅todo (acci贸n del comando)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("botInfo", getBotInfo))

    # Crear el callback handler
    dp.add_handler(ConversationHandler(
        entry_points=[
            # Al recibir el patron definido en el data del bot贸n ejecuta la funcion callback
            CallbackQueryHandler(pattern='contacto', callback=tramites_callback_handler)
        ],
        states={},
        fallbacks=[]
    ))

    # Preguntar por mensajes entrantes
    updater.start_polling()

    # Terminar bot con ctrl + c
    updater.idle()