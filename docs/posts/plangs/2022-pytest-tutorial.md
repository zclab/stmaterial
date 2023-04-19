:::{post} Aug 17, 2022
---
category: 程序语言
tags: python, pytest
language: cn
author: 子川
location: 北京
exclude: true
---
`pytest` 是 python 的一种单元测试框架，与 python 自带的 `unittest` 测试框架类似，但是比 `unittest` 框架使用起来更简洁，效率更高。并且 `pytest` 兼容 `unittest` 的用例，支持的插件也更多。
:::


# `pytest` 使用总结笔记

## 简介

`pytest` 是 python 的一种单元测试框架，与 python 自带的 `unittest` 测试框架类似，但是比 `unittest` 框架使用起来更简洁，效率更高。并且 `pytest` 兼容 `unittest` 的用例，支持的插件也更多 [^pytest]。

**安装**

```bash
pip install pytest
```

简单上手，创建个 `test_sample.py` 文件

```python
def func(x):
    return x + 1

def test_answer():
    assert func(3) == 5
```


运行测试，直接在当前文件夹运行 `pytest`

```shell
collected 1 item

test_sample.py F                                                     [100%]

================================= FAILURES =================================
_______________________________ test_answer ________________________________

    def test_answer():
>       assert func(3) == 5
E       assert 4 == 5
E        +  where 4 = func(3)

test_sample.py:6: AssertionError
============================ 1 failed in 0.12s =============================
```


`pytest` 运行规则：查找当前目录及其子目录下以 `test_*.py` 或 `*_test.py` 文件，找到文件后，在文件中找到以 test 开头函数并执行。

**以类来封装用例**

```python
# content of test_class.py
class TestClass:
    def test_one(self):
        x = "this"
        assert "h" in x

    def test_two(self):
        x = "hello"
        assert hasattr(x, "check")
```


运行可以使用 `pytest [file_path]` 指定文件，`-q` 是静默模式，不会打印用例输出

```shell
$ pytest -q test_class.py
.F                                                                   [100%]
================================= FAILURES =================================
____________________________ TestClass.test_two ____________________________

self = <test_class.TestClass object at 0xdeadbeef>

    def test_two(self):
        x = "hello"
>       assert hasattr(x, "check")
E       AssertionError: assert False
E        +  where False = hasattr('hello', 'check')

test_class.py:8: AssertionError
1 failed, 1 passed in 0.12s
```


用例设计原则

* 文件名以 `test_*.py` 文件和 `*_test.py`
* 以 `test_` 开头的函数
* 以 `Test` 开头的类
* 以 `test_` 开头的方法
* 所有的包 pakege 必须要有 `__init__.py` 文件




## 执行用例

1. 执行某个目录下所有的用例
   ```bash
   pytest 文件名/
   ```
2. 执行某一个py文件下用例
   ```bash
   pytest 脚本名称.py
   ```
3. `-k` 按关键字匹配
   ```bash
   pytest -k "MyClass and not method"
   ```
   这将运行包含与给定字符串表达式匹配的名称的测试，其中包括 Python 使用文件名，类名和函数名作为变量的运算符。 上面的例子将运行 `TestMyClass.test_something` 但不运行 `TestMyClass.test_method_simple`

4. 按节点运行
   每个收集的测试都分配了一个唯一的 `nodeid`，它由模块文件名和后跟说明符组成来自参数化的类名，函数名和参数，由 `:: characters` 分隔。

   运行 `.py` 模块里面的某个函数
   ```bash
   pytest test_mod.py::test_func
   ```

   运行 `.py` 模块里面，测试类里面的某个方法
   ```bash
   pytest test_mod.py::TestClass::test_method
   ```
5. 标记表达式
   ```bash
   pytest -m slow
   ```
   将运行用 `@ pytest.mark.slow` 装饰器修饰的所有测试，slow是自己命名的标记，可以自定义

   ```python
   import pytest

    @pytest.mark.finished
    def test_send_http():
        pass  


    def test_something_quick():
        pass
    ```

    运行测试时使用 `-m` 选项可以加上逻辑

    ```
    >pytest -m "finished and commit"   //匹配finished和commit运行

    >pytest -m "finished and not merged"  //finished运行，merged不运行
    ```

6. 从包里面运行
    ```bash
    pytest --pyargs pkg.testing
    ```
    这将导入 `pkg.testing` 并使用其文件系统位置来查找和运行测试。
