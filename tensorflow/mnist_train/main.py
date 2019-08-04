import numpy as np
import tensorflow as tf
from flask import Flask, jsonify, render_template, request
import json

from tensorflow.contrib.learn.python.learn.datasets.mnist import read_data_sets

from common import Regression, Convolution, IMAGE_SIZE, NUM_CHANNELS
from convolutional_train import BATCH_SIZE
from regression_train import MOVING_AVERAGE_DECAY, REGULARZATION_RATE

x = tf.compat.v1.placeholder('float', [None, 784])
mnist = read_data_sets('./data/', one_hot=True)
sess = tf.Session()
variable_averages = tf.train.ExponentialMovingAverage(MOVING_AVERAGE_DECAY)
regularizer = tf.contrib.layers.l2_regularizer(REGULARZATION_RATE)


y1, _ = Regression.inference(x, regularizer)
sess.run(tf.global_variables_initializer())
saver1 = tf.train.Saver(_)
saver1.restore(sess, "model/regression/regression.ckpt")

y2, _ = Convolution.inference(x, True, regularizer)
sess.run(tf.global_variables_initializer())
saver2 = tf.train.Saver(_)
saver2.restore(sess, "model/convolutional/convolutional.ckpt")


def regression(input):
    return sess.run(y1, feed_dict={x: input}).flatten().tolist()


def convolutional(input):
    return sess.run(y2, feed_dict={x: input}).flatten().tolist()


app = Flask(__name__)


@app.route('/api/mnist', methods=['post'])
def mnist():
    input = ((255 - np.array(request.json, dtype=np.uint8)) / 255.0).reshape(1, 784)
    output1 = regression(input)
    output2 = convolutional(input)

    output = {}
    output["output1"] = output1
    output["output2"] = output2
    res = []
    res.append(output)
    a = {}
    a['site'] = res
    mydata = json.dumps(a, ensure_ascii=False).encode("utf8")
    return mydata


@app.route('/')
def main():
    return render_template('index.html')


if __name__ == "__main__":
    app.debug = True
    app.run(host='127.0.0.1', port=8000)
