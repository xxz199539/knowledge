### api
`tf.clip_by_value(t, clip_value_min, clip_value_max, name=None)`: 基于定义的min与max对tesor数据进行截断操作，目的是为了应对梯度爆发或者梯度消失的情况。通俗来讲就是将一个张量中的数值限制在一个范围内，避免一些运算错误（比如log0是无效的）。

```
>>> with tf.Session() as sess:
...     v = tf.constant([[1.0,2.0,3.0],[4.0,5.0,6.0]])
...     print(tf.clip_by_value(v, 2.5, 4.5).eval())   # 要求输出结果在2.5和4.5之间
... 
[[2.5 2.5 3. ]
 [4.  4.5 4.5]]
```



`sigmoid和函数`: f(x) = 1/(1+exp(-x)),函数图像如下：


![sigmod](https://images2015.cnblogs.com/blog/1204043/201707/1204043-20170721183401542-1855738269.png)

梯度下降算法：

1.`tf.train.GradientDescentOptimizer()`

使用随机梯度下降算法，使参数沿着梯度的反方向，即总损失减小的方向移动，实现更新参数，图像如下：

![tf.train.GradientDescentOptimizer](https://upload-images.jianshu.io/upload_images/3070770-4b6c06932b494d6d.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/348/format/webp)

其中，J(θ)为损失函数，θ为参数，α为学习率

2.`tf.train.MomentumOptimizer()`

在更新参数时，利用了超参数，参数的更新公式是：

$d_i$ = $βd_{i-1}$ + g($θ_{i-1}$)

$θ_i$ = $θ_{i-1}$ - $αd_i$

其中，α是学学习率，超参数为β，θ为参数，g($θ_{i-1}$)为损失函数的梯度。



3.`tf.rain.AdamOptimizer()`

是利用自适应学习率的优化算法，Adam算法和随机梯度下降算法不同。随机梯度下降算法保持单一的学习率更新所有的参数，学习率在训练过程中并不会改变。而Adam算法通过计算梯度的一阶矩阵和二阶矩阵而为不同参数设计独立的自适应学习率。

学习率：决定每次参数更新的幅度。

优化器中都需要一个叫做学习率的参数，使用时，如果学习率选择过大会出现震 荡不收敛的情况，如果学习率选择过小，会出现收敛速度慢的情况。我们可以选 个比较小的值填入，比如 0.01、0.001



`np.random.RandomState(seed)`:通过随机数生成一个模拟数据集，seed为随机数种子

`np.random.RandomState(seed).rand(x,y)`:生成x行y列的随机数矩阵

```python
>>> RandomState(1).rand(5,2)
array([[4.17022005e-01, 7.20324493e-01],
       [1.14374817e-04, 3.02332573e-01],
       [1.46755891e-01, 9.23385948e-02],
       [1.86260211e-01, 3.45560727e-01],
       [3.96767474e-01, 5.38816734e-01]])
```



`cross_entropy`：

给定两个概率分布p和q，通过q来表示p的交叉熵为：

$$H(p,q) = -\sum_xp(x)logq(x)$$

它刻画的是通过概率分布q来表达概率分布p的困难程度。因为正确答案是希望得到的结果，所以当交叉熵作为神经网络损失函数时，p代表的是正确答案，q代表的是预测值，也就是说交叉熵越小，两个概率分布越近。

Demo:

假设有一个三分类问题，某个样例的正确答案是（1，0，0）。某模型经过`softmax`回归之后的预测答案是（0.5，0.4，0.1），那么这个预测和正确答案之间的交叉熵为:

$H((1,0,0),(0.5,0.4,0.1)) = -(1*log0.5 + 0*log0.4 + 0*log0.1) ≈0.3$

如果另一模型的预测是（0.8，0.1，0.1），那么这个预测值和真实值之间的交叉熵为：

$H((1,0,0),(0.8,0.1,0.1)) = -(1*log0.8 + 0*log0.1 + 0*log0.1) ≈0.1$

从直观上可以容易地知道第二个预测答案要优于第一个，计算结果亦是如此。



`tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y)`:因为交叉熵一般会与`softmax`回归一起使用，所有Tensorflow对这两个功能进行了统一封装。其中y代表原始神经网络的输出结果，而y_给出了正确答案。在只有一个正确答案的分类问题中，Tensorflow提供了该函数来进一步加速计算过程。



`tf.reduce_mean`:用于计算张量tensor沿着指定的数轴（tensor的某一维度）上的的平均值，主要用作降维或者计算tensor（图像）的平均值

```python
reduce_mean(input_tensor,               # 输入待降维的tensor
                axis=None,              # 指定的轴，如果不指定则计算所有的
                keep_dims=False,        # 是否降维，True：输出结果保持输入形状,False:降维
                name=None,              # 操作的名称
                reduction_indices=None) # 在以前的版本中指定轴，弃用

>>> x = [[1.0,2.0,3.0],[4.0,5.0,6.0]]
>>> mean_ = tf.reduce_mean(x, axis=0, keep_dims=False)
>>> with tf.Session() as sess:
...     print(sess.run(mean_))
... 
[2.5 3.5 4.5]
>>> mean_new = tf.reduce_mean(x, axis=1, keep_dims=False)
>>> with tf.Session() as sess:
...     print(sess.run(mean_new))
... 
[2. 5.]
```

`tf.log`:对张量中所有元素依次求对数

```
>>> v = tf.constant([1.0,2.0,3.0])
>>> with tf.Session() as sess:
...     print(sess.run(tf.log(v)))
... 
[0.        0.6931472 1.0986123]
```



`tf.greater(v1,v2)`:输入两个张量，比较这两个张量中每一个元素的大小，并返回比较结果，当输入的张量纬度不一样时，Tensorflow会进行类似Numpy广播操作处理。

```
>>> v1 = tf.constant([1.0,2.0,3.0,4.0])
>>> v2 = tf.constant([4.0,3.0,2.0,1.0])
>>> with tf.Session() as sess:
...     print(sess.run(tf.greater(v1,v2)))
... 
[False False  True  True]
```

`tf.where(condition,x=None,y=None,name=None)`:当condition为True，使用x，否则使用y。

```
>>> v1 = tf.constant([1.0,2.0,3.0,4.0])
>>> v2 = tf.constant([4.0,3.0,2.0,1.0])
>>> with tf.Session() as sess:
...     print(sess.run(tf.where(tf.greater(v1,v2),v1,v2)))
... 
WARNING: Logging before flag parsing goes to stderr.
W0724 12:44:48.449423 140735526716288 deprecation.py:323] From <stdin>:2: add_dispatch_support.<locals>.wrapper (from tensorflow.python.ops.array_ops) is deprecated and will be removed in a future version.
Instructions for updating:
Use tf.where in 2.0, which has the same broadcast rule as np.where
[4. 3. 3. 4.]
```



