import logging

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from RoadmapSet import RoadmapSet





roadmap = RoadmapSet()


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

state = 0
i = 0
complete = False


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    global state, i
    state = 0
    i = 0
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\! ',
        reply_markup=ForceReply(selective=True),
    )
    update.message.reply_text('Here are the list of list of learning path I can help you with \n 1. Backend Development \n 2. DS_Algo \n 3. C++. \n Type the serial number of the learning path you want help with.')

def GivePath(i:int) -> str:
    pass


def reset_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Reseting')
    start(update,context)


def Handlestart(s):
    global state
    global roadmap

    try:
        i = int(s)
    except:
        return "Not a valid Input"

    state = 1
    roadmap.set(str(i))

    return roadmap.list_all() + "\n Ender the topic number which you have covered seperated by commas \n"

def HandleListofcoveredtopics(s):
    global state
    global roadmap
    for i in s.split(","):
        i = i.strip()
        roadmap.done(i)

    state = 2

    return "Now please provide the time(in days) you plan to cover the entire roadmap in"

def HandleTime(s):
    global state
    global roadmap

    try:
        i = int(s) 
    except:
        return "Not a valid Input"

    state = 3
    roadmap.Estimate_Time(i)
    return "We are now preparing your roadmap. When you are ready to start. Please type next to see you your first target " 


def HandleNext(s:str):
    global i
    global state, roadmap
    if(s.lower() == "next"):
        output = roadmap.next()
        if(output == ""):
            state = 4
            return "Congratulation You have completed the roadmap"
        elif i == 1:
            i = i + 1
            return "Congratulation for completing your first target. You next target is" + output
        elif i == 0:
            i = i + 1
            return "You first target is" + output
        else:
            return "Congratulation for completing your previous target. You next target is" + output
        

    else:
        return "Please type next to move or /reset to again start from begining"
    

def HandleAllDone(s):
    return "You have completed all the topics please type /reset to restart"



def CarryForward(update: Update, context: CallbackContext) -> None:
    statedict = {
        0: "Handlestart",
        1: "HandleListofcoveredtopics",
        2: "HandleTime",
        3: "HandleNext",
        4: "HandleAllDone"
    }
    update.message.reply_text(eval(statedict[state])(update.message.text))
    return None



def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("TOKEN")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("reset", reset_command))

    # on non command i.e message - CarryForward the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, CarryForward))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()