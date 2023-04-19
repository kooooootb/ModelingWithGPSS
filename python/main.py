from config import *
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import linear_model


def extend_features(x, k):
    X = x
    for i in range(2, k + 1):
        X = np.hstack([X, x ** i])
    return X


def plot_curve(X, Y, label, k):
    color = next(ax._get_lines.prop_cycler)['color']

    regr = linear_model.LinearRegression()
    X = X.reshape(-1, 1)
    regr.fit(extend_features(X, k), Y)

    X_curve = np.linspace(np.min(X), np.max(X), 1000).reshape(-1, 1)
    Y_curve = regr.predict(extend_features(X_curve, k))
    plt.plot(X_curve, Y_curve, label=label, color=color)

    # plot errors
    params_unique = np.unique(X)
    for param in params_unique:
        indices = np.where(X == param)[0]
        values = Y[indices]
        mean = np.mean(values)
        err = np.std(values) / np.sqrt(len(values))
        gran = 100
        err = np.linspace(mean - err, mean + err, gran)
        param_axis = np.repeat(param, gran)
        plt.plot(param_axis, err, color=color)


def plot_with_parameter(data, parameter, par_label, xlim=None, ylim=None, graph_title=None):
    gp = pd.concat([pd.DataFrame({par_label: parameter}), data], axis=1).groupby(par_label)
    mean = gp.mean()
    errors = gp.std().apply(lambda a: a * 2.8 / np.sqrt(10))

    mean.plot(yerr=errors, style="o-", title=graph_title, ylim=ylim, xlim=xlim)


if __name__ == '__main__':
    # queue_data = pd.DataFrame({
    #     'Очередь на блок предварительной подготовки': preproc_queue,
    #     'Очередь на блок сборки': assembly_queue,
    #     'Очередь на блок регулировки': adjust_queue,
    # })
    #
    # utility_data = pd.DataFrame({
    #     'Загрузка блока предварительной подготовки': preproc_utility,
    #     'Загрузка блока сборки': assembly_utility,
    #     'Загрузка блока регулировки': adjust_utility,
    # })

    block = 'блоке регулировки'
    preproc_utility = np.array([x * 100 for x in preproc_utility])
    assembly_utility = np.array([x * 100 for x in assembly_utility])
    adjust_utility = np.array([x * 100 for x in adjust_utility])
    ax = plt.gca()

    plot_curve(parameters, preproc_queue, 'Очередь на блок предварительной подготовки', k=3)
    plot_curve(parameters, assembly_queue, 'Очередь на блок сборки', k=5)
    plot_curve(parameters, adjust_queue, 'Очередь на блок регулировки', k=10)

    plt.title(f'Зависимость средней длины очереди\nот времени обработки в {block}')
    plt.xlabel('Длительность обработки, сек.')
    plt.ylabel('Средняя очередь на блок, ед.')
    plt.legend()
    plt.grid(True)
    plt.ylim((0, 100))
    plt.show()

    plot_curve(parameters, preproc_utility, 'Загрузка блока предварительной подготовки', k=3)
    plot_curve(parameters, assembly_utility, 'Загрузка блока сборки', k=5)
    plot_curve(parameters, adjust_utility, 'Загрузка блока регулировки', k=5)

    plt.title(f'Зависимость средней загрузки\nот времени обработки в {block}')
    plt.xlabel('Длительность обработки, сек.')
    plt.ylabel('Средняя загрузка блока, %')
    plt.legend()
    plt.grid(True)
    plt.ylim((0, 100))
    plt.show()

    # title = f'Длительность обработки в {block}'
    # plot_with_parameter(queue_data, parameters, title, xlim=None, ylim=(0, 100), graph_title=f'Зависимость средней длины очереди\n от длительности обработки в {block}')
    # plot_with_parameter(utility_data, parameters, title, xlim=None, ylim=(0, 1), graph_title=f'Зависимость средней загрузки\n от длительности обработки в {block}')
