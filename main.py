import random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

BOT_CONFIG = {
    'intents': {
    },
    'random_phrases': [],
    'failure_phrases': [
        'Попробуйте написать по другому.', 'Что-то непонятно',
        'Возможно я не знаю.',
    ]
}


def load_config(configs):
    for intent in configs['intents'].items():
        BOT_CONFIG['intents'][intent[0]] = {'examples': intent[1]['examples'], 'responses': intent[1]['responses']}


def load_random(configs):
    for intent in configs['intents'].items():
        BOT_CONFIG['random_phrases'].append(intent[1]['responses'])


percent = 0.1

config_akkym = eval(open('file_akkym.txt', "r").read())
config_kvami = eval(open('file_kvami.txt', "r").read())
config_persons = eval(open('file_persons.txt', "r").read())
config_superpersons = eval(open('file_superpersons.txt', "r").read())
config_kamni = eval(open('file_kamni.txt', "r").read())
config_oruzie = eval(open('file_oruzie.txt', "r").read())
config_voprosi = eval(open('file_voprosi.txt', "r").read())

load_config(config_kvami)
load_config(config_akkym)
load_config(config_persons)
load_config(config_superpersons)
load_config(config_kamni)
load_config(config_oruzie)
load_config(config_voprosi)

load_random(config_kvami)
load_random(config_kamni)
load_config(config_akkym)
load_random(config_oruzie)
load_random(config_persons)
load_random(config_superpersons)
load_config(config_voprosi)


def filter_text(text):
    text = text.lower()
    text = [c for c in text if c in 'абвгдеёжзийклмнопрстуфхцчшщьъыэюя- 1234567890']
    text = ''.join(text)
    return text


# списки с данными и классами
X = []
y = []

# разбиваем наш словарь на фразы и классы
for intent, intent_data in BOT_CONFIG['intents'].items():
    for example in intent_data['examples']:
        X.append(filter_text(example))
        y.append(intent)

# Делаем магическую векторизацию для того что бы разделить слова
vectorizer = CountVectorizer(ngram_range=(2, 3), analyzer="char_wb")
X = vectorizer.fit_transform(X)
print(vectorizer.get_feature_names())
clf = LogisticRegression(max_iter=1000).fit(X, y)  # модель для распознования откуда вопрос


def get_failure_phrase():
    phrases = BOT_CONFIG['failure_phrases']
    return random.choice(phrases)


def generate_answer_by_text(question):
    intent = clf.predict(vectorizer.transform([question]))
    predict_proba = max(clf.predict_proba(vectorizer.transform([question]))[0])
    print(' ', intent, predict_proba)
    phrases = BOT_CONFIG['intents'][intent[0]]['responses']
    if intent == 'расскажи что нибудь':
        phrases = BOT_CONFIG['random_phrases']
        phrase = random.choice(phrases)
        return phrase[0]
    if predict_proba > percent:
        return random.choice(phrases)
    else:
        words = filter_text(question).split(' ')
        if words:
            answ = []
            for intent_ in BOT_CONFIG['intents']:
                for word in words:
                    if word:
                        for respons in BOT_CONFIG['intents'][intent_]['responses']:
                            text = filter_text(respons)
                            if word + ' ' in text:
                                answ.append(
                                    [intent_, BOT_CONFIG['intents'][intent_]['examples'][0],
                                     text.count(word) / len(text.split(' '))])
            answ.sort(key=lambda x: x[2])
            if predict_proba > 0.03:
                if intent != 'Привет' and intent != 'Пока':
                    return 'К сожалению я не нахожу или не знаю ответа на данный вопрос, но возможно вы имели ' \
                           'ввиду "' + BOT_CONFIG['intents'][intent[0]]['examples'][0] + '"? Задайте этот вопрос.'
            else:
                if answ:
                    return 'К сожалению я не нахожу прямого ответа на данный вопрос, но возможно ответ есть тут: "' \
                           + answ[len(answ) - 1][1] + '"? Задайте этот вопрос.'


def filter_answer(answer):
    answer = answer.replace('""', '"')
    answer = answer.replace('??', '')
    if answer[0] == '"':
        answer = answer[1:]
    answer = answer.replace('." ', '. ')
    return answer

def bot(question):
    # Генеруем подходящий по контексту ответ
    question = filter_text(question)
    answer = generate_answer_by_text(question)
    if answer:
        answer = filter_answer(answer)
        return answer
    # Используем заглушку
    answer = get_failure_phrase()
    return answer


print(clf.score(X, y))
"""
question = None
while question not in ['exit', 'выход']:
    question = input()
    answer = bot(question)
    print(answer)
"""

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update: Update, _: CallbackContext) -> None:
    """Echo the user message."""
    user = update.effective_user
    print(user.mention_markdown_v2())
    print('-', update.message.text)
    answer = bot(update.message.text)
    print(' ', answer, '\n')
    update.message.reply_text(answer, parse_mode='markdown')


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("1825689465:AAGgkYSgZm2cK5AnonL97-GCG4kgvAyZ-6A")

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
