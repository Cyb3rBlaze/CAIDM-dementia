import os, random, time, numpy as np, pandas as pd
import tensorflow as tf
from tensorflow import losses, optimizers, metrics
from tensorflow.keras import Input, Model, layers, callbacks, regularizers
from jarvis.train import custom, params
from jarvis.train.client import Client
from jarvis.utils.general import gpus, overload


def cosine_similarity(vects):
    """Find the cosine similarity between two vectors.

    Arguments:
        vects: List containing two tensors of same length.

    Returns:
        Tensor containing cosine similarity
        (as floating point value) between vectors.
    """
    a, b = vects
    return 1 - tf.keras.layers.Dot(axes=1, normalize=True)([a, b])


def euclidean_distance(vects):
    """Find the Euclidean distance between two vectors.

    Arguments:
        vects: List containing two tensors of same length.

    Returns:
        Tensor containing euclidean distance
        (as floating point value) between vectors.
    """
    a, b = vects
    return tf.norm(a - b, ord='euclidean')


def norm_euclidean_distance(vects):
    """Find the normalized Euclidean distance between two vectors.

    Arguments:
        vects: List containing two tensors of same length.

    Returns:
        Tensor containing normalized euclidean distance
        (as floating point value) between vectors.
    """
    a, b = vects
    return tf.norm(tf.nn.l2_normalize(a, 0) - tf.nn.l2_normalize(b, 0), ord='euclidean')


def contrastive_loss(margin=1):
    """Provides 'ctr_loss' an enclosing scope with variable 'margin'.

    Arguments:
        margin: Integer, defines the baseline for distance for which pairs
                should be classified as dissimilar (default is 1). The
                margin should correspond to the range of the distance function
                used to compare the latent vectors.

    Returns:
        'ctr_loss' function with data ('margin') attached.

    Resource:
        https://www.pyimagesearch.com/2021/01/18/contrastive-loss-for-siamese-networks-with-keras-and-tensorflow/
    """
    
    def ctr_loss(y_true, y_pred):
        """Calculates the constrastive loss.

        Arguments:
            y_true: List of labels, each label is of type float32.
            y_pred: List of predictions of same length as of y_true,
                    each label is of type float32.

        Returns:
            A tensor containing constrastive loss as floating point value.
        """
        square_pred = tf.math.square(y_pred)
        margin_square = tf.math.square(tf.math.maximum((margin - y_pred), 0))
        return tf.math.reduce_mean(
            y_true * square_pred + (1 - y_true) * margin_square
        )

    return ctr_loss