7. 在第一个（或N个）失败后停止
    ```
    pytest -x            # stop after first failure
    pytest --maxfail=2    # stop after two failures
    ```

8. 跳过测试
    使用 `pytest.mark.skip` 标记需要跳过的用例
    ```python
    @pytest.mark.skip(reason="not finished")
    def test_send_http():
        pass 
    ```

    也支持使用 `pytest.mark.skipif` 为测试函数指定被忽略的条件

    ```python
    @pytest.mark.skipif(finishflag==Fasle,reason="not finished")
    def test_send_http():
        pass 
    ```

9. 脚本调用执行
    直接使用
    ```bash
    pytest.main()
    ```

    像命令行一样传递参数
    ```bash
    pytest.main(["-x", "mytestdir"])
    ```



## 用例编写

### 断言

pytest 直接使用 python assert 语法来写

```python
def f():
    return 3

def test_function():
    assert f() == 4
```

断言中添加消息

```python
assert a % 2 == 0, "value was odd, should be even"
```


### 预设与清理

与 `unittest` 中的 `setup` 和 `teardown` 类似，`pytest` 也有这样的环境清理方法，主要有

* 模块级（`setup_module/teardown_module`）开始于模块始末，全局的
* 函数级（`setup_function/teardown_function`）只对函数用例生效（不在类中）
* 类级（`setup_class/teardown_class`）只在类中前后运行一次（在类中）
* 方法级（`setup_method/teardown_method`）开始于方法始末（在类中）
* 类里面的（`setup/teardown`）运行在调用方法的前后


```python
import pytest

class TestClass:
    
    def setup_class(self):
        print("setup_class：类中所有用例执行之前")

    def teardown_class(self):
        print("teardown_class：类中所有用例执行之前")

    def setup_method(self):
        print("setup_method:  每个用例开始前执行")

    def teardown_method(self):
        print("teardown_method:  每个用例结束后执行")

    def setup(self):
        print("setup: 每个用例开始前执行")

    def teardown(self):
        print("teardown: 每个用例结束后执行")

    def test_one(self):
        print("执行第一个用例")

    def test_two(self):
        print("执行第二个用例")

def setup_module():
    print("setup_module：整个.py模块只执行一次")

def teardown_module():
    print("teardown_module：整个.py模块只执行一次")

def setup_function():
    print("setup_function：每个方法用例开始前都会执行")

def teardown_function():
    print("teardown_function：每个方法用例结束前都会执行")

def test_three():
        print("执行第三个用例")
```


使用 `pytest -s test_sample.py` 运行，`-s` 参数是为了显示用例的打印信息，下面是输出，可以看出几个方法之间的优先级

```
test_sample.py setup_module：整个.py模块只执行一次
setup_class：类中所有用例执行之前
setup_method:  每个用例开始前执行
setup: 每个用例开始前执行
执行第一个用例
.teardown: 每个用例结束后执行
teardown_method:  每个用例结束后执行
setup_method:  每个用例开始前执行
setup: 每个用例开始前执行
执行第二个用例
.teardown: 每个用例结束后执行
teardown_method:  每个用例结束后执行
teardown_class：类中所有用例执行之前
setup_function：每个方法用例开始前都会执行
执行第三个用例
.teardown_function：每个方法用例结束前都会执行
teardown_module：整个.py模块只执行一次
```

:::{note}
`setup_method` 和 `teardown_method` 的功能和 `setup/teardown` 功能是一样的，一般二者用其中一个即可；函数里面用到的 `setup_function/teardown_function` 与类里面的 `setup_class/teardown_class` 互不干涉
:::


### 参数化

使用 `pytest.mark.parametrize(argnames, argvalues)` 可以实现函数的参数化

```python
@pytest.mark.parametrize('text',['test1','test2','test3'])
def test_one(text):
    print(text)
```

`argnames` 就是形参名称，`argvalues` 就是待测的一组数据.



## 固件 `fixture`
### 基本使用

固件 Fixture 是一些函数，pytest 会在执行测试函数之前（或之后）加载运行它们。主要是为一些单独测试用例需要预先设置与清理的情况下使用的。

不同于上面的 `setup` 和 `teardown` 的就是，可以自定义函数，可以指定用例运行，使用方法如下

