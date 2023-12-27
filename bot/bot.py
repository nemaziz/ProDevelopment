import logging
from random import shuffle
import io

from telegram import Update, ForceReply, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

# включаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

API = '5853948181:AAFCdjcHKKTRn3YG3QvJpjtA-Hy_Wn2PKSY'

old_images = [f'Рисунок{i}.jpg' for i in range(1, 9)]
images = [f'Рисунок{i}.jpg' for i in range(1, 9)]


# это обработчики команд (handler-ы). Обычно приниают вот эти два параметра, которые содержат нужный
# контекст, то есть необъодимые для нас переменные (типа, имени пользователя, его ID и так далее), и
# созданный нами движок (об этом ниже)

# вот обработчик команды /start. Когда пользователь вводит /start, вызывается эта функция
# то же самое происходит, если пользователь выберет команду start из списка команд (это
# сделаем позже в BotFather)

def send_keyword(engine: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("Вариант сверху", callback_data="up"),
        ],
        [
            InlineKeyboardButton("Вариант снизу", callback_data="down")
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    engine.message.reply_text("Выберите лучший вариант:", reply_markup=reply_markup)

def start(engine: Update, context: CallbackContext) -> None:
    # получаем имя пользователя, которое он указал у себя в настройках телеграма,
    # из нашего "движка"
    user = engine.effective_user
    message = engine.effective_message
    # отправляем нашему пользователю приветственное сообщение
    if message['text'] == '/start':
        engine.message.reply_text(
            f'''Привет, {user.first_name}!\nЯ бот компании ПROДевелопмент!\n\nВам будет представлен ряд дизайнов домов. Ваша задача - выбрать тот, который вам больше нравится. Продолжайте выбор, пока не останется один дизайн.\nВ конце вы сможете посмотреть на дом своей мечты! Чтобы начать заново отправьте команду \\restart'''
        )
    else:
        engine.message.reply_text("Давайте начнем заново!")
        
    
    global images, old_images
    if len(images) != old_images:
        images = [] + old_images
        print('add', images)
    
    shuffle(images)
    send_picture(engine, context)

def button(engine: Update, context: CallbackContext) -> None:
    
    """Parses the CallbackQuery and updates the message text."""
    query = engine.callback_query
    
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

#     query.message.reply_text(f"option: {query.data}")
    if query.data == 'up':
        images.pop(1)
    else:
        images.pop(0)
    
    send_picture(query, context)



def send_picture(engine: Update, context: CallbackContext) -> None:
    if len(images) != 1:
        pictureup = fr'pictures\{images[0]}'
        engine.message.reply_photo(open(pictureup, 'rb'))
        picturedown = fr'pictures\{images[1]}'
        engine.message.reply_photo(open(picturedown, 'rb'))
        send_keyword(engine, context)
    else:
        pictureup = fr'pictures\{images[0]}'
        engine.message.reply_photo(open(pictureup, 'rb'),
                                  caption = "Поздравляем! Ваш дом мечты:")
    print(images)


def echo(engine: Update, context: CallbackContext) -> None:
    # вызываем команду отправки сообщения пользователю, используя
    # при это текст сообщения, полученный от пользователя
    engine.message.reply_text(f'Не совсем вас понял. ' +
                              'Вы можете выбрать дизайн дома на предыдущем шаге, либо начать заново с помощью \start')
    

def main() -> None:
    # создаем объект фреймворка (библиотеки) для создания телеграм-ботов, с помощью
    # которого мы сможем взаимодействовать с фреймворком, то есть тот связующий объект,
    # через который мы будем общаться со всеми внутренностями (которые делают основную
    # работу по отправке сообщений за нас) фреймворка. Причем, общаться будем в обе стороны:
    # принимать сообщения от него и задавать параметры для него
    #
    # я назвал его engine (движок), чтобы было понятнее. В самой либе (библиотеке, фреймворке)
    # он называется Updater, как видно, что немного запутывает
    engine = Updater(API)

    # получаем объект "передатчика" или обработчика сообщений от нашего движка
    dispatcher = engine.dispatcher
    
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("restart", start))
    dispatcher.add_handler(CallbackQueryHandler(button))
    
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))


    # непосредственно старт бота
    engine.start_polling()
    engine.idle()



if __name__ == '__main__':
    main()