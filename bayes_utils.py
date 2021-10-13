# A set of tools

import numpy as np
import math
import csv
import string
import scipy.stats as stats
from collections import Counter

# import multiprocessing
# pool = multiprocessing.Pool()

# Some code was reused to avoid boilerplate.
# Credit to:
# http://machinelearningmastery.com/naive-bayes-classifier-scratch-python/


def loadCsv(filename):
    # Loads a CSV
    lines = csv.reader(open(filename, "rb"))
    dataset = list(lines)
    for i in range(len(dataset)):
        dataset[i] = [x for x in dataset[i]]
    return dataset


def uniform_data(dataset):
    # Some labels have . and extra spaces. Unoform data will strip spaces and
    # remove .
    return [[str(t).strip().replace(".", "") for t in i] for i in dataset]


def mean(numbers):
    # Computes the mean of list of numbers
    return sum(numbers)/float(len(numbers))


def stdev(numbers):
    # Computes the standar deviation of a list of numbers
    avg = mean(numbers)
    variance = sum([pow(x-avg, 2) for x in numbers])/float(len(numbers)-1)
    return math.sqrt(variance)


def separateByClass(dataset):
    # Dataset is a list of vectors, with label being the last index
    # [feature1, feature2, feature3, label]
    # Separates a dataset into a dict with each label
    # { label1: [feature1, feature2, feature3] }
    separated = {}
    for i in range(len(dataset)):
        vector = dataset[i]
        if (vector[-1] not in separated):
            separated[vector[-1]] = []
        separated[vector[-1]].append(vector)
    return separated


def summarize(dataset):
    # Dataset is a list of lists. Zip will aggregate all the same features
    # eg. [a,b,c] [g,t,e] -> [(a,g), (b,t), (c,e)]
    # Returns (mean_of_dataset, stdev_of_dataset) for each feature
    summaries = [
        (mean(attribute), stdev(attribute))
        for attribute in zip(*dataset)]
    # The las summary is the summary of the labels.
    del summaries[-1]
    return summaries


def discretize_variable(dataset, index):
    # Inneficiently puts a constant variable into one of the 4 percentiles
    print(f"Discretizing... variable {index}")
    # variable_values = [sample[index] for sample in dataset]
    new_values = stats.rankdata(
        dataset[:, index], "average")/dataset.shape[0]
    dataset[:, index] = (np.round(new_values*100)/25).astype(int)

    return dataset


def discrete_summarize(dataset):
    # Dataset is a list of lists. Zip will aggregate all the same features
    # eg. [a,b,c] [g,t,e] -> [(a,g), (b,t), (c,e)]
    # Counts occurency of each discrete occurrence of feature. eg {'<10': 10}
    # Returns (summaries, )
    summaries = [
        dict(Counter(attribute))
        for attribute in zip(*dataset)]
    # The las summary is the summary of the labels.
    del summaries[-1]
    return (summaries, len(dataset))


def summarizeByClass(dataset):
    # Creates a summary for each class value
    # eg {positive: ((mean, stdv)(mean, stdv)}
    separated = separateByClass(dataset)
    summaries = {}
    for classValue, instances in separated.items():
        summaries[classValue] = summarize(instances)
    return summaries


def discrete_summarize_by_class(dataset):
    # Creates a summary for each class value
    # eg {positive: ((mean, stdv)(mean, stdv)}
    separated = separateByClass(dataset)
    summaries = {}
    for classValue, instances in separated.items():
        summaries[classValue] = discrete_summarize(instances)
    return summaries


def discrete_summarize_total(dataset):
    # summrize the total data
    summaries = discrete_summarize(dataset)
    return summaries


def calculateProbability(x, mean, stdev):
    exponent = math.exp(-(math.pow(x-mean, 2)/(2*math.pow(stdev, 2))))
    return (1 / (math.sqrt(2*math.pi) * stdev)) * exponent


def calculateDiscreteProbability(x, mean, stdev):
    exponent = math.exp(-(math.pow(x-mean, 2)/(2*math.pow(stdev, 2))))
    return (1 / (math.sqrt(2*math.pi) * stdev)) * exponent


def calculateClassProbabilities(summaries, inputVector):
    probabilities = {}
    for classValue, classSummaries in summaries.items():
        probabilities[classValue] = 1
        for i in range(len(classSummaries)):
            mean, stdev = classSummaries[i]
            x = inputVector[i]
            probabilities[classValue] *= calculateProbability(
                x, mean, stdev)
    return probabilities
