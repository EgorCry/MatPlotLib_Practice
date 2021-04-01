import json
import email.utils
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

with open('table.json', encoding='utf8') as f:
    table = json.loads(f.read())  # Таблица решений задач

with open('failed.json', encoding='utf8') as f:
    failed = json.loads(f.read())  # Данные по ошибкам

with open('messages.json', encoding='utf8') as f:
    messages = json.loads(f.read())  # Полученные сообщения

date_messages = messages

messages = [(m['subj'].upper(), email.utils.parsedate(m['date'])) for m in messages]


def plot_by_activity_hours():
    hours = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
    activity = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    for group, message in messages:
        activity[hours.index(int(message[3]))] = activity[hours.index(int(message[3]))] + 1

    df = pd.DataFrame({'group': hours, 'values': activity})

    # Reorder it following the values:
    ordered_df = df.sort_values(by='values')
    my_range = range(1, len(df.index) + 1)

    # Make the plot
    plt.title('Activity by hours of the day')
    plt.stem(ordered_df['values'])
    plt.xticks(my_range, ordered_df['group'])

    plt.show()


def plot_activity_by_day():
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    activity = [0, 0, 0, 0, 0, 0, 0]

    for message in date_messages:
        day = message.get('date')[:3]
        activity[days.index(day)] = activity[days.index(day)] + 1

    plt.title('Activity by days of the week')
    plt.pie(activity, labels=days)
    plt.show()


def plot_activity_by_group():
    groups = []
    activity = []
    for message in messages:
        temp = message[0].split()
        if temp[0] not in groups:
            groups.append(temp[0])
            activity.append(1)
        else:
            activity[groups.index(temp[0])] = activity[groups.index(temp[0])] + 1

    y_pos = np.arange(len(groups))

    plt.bar(y_pos, activity)

    plt.xticks(y_pos, groups)

    plt.show()


def plot_by_right_answers():
    groups = []
    scores = []

    temp = table.get('data')

    for message in temp:
        if message[3] == 1 and message[0] not in groups:
            groups.append(message[0])
            scores.append(1)
        elif message[3] == 1 and message[0] in groups:
            scores[groups.index(message[0])] = scores[groups.index(message[0])] + 1

    fig, ax = plt.subplots()

    ax.plot(groups, scores)

    ax.yaxis.set_tick_params(which='major', labelcolor='green', labelleft=False, labelright=True)

    plt.show()


def plot_by_failed_and_success():
    temp = table.get('data')

    success = []
    failed = []
    tasks = []

    for message in temp:
        if message[2] not in tasks:
            tasks.append(message[2])

    for task in tasks:
        temp_count_failed = 0
        temp_count_success = 0
        for message in temp:
            if task in message and message[3] == 1:
                temp_count_success += 1
            if task in message and message[3] == 0:
                temp_count_failed += 1
        success.append(temp_count_success)
        failed.append(temp_count_failed)

    fig, (ax1, ax2) = plt.subplots(2)
    fig.suptitle('Success and Failed plots')
    ax1.plot(tasks, success)
    ax2.plot(tasks, failed)

    plt.show()


def plot_by_failed():
    temp = table.get('data')

    tasks = []
    failed = []

    for message in temp:
        if message[2] not in tasks:
            tasks.append(message[2])
            failed.append(1)
        elif message[2] in tasks:
            failed[tasks.index(message[2])] = failed[tasks.index(message[2])] + 1

    fig, ax = plt.subplots()

    ax.bar(tasks, failed, 0.5, label='Failed')

    ax.set_ylabel('Tasks')

    plt.show()


# Examples how plots working

plot_by_activity_hours()
plot_activity_by_day()
plot_activity_by_group()
plot_by_right_answers()
plot_by_failed_and_success()
plot_by_failed()
