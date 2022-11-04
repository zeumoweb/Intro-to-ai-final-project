# Helping function to help with exploratory data analysis
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from scipy import stats


# helper functions for plotting

def binary_to_ints(value):
    if value:
      return 1
    else:
      return 0



def train_validate_test_split(data, target, seed = 126):
    """
    It splits the data into train, validate and test sets.

    :param data: the dataframe you want to split
    :param target: The column name of the target variable
    :param seed: The random seed to use when splitting the data, defaults to 126 (optional)
    :return: three dataframes: train, validate, and test.
    """
    train_validate, test = train_test_split(data, test_size=0.20, random_state=seed, stratify=data[target])
    train, validate = train_test_split(train_validate, test_size=0.30, random_state=seed,stratify=train_validate[target])
    return train, validate, test

def process_unencoded_data(data):
    """
    It takes in a dataframe, drops duplicates, removes rows where tenure is 0, removes $ and , from
    TotalCharges, converts TotalCharges to float, strips whitespace from all object columns, and returns
    a train, validate, and test dataframe

    :param data: the dataframe to be split
    :return: A tuple of 4 dataframes
    """
    data.drop_duplicates(inplace = True)
    categorical_columns = data.select_dtypes('object').columns


    for column in categorical_columns:
        data[column] = data[column].str.strip()
    # data.drop(columns = ['InternetService', 'Contract', 'PaymentMethod'], inplace = True)
    return train_validate_test_split(data, 'Revenue')




# univariate data exploratory analysis

def univariate(data, categorical_vars, quantitative_vars):
    for var in categorical_vars:
        univariate_categorical(data, var)

    for column in quantitative_vars:
        plot, descriptive_statistics = univariate_quant(data, column)
        plt.gca(figsize = 10)
        plt.show(plot)
        print(descriptive_statistics)


def univariate_categorical(data, categorical_vars):
    frequency_table = freq_table(data, categorical_vars)
    plt.figure(figsize=(6,3))
    sns.barplot(x=categorical_vars, y='Count', data=frequency_table, color='lightblue')
    plt.xticks(rotation = 90)
    plt.title(categorical_vars)
    plt.show()
    print(frequency_table)


def univariate_quant(data, quantitative_vars):
    descriptive_statistics = data[quantitative_vars].describe()
    plt.figure(figsize=(8,2))
    p = plt.subplot(1, 2, 1)
    p = plt.hist(data[quantitative_vars], color='lightblue')
    p = plt.title(quantitative_vars)

    # second plot: box plot
    p = plt.subplot(1, 2, 2)
    p = plt.boxplot(data[quantitative_vars])
    p = plt.title(quantitative_vars)
    return p, descriptive_statistics


def freq_table(train, cat_var):
    class_labels = list(train[cat_var].unique())
    freq_table = (
      pd.DataFrame(
        {cat_var: class_labels,
        'Count': train[cat_var].value_counts(normalize=False),
        'Percent': round(train[cat_var].value_counts(normalize=True)*100,2)
        }))

    return freq_table



# Bivariate data exploratory Analysis
def bivariate_categorical(data, target, categorical_vars):
    ct = pd.crosstab(data[categorical_vars], data[target], margins=True)
    chi2_summary, observed, expected = run_chi2(data, categorical_vars, target)
    p = plot_cat_by_target(data, target, categorical_vars)

    print(chi2_summary)
    print("\nobserved:\n", ct)
    print("\nexpected:\n", expected)
    plt.show(p)
    print("\n_____________________\n")

def bivariate_quant(data, target, quantitative_vars):
    print(quantitative_vars, "\n____________________\n")
    descriptive_stats = data.groupby(target)[quantitative_vars].describe()
    average = data[quantitative_vars].mean()
    mann_whitney = compare_means(data, target, quantitative_vars)
    plt.figure(figsize=(4,4))
    boxen = plot_boxen(data, target, quantitative_vars)
    swarm = plot_swarm(data, target, quantitative_vars)
    plt.show()
    print(descriptive_stats, "\n")
    print("\nMann-Whitney Test:\n", mann_whitney)
    print("\n____________________\n")


def run_chi2(data, categorical_var, target_variable):
    observed = pd.crosstab(data[categorical_var], data[target_variable])
    chi2, p, degf, expected = stats.chi2_contingency(observed)
    chi2_summary = pd.DataFrame({'chi2': [chi2], 'p-value': [p],
                                 'degrees of freedom': [degf]})
    expected = pd.DataFrame(expected)
    return chi2_summary, observed, expected

def plot_cat_by_target(data, target_variable, categorical_var):
    p = plt.figure(figsize=(2,2))
    p = sns.barplot(categorical_var, target_variable, data=data, alpha=.8, color='lightseagreen')
    overall_rate = data[target_variable].mean()
    p = plt.axhline(overall_rate, ls='--', color='gray')
    return p



def plot_swarm(data, target_variable, quantitative_var):
    average = data[quantitative_var].mean()
    p = sns.swarmplot(data=data, x=target_variable, y=quantitative_var, color='lightgray')
    p = plt.title(quantitative_var)
    p = plt.axhline(average, ls='--', color='black')
    return p

def plot_boxen(data, target_variable, quantitative_var):
    average = data[quantitative_var].mean()
    p = sns.boxenplot(data=data, x=target_variable, y=quantitative_var, color='seablue')
    p = plt.title(quantitative_var)
    p = plt.axhline(average, ls='--', color='black')
    return p

# alt_hyp = ‘two-sided’, ‘less’, ‘greater’

def compare_means(data, target_variable, quantitative_vars, alt_hyp='two-sided'):
    x = data[data[target_variable]==0][quantitative_vars]
    y = data[data[target_variable]==1][quantitative_vars]
    return stats.mannwhitneyu(x, y, use_continuity=True, alternative=alt_hyp)

# Multivariate data exploratory analysis