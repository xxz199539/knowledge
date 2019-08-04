# -*- coding:utf-8 -*-
import os
import tensorflow as tf
from tensorflow.contrib.learn.python.learn.datasets.mnist import read_data_sets



# 配置神经网络参数
import common

BATCH_SIZE = 100
LEARNING_RATE_BASE = 0.8  # 基础的学习率
LEARNING_RATE_DECAY = 0.99  # 学习率的衰减率
REGULARZATION_RATE = 0.0001  # 描述模型复杂度的正则化项在损失函数中的系数
TRAINING_STEPS = 30000
MOVING_AVERAGE_DECAY = 0.99  # 滑动平均衰减率


# 模型保存的路径和文件名
MODEL_SAVE_PATH = './model/regression/'
MODEL_NAME = 'regression.ckpt'


def train(mnist):
    # 定义输入输出placeholder
    x = tf.compat.v1.placeholder(tf.float32, shape=[None, common.INPUT_NODE], name='x-input')
    y_ = tf.compat.v1.placeholder(tf.float32, shape=[None, common.OUTPUT_NODE], name='y-input')

    regularizer = tf.contrib.layers.l2_regularizer(REGULARZATION_RATE)
    # 直接使用mnist_inference中定义的前向传播过程
    y,_ = common.Regression.inference(x, regularizer)
    global_step = tf.Variable(0, trainable=False)

    # 定义损失函数，学习率，滑动平均操作以及训练过程
    variable_averages = tf.train.ExponentialMovingAverage(MOVING_AVERAGE_DECAY, global_step)
    variable_averages_op = variable_averages.apply(tf.compat.v1.trainable_variables())
    cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=y, labels=tf.argmax(y_, 1))
    cross_entropy_mean = tf.reduce_mean(cross_entropy)
    loss = cross_entropy_mean + tf.add_n(tf.compat.v1.get_collection('losses'))
    learning_rate = tf.compat.v1.train.exponential_decay(LEARNING_RATE_BASE, global_step, mnist.train.num_examples / BATCH_SIZE,
                                               LEARNING_RATE_DECAY)
    train_step = tf.compat.v1.train.GradientDescentOptimizer(learning_rate).minimize(loss, global_step=global_step)
    train_op = tf.group([train_step, variable_averages_op])

    # 使用前向传播的结果计算正确率，如果需要对未知的样例进行分类，那么使用tf.argmax(y, 1)就可以得到输入样例的预测类别
    correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    # 初始化Tensorflow持久化类
    saver = tf.compat.v1.train.Saver()
    with tf.compat.v1.Session() as sess:
        tf.compat.v1.global_variables_initializer().run()
        for i in range(TRAINING_STEPS):
            xs, ys = mnist.train.next_batch(BATCH_SIZE)
            _, loss_value, step, accuracy_score = sess.run([train_op, loss, global_step, accuracy], feed_dict={x: xs, y_: ys})

            if i % 1000 == 0:
                # 输出当前的训练情况，这里只输出了模型在当前训练batch上的损失函数大小，通过损失函数的大小可以大概了解训练的
                #  情况，在验证数据集上的正确率信息会有一个单独的程序来生成
                print("After {} training step, loss on training batch is {},accury is {}".format(i, loss_value, accuracy_score))
                # 保存当前的模型，注意这里给出了global_step参数，这样可以让每个被保存模型的文件名尾加上训练的轮数
        saver.save(sess, os.path.join(MODEL_SAVE_PATH, MODEL_NAME))
    return y, saver

def main(argv=None):
    mnist = read_data_sets('./data/', one_hot=True)
    train(mnist)


if __name__ == '__main__':
    tf.compat.v1.app.run()
