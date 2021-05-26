import codecs

BOT_CONFIG = {
    'intents': {
        '': {
            'examples': [''],
            'responses': ['']
        },
    },
    'failure_phrases': ['Попробуйте написать по другому.', 'Что-то непонятно', 'Возможно я не знаю.']
}


########################## аккуматизированные
def parsing_akkym():
    filename = 'сиоп_аккуматизация.csv'
    file = open(filename, "r")
    data = file.read()
    dataset = []
    file_akkym = ''
    for row in data.split(';";"\n'):
        if len(row) > 1:
            dataset.append([])
            for text in row.split(';'):
                dataset[len(dataset) - 1].append(text.replace('"', '').replace('\n', '\\n'))

    # формирую всех аккуматизированных
    file_akkym += "{'intents': {\n"
    for row in dataset:
        # print("        '",row[0],"': {\n            'examples':",row[1:3],",\n            'responses': ['",row[3],"']\n        },", sep='')
        file_akkym += "        '" + row[0] + "': {\n            'examples': ['" + row[1] + "', '" + row[
            2] + "'],\n            'responses': ['" + row[3] + ' [Фото](' + row[4] + ')' + "']\n        },\n"
    all = 'Все аккуматизированные персонажи: '
    for row in dataset:
        all += row[0] + ', '
    all += 'продолжение следует.'
    file_akkym += "         'Все аккуматизированные персонажи': {\n            'examples': ['все аккуматизированные персонажи','Список аккуматизированных','переисли аккуматизированных','список злодеев','все злодеи'],\n            'responses': ['" + all + "']\n        },\n"
    file_akkym += "    },}"
    #print(file_akkym)
    f = open('file_akkym.txt', 'w')
    f.write(file_akkym)
    #a = eval(file_akkym)


########################## квами
def parsing_kvami():
    filename = 'сиоп_квами.csv'
    file = open(filename, "r")
    data = file.read()
    rows = data.split(';";"\n')

    # вопросы отделили
    qs_all = rows[0]
    qs = qs_all.split(';')
    iqs = []
    for q in qs:
        if len(q) > 1:
            iqs.append([])
            for text in q.split('?'):
                iqs[len(iqs) - 1].append(text)

    #print(iqs)
    # отделяем имя квами и ответы на вопросы
    answers = rows[1:]
    split_answers = []
    for row in answers:
        if len(row) > 1:
            split_answers.append([])
            for text in row.split(';'):
                split_answers[len(split_answers) - 1].append(text.replace('\n', '\\n'))

    #for a in split_answers:
    #    print(a)

    # отделим квами
    kvami = []
    person = []
    answers = []
    links = []
    for answer in split_answers:
        if answer:
            kvami.append(answer[0])
            person.append(answer[1].split('/'))
            answers.append(answer[2:-1])
            links.append(answer[-1])

    # сделаем ответы на вопросы
    q_link = ['кто такой', 'как выглядит', 'какой характер у']
    file_kvami = "{'intents': {\n"
    for k, answ, l, p in zip(kvami, answers, links, person):
        for qs, an in zip(iqs, answ):
            if an:
                file_kvami += "        '" + qs[0] + " " + k + "': {\n            'examples': ["
                for a in qs[:-1]:
                    file_kvami += "'" + a + " " + k + "',"
                file_kvami += "'" + qs[
                    len(qs) - 1] + ' ' + k + "'" + "],\n            'responses': ['" + an
                if qs[0] in q_link:
                    file_kvami += ' [Фото](' + l + ')'
                file_kvami += "']\n        },\n"

    file_kvami += "    },}"
    #print(file_kvami)
    f = open('file_kvami.txt', 'w')
    f.write(file_kvami)
    #a = eval(file_kvami)


########################## персы
def parsing_persons():
    filename = 'сиоп_персонажи.csv'
    file = open(filename, "r")
    data = file.read()

    rows = data.split(';";"\n')

    # вопросы отделили
    qs_all = rows[0]
    qs = qs_all.split(';')
    iqs = []
    for q in qs:
        if len(q) > 1:
            iqs.append([])
            for text in q.split('? '):
                iqs[len(iqs) - 1].append(text.replace('?', ''))
    # print(iqs)

    # отделяем имя персонажей и ответы на вопросы
    answers = rows[1:]
    split_answers = []
    for row in answers:
        if len(row) > 1:
            split_answers.append([])
            for text in row.split(';'):
                split_answers[len(split_answers) - 1].append(text.replace('\n', '\\n'))

    # for a in split_answers:
    #    print(a)
    # print(iqs)

    # отделим персонажей
    persons = []
    links = []
    answers = []
    for answer in split_answers:
        persons.append([answer[0].split(' ')[0], answer[0]])
        links.append(answer[-1])
        answers.append(answer[1:-1])

    q_link = ['расскажи про', 'как выглядит', 'характер']
    file_persons = "    {'intents': {\n"
    for person, answ, link in zip(persons, answers, links):
        for qs, an in zip(iqs, answ):
            if an:
                file_persons += "        '" + qs[0] + " " + person[1] + "': {\n            'examples': ["
                for p in person:
                    for a in qs[:]:
                        file_persons += "'" + a + " " + p + "',"
                file_persons += "],\n            'responses': ['" + an
                if qs[0] in q_link:
                    file_persons += ' [Фото](' + link + ')'
                file_persons += "']\n        },\n"

    file_persons += "    },\n}"
    #print(file_persons)
    f = open('file_persons.txt', 'w')
    f.write(file_persons)
    a = eval(file_persons)


