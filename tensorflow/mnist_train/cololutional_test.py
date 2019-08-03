# -*- coding:utf-8 -*-


import time
import tensorflow as tf
import numpy as np
from tensorflow.contrib.learn.python.learn.datasets.mnist import read_data_sets

from common import INPUT_NODE, OUTPUT_NODE, Regression, IMAGE_SIZE, NUM_CHANNELS, Convolution
from convolutional_train import MODEL_SAVE_PATH, BATCH_SIZE, MOVING_AVERAGE_DECAY

EVAL_INTERVAL_SECS = 10


def evaluate_regression(mnist):
    with tf.Graph().as_default() as g:
        x = tf.compat.v1.placeholder(
            tf.float32, shape=[BATCH_SIZE, IMAGE_SIZE, IMAGE_SIZE, NUM_CHANNELS], name='x-input')
        y_ = tf.compat.v1.placeholder(tf.float32, [None, OUTPUT_NODE], name='y_input')
        validate_feed = {x: np.reshape(mnist.validation.images, [BATCH_SIZE, IMAGE_SIZE, IMAGE_SIZE, NUM_CHANNELS]), y_: mnist.validation.labels}

        # 直接通过调用封装好的函数来计算前向传播的结果，因为测试时不关注正则化损失的值，所以这里用于计算正则化损失的函数被设置为None
        y = Convolution.inference(x, True, None)

        # 使用前向传播的结果计算正确率，如果需要对未知的样例进行分类，那么使用tf.argmax(y, 1)就可以得到输入样例的预测类别
        correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

        # 通过变量重命名的方式来加载模型，这样在前向传播的过程中就不需要调用求滑动平均的函数来获取平均值了
        variable_averages = tf.train.ExponentialMovingAverage(MOVING_AVERAGE_DECAY)
        variables_to_restore = variable_averages.variables_to_restore()
        saver = tf.compat.v1.train.Saver(variables_to_restore)

        # 每隔EVAL_INTERVAL_SECS秒来调用一次计算正确率的过程以检测训练过程中正确率的变化
        with tf.compat.v1.Session() as sess:
            ckpt = tf.train.get_checkpoint_state(MODEL_SAVE_PATH)
            if ckpt and ckpt.model_checkpoint_path:
                saver.restore(sess, ckpt.model_checkpoint_path)
                accuracy_score = sess.run(accuracy, feed_dict=validate_feed)
                print("validation accuracy={}".format( accuracy_score))
            else:
                print("no checkpoint file found")
                return


def main(argv=None):
    mnist = read_data_sets('./data/', one_hot=True)
    evaluate_regression(mnist)


if __name__ == '__main__':
    tf.compat.v1.app.run()
