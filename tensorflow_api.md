### api
`tf.clip_by_value(t, clip_value_min, clip_value_max, name=None)`: 基于定义的min与max对tesor数据进行截断操作，目的是为了应对梯度爆发或者
梯度消失的情况。

`sigmoid和函数`: f(x) = 1/(1+exp(-x)),函数图像如下：

![sigmod](https://images2015.cnblogs.com/blog/1204043/201707/1204043-20170721183401542-1855738269.png)