########################## супергерои
def parsing_superhero():
    filename = 'сиоп_супергерои.csv'
    file = open(filename, "r")
    data = file.read()
    rows = data.split(';";"\n')
    # print(rows)

    # вопросы отделили
    qs_all = rows[0]
    qs = qs_all.split(';')
    iqs = []
    for q in qs:
        if len(q) > 1:
            iqs.append([])
            for text in q.split('? '):
                iqs[len(iqs) - 1].append(text.replace('?', ''))
    # print(iqs)

    # отделяем имя персонажей и ответы на вопросы
    answers = rows[1:]
    split_answers = []
    for row in answers:
        if len(row) > 1:
            split_answers.append([])
            for text in row.split(';'):
                if text:
                    split_answers[len(split_answers) - 1].append(text.replace('\n', '\\n'))

    # for a in split_answers:
    #   print(a)
    # print(iqs)

    # отделим персонажей
    persons = []
    kvami = []
    answers = []
    links = []
    for answer in split_answers:
        if answer:
            persons.append([answer[0].split('/'), answer[1]])
            kvami.append(answer[2])
            answers.append(answer[3:-1])
            links.append(answer[-1])
    # print(answers)
    # print(persons)
    q_link = ['расскажи про', 'как выглядит', 'какой характер у']
    file_superpersons = "{'intents': {\n"
    for p, answ, l, k in zip(persons, answers, links, kvami):
        for qs, an in zip(iqs, answ):
            if an:
                file_superpersons += "        '" + qs[0] + " " + p[0][0] + "': {\n            'examples': ["
                for ps in p[0]:
                    for a in qs:
                        file_superpersons += "'" + a + " " + ps + "',"
                    if qs[0] == 'квами':
                        file_superpersons += "'" + qs[0] + " " + p[1] + "',"
                file_superpersons += "],\n            'responses': ['" + an.replace('\n', '')
                if qs[0] in q_link:
                    file_superpersons += ' [Фото](' + l + ')'
                file_superpersons += "']\n        },\n"
    file_superpersons += "    },\n}"
    # print(file_superpersons)
    f = open('file_superpersons.txt', 'w')
    f.write(file_superpersons)
    #a = eval(file_superpersons)


########################## оружие
def parsing_orusie():
    filename = 'сиоп_оружие.csv'
    file = open(filename, "r")
    data = file.read()
    rows = data.split(';";"\n')
    # for row in rows:
    #    print(row)

    # отделяем имя персонажей и ответы на вопросы
    split_answers = []
    for row in rows:
        if len(row) > 1:
            split_answers.append([])
            for text in row.split(';'):
                if text:
                    split_answers[len(split_answers) - 1].append(text.replace('\n', '\\n'))

    # for a in split_answers:
    #    print(a)

    # отделим персонажей
    persons = []
    oruzie = []
    answers = []
    links = []
    for answer in split_answers:
        if answer:
            persons.append([answer[0].split('/'), answer[1]])
            oruzie.append(answer[2])
            answers.append(answer[3:-1])
            links.append(answer[-1])
    # print(answers)
    # print(persons)
    questions = ['какое оружие у', 'что такое', 'какое оружие у']
    file_oruzie = "{'intents': {\n"
    for person, answer, link, oruzi in zip(persons, answers, links, oruzie):
        for an in answer:
            if an:
                file_oruzie += "        '" + questions[0] + " " + person[0][0] + "': {\n            'examples': ["
                file_oruzie += "'" + oruzi.split(' ')[0] + "',"
                file_oruzie += "'" + oruzi + "',"
                for pers in person[0]:
                    for question in questions[0:1]:
                        file_oruzie += "'" + question + " " + pers + "',"
                file_oruzie += "'" + questions[1] + " " + oruzi + "',"
                file_oruzie += "],\n            'responses': ['" + an.replace('\n', '')
                file_oruzie += ' [Фото](' + link + ')'
                file_oruzie += "']\n        },\n"
    all = 'Всё оружие: '
    for row in oruzie:
        all += row + ', '
    all += 'возможно есть и другое.'
    file_oruzie += "         'Список оружия': {\n            'examples': ['всё оружие','список оружия','переисли всё оружие','как много оружия','сколько всего оружия'],\n            'responses': ['" + all + "']\n        },\n"
    file_oruzie += "    },\n}"
    #print(file_oruzie)
    f = open('file_oruzie.txt', 'w')
    f.write(file_oruzie)
    #a = eval(file_oruzie)


