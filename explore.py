# Helping function to help with exploratory data analysis
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split


# helper functions for plotting

def binary_to_ints(value):
    if value:
      return 1
    else:
      return 0


def validate_train_test_split(data, target_variable, seed):
    validate_train, test = train_test_split(data, test_size = 0.2, stratify = data[target_variable])
    train, validate = train_test_split(validate_train, test_size=0.3, random_state=seed, stratify=validate_train[target_variable])
    return train, validate, test

# univariate data exploratory analysis


# Bivariate data exploratory Analysis


# Multivariate data exploratory analysis


