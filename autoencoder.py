from __future__ import print_function

import math
import numpy as np
import numpy.linalg as nla
import pandas as pd
import re
import six
from os.path import join
from matplotlib import pyplot as plt

import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

pd.options.display.float_format = '{:.2F}'.format
#pd.options.display.max_rows = 10

data = pd.read_csv("mergedtable.csv", sep='|')

data.drop(columns=['id'], inplace=True)
#print(data.head())

class SimilarityEncoder(object):
    def __init__(self, dataframe, input_feature, output_feature, dense_feature, sparse_feature,
                 hidden_dims=[32],regularization=0.0, use_bias=True, batch_size=8, inspect=False):
        used_feature_space = tuple(set(input_feature).union(output_feature))
        sparse_feature_space = tuple(set(used_feature_space).difference(dense_feature))
        spare_feature_vocab = {i: sorted(list(set(data[i].values))) for i in sparse_feature_space}

