"""
    Handler that manages reminders removal
"""
import logging

from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters

from bot.constants import READ_DELETE
from bot.handlers.misc import cancel
from bot.jobs.db_ops import remove_reminder

logger = logging.getLogger(__name__)


def rm_reminder(update, context):
    logger.info("STARTED new reminder removal")
    if not context.args:
        update.effective_message.reply_text("🗑 What reminder do you want to delete?", quote=False)
        logger.info("Waiting user input on what reminder to remove..")
        return READ_DELETE

    reminder_key = ' '.join(context.args)
    return _delete_reminder(update, reminder_key)


def rm_reminder_from_text(update, context):
    reminder_key = update.message.text
    return _delete_reminder(update, reminder_key)


def _delete_reminder(update, reminder_key):
    msg = remove_reminder(
        text=reminder_key,
        user_id=str(update.message.from_user.id),
    )
    update.message.reply_text(msg, parse_mode='markdown')

    logger.info("ENDED reminder removal successfully")
    return ConversationHandler.END


remove_reminders = ConversationHandler(
    entry_points=[
        CommandHandler(['delete', 'borrar'], rm_reminder),
    ],
    states={
        READ_DELETE: [MessageHandler(Filters.text, rm_reminder_from_text)]
    },
    fallbacks=[CommandHandler('cancel', cancel)],
    name='Delete reminders',
    persistent=True
)