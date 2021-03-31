import matplotlib.pyplot as plt
import numpy as np


def plot_game_per_year():

    f = open('GAMES.csv', 'r', encoding='utf-8')

    data = f.readlines()

    year_list = []
    game_per_year_list = []

    years = []

    for row in data:
        row = row.replace('"', '').rstrip().split(';')
        if row[3] != 'не издана':
            years.append(int(row[3]))
            if int(row[3]) not in year_list:
                year_list.append(int(row[3]))

    sorted(year_list)

    for year in year_list:
        game_per_year_list.append(years.count(int(year)))

    fig, ax = plt.subplots()
    ax.bar(year_list, game_per_year_list)
    plt.show()

    f.close()


def plot_genre_per_year():

    f = open('GAMES.csv', 'r', encoding='utf-8')

    data = f.readlines()

    years = []
    genres = []
    for row in data:
        row = row.replace('"', '').rstrip().split(';')
        if row[1] not in genres:
            genres.append(row[1])
        row[3] = int(row[3]) if row[3] != 'не издана' else row[3]
        if row[3] not in years and type(row[3]) == int:
            years.append(row[3])

    genres_per_year = []

    for i in range(len(years)):
        temp_genres = []
        for genre in genres:
            temp_genre_count = 0
            for row in data:
                row = row.replace('"', '').rstrip().split(';')
                if row[1] == genre:
                    temp_genre_count += 1
            temp_genres.append(temp_genre_count)
        genres_per_year.append(temp_genres)

    width = 2

    Pos = np.array(range(len(genres_per_year[0])))

    for i in range(len(genres_per_year)):
        plt.bar(Pos + i*width, genres_per_year[i], width=width)

    plt.show()

    f.close()


# Example
plot_game_per_year()
# plot_genre_per_year()
