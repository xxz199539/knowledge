# -*- coding:utf-8 -*-


import tensorflow as tf

# 定义神经网络结构相关的参数
INPUT_NODE = 784
OUTPUT_NODE = 10
LAYER1_NODE = 500
IMAGE_SIZE = 28
NUM_CHANNELS = 1
NUM_LABELS = 10


# 线性回归
class Regression:
    # 听过tf.get_variable函数来获取变量。在训练神经网络时会创建这些变量；在测试时会通过保存的模型加载这些变量的取值。而且更加方便的是，因为
    # 可以在变量加载时将滑动平均变量重命名，所以可以直接通过同样的名字在训练时使用变量自身，而在测试时使用变量的滑动平均变量均值。这个函数也会将
    # 变量的正则化损失加入损失集合
    @staticmethod
    def get_weight_variable(shape, regularizer):
        weights = tf.get_variable('weight', shape, initializer=tf.truncated_normal_initializer(stddev=0.1))

        # 当给出了正则化损失函数时，将当前变量的正则化损失加入名字为loss的集合，在这里使用了add_to_collection函数将一个张量加入一个集合，
        # 这个集合名称为losses。这是自定义集合，不在tensorflow自动管理的集合列表中
        if regularizer:
            tf.compat.v1.add_to_collection('losses', regularizer(weights))
        return weights

    # 定义神经网络的前向传播过程
    @staticmethod
    def inference(input_tensor, regularizer):
        # 声明第一层神经网络的变量并完成前向传播过程
        with tf.compat.v1.variable_scope('layer1'):
            # 这里通过tf.get_variable或tf.Variable没有本质区别，因为在训练或是测试中没有在同一个程序中多次调用这个函数。如果在同一程序中
            # 多次调用，第一次调用之后需要将resuse参数设置为True。
            weights = Regression.get_weight_variable([INPUT_NODE, LAYER1_NODE], regularizer)
            tf.compat.v1.add_to_collection("regression_inference", weights)
            biases = tf.compat.v1.get_variable('biases', [LAYER1_NODE], initializer=tf.constant_initializer(0.0))
            layer1 = tf.nn.relu(tf.matmul(input_tensor, weights) + biases)
            tf.compat.v1.add_to_collection("regression_inference", biases)
        # 类似的声明第二层神经网络的变量并完成前向传播过程
        with tf.compat.v1.variable_scope('layer2'):
            weights = Regression.get_weight_variable([LAYER1_NODE, OUTPUT_NODE], regularizer)
            tf.compat.v1.add_to_collection("regression_inference", weights)
            biases = tf.compat.v1.get_variable('biases', [OUTPUT_NODE], initializer=tf.constant_initializer(0.0))
            layer2 = tf.matmul(layer1, weights) + biases
            tf.compat.v1.add_to_collection("regression_inference", biases)
        return layer2, tf.compat.v1.get_collection("regression_inference")


