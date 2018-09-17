# eval

eval() 函数用来执行一个字符串表达式，并返回表达式的值。

`eval(expression[, globals[, locals]])`

>expression -- 表达式。

>globals -- 变量作用域，全局命名空间，如果被提供，则必须是一个字典对象。

>locals -- 变量作用域，局部命名空间，如果被提供，可以是任何映射对象。

例子：

```
>>>x = 7
>>> eval( '3 * x' )
21
>>> eval('pow(2,2)')
4
>>> eval('2 + 2')
4
>>> n=81
>>> eval("n + 4")
85
```

# exec

`exec(object[, globals[, locals]])`:

exec 执行储存在字符串或文件中的 Python 语句，相比于 eval，exec可以执行更复杂的 Python 代码。

>object：必选参数，表示需要被指定的Python代码。它必须是字符串或code对象。如果object是一个字符串，该字符串会先被解析为一组Python语句，然后在执行（除
非发生语法错误）。如果object是一个code对象，那么它只是被简单的执行。

>globals：可选参数，表示全局命名空间（存放全局变量），如果被提供，则必须是一个字典对象。

>locals：可选参数，表示当前局部命名空间（存放局部变量），如果被提供，可以是任何映射对象。如果该参数被忽略，那么它将会取与globals相同的值。

例子：

```
>>> exec("print('hello,world')")
hello,world
```

```
>>> exec("""for _ in range(5):
...     print(_)""")
```
```
>>> x = 10
>>> expr = """
... z = 30
... sum = x + y + z
... print(sum)
... """
>>> def func():
...     y = 20
...     exec(expr)
...     exec(expr, {'x': 1,'y':2}) # 越靠近函数，参数的优先级越高
... 
>>> func()
60
33
```