```python
@pytest.fixture()
def text():
    print("开始执行")          #使用pytest.fixture()装饰一个函数成为fixture

def test_one():
    print("执行第一个用例")

def test_two(text):          #用例传入fixture函数名，以此来确认执行
    print("执行第二个用例")
```

使用 `yield` 可以实现固件的拆分运行，`yield` 前在用例前执行，`yield` 后再用例后执行

```python
@pytest.fixture()
def text():
    print("开始执行")
    yield                 #yield 关键词将固件分为两部分，yield 之前的代码属于预处理，会在测试前执行；yield 之后的代码属于后处理，将在测试完成后执行
    print("执行完毕")

def test_one():
    print("执行第一个用例")

def test_two(text):
    print("执行第二个用例")
```

### 统一管理

固件可以直接定义在各测试脚本中，就像上面的例子。更多时候，我们希望一个固件可以在更大程度上复用，这就需要对固件进行集中管理。Pytest 使用文件 `conftest.py` 集中管理固件。

不用显式调用 `conftest.py`，`pytest` 会自动调用，可以把 `conftest` 当做插件来理解


`./conftest.py`

```python
@pytest.fixture()
def text():
    print("开始执行")
    yield
    print("执行完毕")
```

`./test_sample.py`

```python
def test_one():
    print("执行第一个用例")

def test_two(text):
    print("执行第二个用例")
```


### 作用域

`fixture` 可以通过 `scope` 参数声明作用域，比如

* `function`: 函数级，每个测试函数都会执行一次固件；
* `class`: 类级别，每个测试类执行一次，所有方法都可以使用；
* `module`: 模块级，每个模块执行一次，模块内函数和方法都可使用；
* `session`: 会话级，一次测试只执行一次，所有被找到的函数和方法都可用。


`./conftest.py`
```python
@pytest.fixture(scope="module")
def text():
    print("开始执行")
    yield
    print("执行完毕")
```

`./test_sample.py`
```python
def test_one(text):
    print("执行第一个用例")

def test_two(text):
    print("执行第二个用例")
```

执行情况

```
test_sample.py 开始执行
执行第一个用例
.执行第二个用例
.执行完毕
```

如果对于类使用作用域，需要使用 `pytest.mark.usefixtures`（对函数和方法也适用）

`./conftest.py`
```python
@pytest.fixture(scope="class")
def text():
    print("开始执行")
    yield
    print("执行完毕")
```

`./test_sample.py`
```python
@pytest.mark.usefixtures('text')
class TestClass:

    def test_one(self):
        print("执行第一个用例")

    def test_two(self):
        print("执行第二个用例")
```


### 自动运行

将 `fixture` 的 `autouse` 参数设置为 True 时，可以不用传入函数，自动运行

`./conftest.py`
```python
@pytest.fixture(scope="module",autouse=True)
def text():
    print("开始执行")
    yield
    print("执行完毕")
```

`./test_sample.py`
```python
def test_one():
    print("执行第一个用例")

def test_two():
    print("执行第二个用例")
```


### 参数化

使用 `fixture` 的 `params` 参数可以实现参数化

`./conftest.py`
```python
@pytest.fixture(scope="module",params=['test1','test2'])
def text(request):
    print("开始执行")
    yield request.param
    print("执行完毕")
```

`./test_sample.py`
```python
def test_one(text):
    print("执行第一个用例")
    print(text)

def test_two(text):
    print("执行第二个用例")
```

固件参数化需要使用 `pytest` 内置的固件 `request`，并通过 `request.param` 获取参数。

结果如下

```
test_sample.py 开始执行
执行第一个用例
test1
.执行第二个用例
.执行完毕
开始执行
执行第一个用例
test2
.执行第二个用例
.执行完毕
```


## 生成报告
### HTML报告

安装 `pytest-html`
```bash
pip install pytest-html
```

使用方法是，直接在命令行pytest命令后面加--html=<文件名字或者路径>.html参数就可以了
```bash
pytest --html=report.html
```


上面生成的报告包括html和一个assets文件（里面是报告CSS样式），如果要合成一个文件可以添加下面的参数
```bash
pytest --html=report.html --self-contained-html
```


### XML报告
使用命令可以生成XML格式报告
```bash
pytest --junitxml=report.xml
```






[^pytest]: [pytest使用总结笔记](https://www.cnblogs.com/fengf233/p/11850188.html)