# 卷积神经网络
class Convolution:
    # 第一层卷积层的尺寸和深度
    CONV1_DEEP = 32
    CONV1_SIZE = 5

    # 第二层卷积层的尺寸和深度
    CONV2_DEEP = 64
    CONV2_SIZE = 5

    # 全连接层的节点个数
    FC_SIZE = 512

    # 定义卷积神经网络的前向传播过程，这里添加了一个新的参数train，用于区分训练过程和测试过程。在这个程序将使用dropout方法，进一步提升可
    # 靠性并防止过拟合，只在训练时使用
    @staticmethod
    def inference(input_tensor, train, regularizer):
        # 声明第一层卷积层的变量并实现前向传播过程
        with tf.compat.v1.variable_scope("layer1-conv1"):
            conv1_weights = tf.compat.v1.get_variable(
                "weight", [Convolution.CONV1_SIZE, Convolution.CONV1_SIZE, NUM_CHANNELS, Convolution.CONV1_DEEP],
                initializer=tf.truncated_normal_initializer(stddev=0.1))
            tf.compat.v1.add_to_collection("convolution_inference", conv1_weights)
            conv1_biases = tf.compat.v1.get_variable(
                "bias", [Convolution.CONV1_DEEP], initializer=tf.compat.v1.constant_initializer(0.0)
            )
            tf.compat.v1.add_to_collection("convolution_inference", conv1_biases)
            # 使用边长为5，深度为32的过滤器，过滤移动的步长为1，且使用全0填充
            conv1 = tf.compat.v1.nn.conv2d(
                tf.reshape(input_tensor, [1, 28, 28, 1]), conv1_weights, strides=[1, 1, 1, 1], padding="SAME"
            )
            relu1 = tf.compat.v1.nn.relu(tf.compat.v1.nn.bias_add(conv1, conv1_biases))

        # 实现第二层池化层的前向传播过程。这里选用最大池化层，过滤器的边长为2，使用全0填充且移动步长为2，这一层的输入是上一层的输出，也就是
        # 29*28*32的矩阵，输出为14*14*32的矩阵
        with tf.compat.v1.name_scope("layer2-poll1"):
            pool1 = tf.compat.v1.nn.max_pool(
                relu1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding="SAME"
            )

        # 声明第三层卷积层的变量并实现前向传播过程，这一层的输入为上一层的输出层，输出为14*14*64
        with tf.compat.v1.variable_scope("layer3-conv2"):
            conv2_weights = tf.compat.v1.get_variable(
                "weight",
                [Convolution.CONV2_SIZE, Convolution.CONV2_SIZE, Convolution.CONV1_DEEP, Convolution.CONV2_DEEP],
                initializer=tf.compat.v1.truncated_normal_initializer(stddev=0.1)
            )
            tf.compat.v1.add_to_collection("convolution_inference", conv2_weights)
            conv2_biases = tf.compat.v1.get_variable(
                "bias", [Convolution.CONV2_DEEP], initializer=tf.compat.v1.constant_initializer(0.0)
            )
            tf.compat.v1.add_to_collection("convolution_inference", conv2_biases)

            # 使用边长为5，深度为64的过滤器，过滤器步长为1，且使用全0填充
            conv2 = tf.compat.v1.nn.conv2d(
                pool1, conv2_weights, strides=[1, 1, 1, 1], padding="SAME"
            )
            relu2 = tf.compat.v1.nn.relu(tf.compat.v1.nn.bias_add(conv2, conv2_biases))

        # 实现第四层池化层的前向传播过程，这一层是输入为14*14*64，输出为7*7*64
        with tf.compat.v1.name_scope("layer4-pool2"):
            pool2 = tf.compat.v1.nn.max_pool(
                relu2, ksize=[1, 2, 2, 1],strides=[1, 2, 2, 1], padding="SAME"
            )

        # 将第四层池化层的输出转化为第五层全连接层输入格式，第四层输出为7*7*64的矩阵，然而第五层全连接需要的输入格式为向量，所以在这里需要
        # 降维。注意因为每一层神经网络的输入输出都为一个batch的矩阵，所以在这里得到的纬度也包含了一个batch中数据的个数。
        pool_shape = pool2.get_shape().as_list()
        # 计算将矩阵降维成向量之后的长度，这个长度就是矩阵长款及深度的城际，注意这里pool_shape[0]为一个batch中数据的个数
        nodes = pool_shape[1] * pool_shape[2] * pool_shape[3]

        # 通过tf.reshape函数将第四层的输出变为一个batch向量
        reshaped = tf.reshape(pool2, [pool_shape[0], nodes])

        # 声明第五层全连接层的变量并实现前向传播过程，这一层的输入为拉直之后的一组向量--长度为3136，输出为长度为512的向量
        # dropout可以避免过拟合，在训练时会随机将部分节点的输出改为0。
        with tf.compat.v1.variable_scope("layer5-fc1"):
            fc1_weights = tf.compat.v1.get_variable(
                "weight", [nodes, Convolution.FC_SIZE], initializer=tf.compat.v1.truncated_normal_initializer(stddev=0.1)
            )
            tf.compat.v1.add_to_collection("convolution_inference", fc1_weights)
            # 只有全连接层的权重需要加入正则化
            if regularizer:
                tf.compat.v1.add_to_collection("losses1", regularizer(fc1_weights))
            fc1_biases = tf.compat.v1.get_variable(
                "bias", [Convolution.FC_SIZE], initializer=tf.compat.v1.constant_initializer(0.1)
            )
            tf.compat.v1.add_to_collection("convolution_inferencee", fc1_biases)
            fc1 = tf.compat.v1.nn.relu(tf.compat.v1.matmul(reshaped, fc1_weights) + fc1_biases)
            if train:
                fc1 = tf.compat.v1.nn.dropout(fc1, 1.0)

        # 声明第六层全连接层的变量并实现前向传播过程，这一层的输入为一组长度为512的向量，输出为长度为10的变量
        with tf.compat.v1.variable_scope("layer6-fc2"):
            fc2_weights = tf.compat.v1.get_variable(
                "weight", [Convolution.FC_SIZE, NUM_LABELS], initializer=tf.compat.v1.truncated_normal_initializer(
                    stddev=0.1))
            tf.compat.v1.add_to_collection("convolution_inference", fc2_weights)
            if regularizer:
                tf.compat.v1.add_to_collection("losses1", regularizer(fc2_weights))
            fc2_biases = tf.compat.v1.get_variable(
                "bias", [NUM_LABELS], initializer=tf.compat.v1.constant_initializer(0.1)
            )
            tf.compat.v1.add_to_collection("convolution_inference", fc2_biases)
            logit = tf.compat.v1.matmul(fc1, fc2_weights) + fc2_biases

        return logit, tf.compat.v1.get_collection("convolution_inference")