########################## камни
def parsing_kamni():
    filename = 'сиоп_камни.csv'
    file = open(filename, "r")
    data = file.read()
    rows = data.split(';";"\n')
    # for row in rows:
    #    print(row)

    # отделяем имя персонажей и ответы на вопросы
    split_answers = []
    for row in rows:
        if len(row) > 1:
            split_answers.append([])
            for text in row.split(';'):
                if text:
                    split_answers[len(split_answers) - 1].append(text.replace('\n', '\\n'))

    # for a in split_answers:
    #    print(a)

    # отделим персонажей
    kvami = []
    kamni = []
    answers = []
    orusie = []
    links = []
    for answer in split_answers:
        if answer:
            kvami.append(answer[0])
            kamni.append(answer[1])
            orusie.append(answer[2])
            answers.append(answer[-1])
            links.append(answer[3:5])
    # for link in links:
    #    print(link)
    questions = ['какое камень у', 'какой камень у оружия', 'какое оружие у']
    file_kamni = "{'intents': {\n"
    for kvam, kamen, oruz, answer, link in zip(kvami, kamni, orusie, answers, links):
        if answer:
            file_kamni += "        '" + questions[0] + " " + kvam + "': {\n            'examples': ["
            file_kamni += "'" + kamen + "',"
            file_kamni += "'" + questions[0] + " " + kvam + "',"
            if len(oruz) < 20:
                file_kamni += "'" + questions[1] + " " + oruz + "',"
            file_kamni += "],\n            'responses': ['" + answer
            file_kamni += ' [Фото](' + link[0] + ')'
            file_kamni += "']\n        },\n"
        if len(oruz) < 20:
            file_kamni += "        '" + questions[2] + " " + kamen + "': {\n            'examples': ["
            file_kamni += "'" + questions[2] + " " + kamen + "',"
            file_kamni += "],\n            'responses': ['" + oruz
            if link[1]:
                file_kamni += ' [Фото](' + link[1] + ')'
            file_kamni += "']\n        },\n"
    all = 'Все камни чудес: '
    for row in kamni:
        all += row + ', '
    all += 'возможно есть и другие.'
    file_kamni += "         'Список камней': {\n            'examples': ['все камни чудес','список камней чудес','переисли все камни чудес','список камней','все камни'],\n            'responses': ['" + all + "']\n        },\n"
    file_kamni += "    },\n}"
    #print(file_kamni)
    f = open('file_kamni.txt', 'w')
    f.write(file_kamni)
    #a = eval(file_kamni)


########################## вопросы
def parsing_voprosi():
    filename = 'сиоп_вопросы.csv'
    file = open(filename, "r")
    data = file.read()
    rows = data.split(';";"\n')

    # отделяем имя персонажей и ответы на вопросы
    split_answers = []
    for row in rows:
        if len(row) > 1:
            split_answers.append([])
            for text in row.split(';'):
                split_answers[len(split_answers) - 1].append(text.replace('\n', '\\n'))

    # отделим персонажей
    questions = []
    answers = []
    links = []
    for answer in split_answers:
        if answer:
            questions.append(answer[0].split('?'))
            answers.append(answer[1].split('?'))
            links.append(answer[2])

    file_voprosi = "{'intents': {\n"
    for question, answer, link in zip(questions, answers, links):
        if answer:
            file_voprosi += "        '" + question[0] + "': {\n            'examples': ["
            for q in question:
                if q:
                    file_voprosi += "'" + q + "',"
            file_voprosi += "],\n            'responses': ["
            for a in answer:
                file_voprosi += "'" + a
                if link:
                    file_voprosi += ' [Фото](' + link + ')'
                file_voprosi += "',"
            file_voprosi += "]\n        },\n"
    file_voprosi += "    },\n}"
    print(file_voprosi)
    f = open('file_voprosi.txt', 'w')
    f.write(file_voprosi)
    #a = eval(file_voprosi)

parsing_persons()
parsing_superhero()
parsing_akkym()
parsing_kamni()
parsing_kvami()
parsing_orusie()
parsing_voprosi()
