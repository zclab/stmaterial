---
blogpost: true
date: Jan 15, 2022
author: 子川
category: 程序语言
tags: python, typing
---

# Python 中 `typing` 模块和类型注解的使用

Python 运行时不强制执行函数和变量类型注解，但这些注解可用于类型检查器、IDE、静态检查器等第三方工具。`typing` 模块提供对类型提示的运行时支持。最基本的支持包括 `Any` , `Union` , `Callable` , `TypeVar` , 和 `Generic` 。

## 实例引入

我们知道 Python 是一种动态语言，在声明一个变量时我们不需要显式地声明它的类型，例如下面的例子：

```python
a = 2
print('1 + a =', 1 + a)
```

运行结果：

```python
1 + a = 3
```

这里我们首先声明了一个变量 a，并将其赋值为了 2，然后将最后的结果打印出来，程序输出来了正确的结果。但在这个过程中，我们没有声明它到底是什么类型。 但如果这时候我们将 a 变成一个字符串类型，结果会是怎样的呢？改写如下：

```python
a = '2'
print('1 + a =', 1 + a)
```

运行结果：

```python
TypeError: unsupported operand type(s) for +: 'int' and 'str'
```

直接报错了，错误原因是我们进行了字符串类型的变量和数值类型变量的加和，两种数据类型不同，是无法进行相加的。 如果我们将上面的语句改写成一个方法定义：

```python
def add(a):
    return a + 1
```

这里定义了一个方法，传入一个参数，然后将其加 1 并返回。 如果这时候如果用下面的方式调用，传入的参数是一个数值类型：

```python
add(2)
```

则可以正常输出结果 3。但如果我们传入的参数并不是我们期望的类型，比如传入一个字符类型，那么就会同样报刚才类似的错误。 但又由于 Python 的特性，很多情况下我们并不用去声明它的类型，因此从方法定义上面来看，我们实际上是不知道一个方法的参数到底应该传入什么类型的。 这样其实就造成了很多不方便的地方，在某些情况下一些复杂的方法，如果不借助于一些额外的说明，我们是不知道参数到底是什么类型的。 因此，Python 中的类型注解就显得比较重要了。

## 类型注解

在 Python 3.5 中，Python PEP 484 引入了类型注解（type hints），在 Python 3.6 中，PEP 526 又进一步引入了变量注解（Variable Annotations），所以上面的代码我们改写成如下写法：

```python
a: int = 2
print('5 + a =', 5 + a)

def add(a: int) -> int:
    return a + 1
```

具体的语法是可以归纳为两点：

- 在声明变量时，变量的后面可以加一个冒号，后面再写上变量的类型，如 int、list 等等。
- 在声明方法返回值的时候，可以在方法的后面加一个箭头，后面加上返回值的类型，如 int、list 等等。

在 PEP 8 中，具体的格式是这样规定的：

- 在声明变量类型时，变量后方紧跟一个冒号，冒号后面跟一个空格，再跟上变量的类型。
- 在声明方法返回值的时候，箭头左边是方法定义，箭头右边是返回值的类型，箭头左右两边都要留有空格。

有了这样的声明，以后我们如果看到这个方法的定义，我们就知道传入的参数类型了，如调用 add 方法的时候，我们就知道传入的需要是一个数值类型的变量，而不是字符串类型，非常直观。 但值得注意的是，这种类型和变量注解实际上只是一种类型提示，对运行实际上是没有影响的，比如调用 add 方法的时候，我们传入的不是 int 类型，而是一个 float 类型，它也不会报错，也不会对参数进行类型转换，如：

```python
add(1.5)
```

我们传入的是一个 float 类型的数值 1.5，看下运行结果：

```python
2.5
```

可以看到，运行结果正常输出，而且 1.5 并没有经过强制类型转换变成 1，否则结果会变成 2。 因此，类型和变量注解只是提供了一种提示，对于运行实际上没有任何影响。 不过有了类型注解，一些 IDE 是可以识别出来并提示的，比如 PyCharm 就可以识别出来在调用某个方法的时候参数类型不一致，会提示 WARNING。 比如上面的调用，如果在 PyCharm 中，就会有如下提示内容：

```python
Expected type 'int', got 'float' instead
This inspection detects type errors in function call expressions. Due to dynamic dispatch and duck typing, this is possible in a limited but useful number of cases. Types of function parameters can be specified in docstrings or in Python 3 function annotations.
```

另外也有一些库是支持类型检查的，比如 mypy，安装之后，利用 mypy 即可检查出 Python 脚本中不符合类型注解的调用情况。 上面只是用一个简单的 int 类型做了实例，下面我们再看下一些相对复杂的数据结构，例如列表、元组、字典等类型怎么样来声明。 可想而知了，列表用 list 表示，元组用 tuple 表示，字典用 dict 来表示，那么很自然地，在声明的时候我们就很自然地写成这样了：

```python
names: list = ['Germey', 'Guido']
version: tuple = (3, 7, 4)
operations: dict = {'show': False, 'sort': True}
```

这么看上去没有问题，确实声明为了对应的类型，但实际上并不能反映整个列表、元组的结构，比如我们只通过类型注解是不知道 `names` 里面的元素是什么类型的，只知道 `names` 是一个列表 `list` 类型，实际上里面都是字符串 `str` 类型。我们也不知道 `version` 这个元组的每一个元素是什么类型的，实际上是 `int` 类型。但这些信息我们都无从得知。因此说，仅仅凭借 `list`、`tuple` 这样的声明是非常 “弱” 的，我们需要一种更强的类型声明。 这时候我们就需要借助于 `typing` 模块了，它提供了非常 “强 “的类型支持，比如 `List[str]`、`Tuple[int, int, int]` 则可以表示由 `str` 类型的元素组成的列表和由 `int` 类型的元素组成的长度为 3 的元组。所以上文的声明写法可以改写成下面的样子：

```python
from typing import List, Tuple, Dict

names: List[str] = ['Germey', 'Guido']
version: Tuple[int, int, int] = (3, 7, 4)
operations: Dict[str, bool] = {'show': False, 'sort': True}
```

这样一来，变量的类型便可以非常直观地体现出来了。 目前 `typing` 模块也已经被加入到 Python 标准库中，不需要安装第三方模块，我们就可以直接使用了。

## `typing`

下面我们再来详细看下`typing` 模块的具体用法，这里主要会介绍一些常用的注解类型，如 `List`、`Tuple`、`Dict`、`Sequence` 等等，了解了每个类型的具体使用方法，我们可以得心应手的对任何变量进行声明了。 在引入的时候就直接通过 `typing` 模块引入就好了，例如：

```python
from typing import List, Tuple
```

### `List`

`List`、列表，是 list 的泛型，基本等同于 list，其后紧跟一个方括号，里面代表了构成这个列表的元素类型，如由数字构成的列表可以声明为：

```python
var: List[int or float] = [2, 3.5]
```

另外还可以嵌套声明都是可以的：

```python
var: List[List[int]] = [[1, 2], [2, 3]]
```

### `Tuple`、`NamedTuple`

Tuple、元组，是 tuple 的泛型，其后紧跟一个方括号，方括号中按照顺序声明了构成本元组的元素类型，如 `Tuple[X, Y]` 代表了构成元组的第一个元素是 X 类型，第二个元素是 Y 类型。 比如想声明一个元组，分别代表姓名、年龄、身高，三个数据类型分别为 str、int、float，那么可以这么声明：

```python
person: Tuple[str, int, float] = ('Mike', 22, 1.75)
```

同样地也可以使用类型嵌套。 `NamedTuple`，是 `collections.namedtuple` 的泛型，实际上就和 `namedtuple` 用法完全一致，但个人其实并不推荐使用 `NamedTuple`，推荐使用 attrs 这个库来声明一些具有表征意义的类。

### `Dict`、`Mapping`、`MutableMapping`

`Dict`、字典，是 dict 的泛型；`Mapping`，映射，是 `collections.abc.Mapping` 的泛型。根据官方文档，`Dict` 推荐用于注解返回类型，`Mapping` 推荐用于注解参数。它们的使用方法都是一样的，其后跟一个中括号，中括号内分别声明键名、键值的类型，如：

```python
def size(rect: Mapping[str, int]) -> Dict[str, int]:
    return {'width': rect['width'] + 100, 'height': rect['width'] + 100}
```

这里将 Dict 用作了返回值类型注解，将 Mapping 用作了参数类型注解。 MutableMapping 则是 Mapping 对象的子类，在很多库中也经常用 MutableMapping 来代替 Mapping。

### `Set`、`AbstractSet`

`Set`、集合，是 `set` 的泛型；`AbstractSet`、是 `collections.abc.Set` 的泛型。根据官方文档，Set 推荐用于注解返回类型，`AbstractSet` 用于注解参数。它们的使用方法都是一样的，其后跟一个中括号，里面声明集合中元素的类型，如：

```python
def describe(s: AbstractSet[int]) -> Set[int]:
    return set(s)
```

这里将 Set 用作了返回值类型注解，将 `AbstractSet` 用作了参数类型注解。

### `Sequence`

`Sequence`，是 `collections.abc.Sequence` 的泛型，在某些情况下，我们可能并不需要严格区分一个变量或参数到底是列表 list 类型还是元组 `tuple` 类型，我们可以使用一个更为泛化的类型，叫做 `Sequence`，其用法类似于 `List`，如：

```python
def square(elements: Sequence[float]) -> List[float]:
    return [x ** 2 for x in elements]
```

### `NoReturn`

`NoReturn`，当一个方法没有返回结果时，为了注解它的返回类型，我们可以将其注解为 `NoReturn`，例如：

```python
def hello() -> NoReturn:
    print('hello')
```

### `Any`

Any，是一种特殊的类型，它可以代表所有类型，静态类型检查器的所有类型都与 Any 类型兼容，所有的无参数类型注解和返回类型注解的都会默认使用 Any 类型，也就是说，下面两个方法的声明是完全等价的：

```python
def add(a):
    return a + 1

def add(a: Any) -> Any:
    return a + 1
```

原理类似于 object，所有的类型都是 object 的子类。但如果我们将参数声明为 object 类型，静态参数类型检查便会抛出错误，而 Any 则不会，具体可以参考官方文档的说明：[Any 类型](https://docs.python.org/zh-cn/3/library/typing.html?highlight=typing#the-any-type)。

### `TypeVar`

`TypeVar`，我们可以借助它来自定义兼容特定类型的变量，比如有的变量声明为 `int`、`float`、`None` 都是符合要求的，实际就是代表任意的数字或者空内容都可以，其他的类型则不可以，比如列表 `list`、字典 `dict` 等等，像这样的情况，我们可以使用 `TypeVar` 来表示。 例如一个人的身高，便可以使用 `int` 或 `float` 或 `None` 来表示，但不能用 `dict` 来表示，所以可以这么声明：

```python
height = 1.75
Height = TypeVar('Height', int, float, None)
def get_height() -> Height:
    return height
```

这里我们使用 `TypeVar` 声明了一个 Height 类型，然后将其用于注解方法的返回结果。

### `NewType`

`NewType`，我们可以借助于它来声明一些具有特殊含义的类型，例如像 `Tuple` 的例子一样，我们需要将它表示为 `Person`，即一个人的含义，但但从表面上声明为 `Tuple` 并不直观，所以我们可以使用 `NewType` 为其声明一个类型，如：

```python
Person = NewType('Person', Tuple[str, int, float])
person = Person(('Mike', 22, 1.75))
```

这里实际上 person 就是一个 tuple 类型，我们可以对其像 tuple 一样正常操作。

### `Callable`

`Callable`，可调用类型，它通常用来注解一个方法，比如我们刚才声明了一个 `add` 方法，它就是一个 `Callable` 类型：

```python
print(Callable, type(add), isinstance(add, Callable))
```

运行结果：

```
typing.Callable <class 'function'> True
```

在这里虽然二者 `add` 利用 `type` 方法得到的结果是 function，但实际上利用 `isinstance` 方法判断确实是 `True`。 `Callable` 在声明的时候需要使用 `Callable[[Arg1Type, Arg2Type, ...], ReturnType]` 这样的类型注解，将参数类型和返回值类型都要注解出来，例如：

```python
def date(year: int, month: int, day: int) -> str:
    return f'{year}-{month}-{day}'

def get_date_fn() -> Callable[[int, int, int], str]:
    return date
```

这里首先声明了一个方法 date，接收三个 int 参数，返回一个 str 结果，`get_date_fn` 方法返回了这个方法本身，它的返回值类型就可以标记为 `Callable`，中括号内分别标记了返回的方法的参数类型和返回值类型。

### `Union`

`Union`，联合类型，`Union[X, Y]` 代表要么是 `X` 类型，要么是 `Y` 类型。 联合类型的联合类型等价于展平后的类型：

```python
Union[Union[int, str], float] == Union[int, str, float]
```

仅有一个参数的联合类型会坍缩成参数自身，比如：

```python
Union[int] == int
```

多余的参数会被跳过，比如：

```python
Union[int, str, int] == Union[int, str]
```

在比较联合类型的时候，参数顺序会被忽略，比如：

```python
Union[int, str] == Union[str, int]
```

这个在一些方法参数声明的时候比较有用，比如一个方法，要么传一个字符串表示的方法名，要么直接把方法传过来：

```python
def process(fn: Union[str, Callable]):
    if isinstance(fn, str):
        # str2fn and process
        pass
    elif isinstance(fn, Callable):
        fn()
```

这样的声明在一些类库方法定义的时候十分常见。

### `Optional`

`Optional`，意思是说这个参数可以为空或已经声明的类型，即 `Optional[X]` 等价于 `Union[X, None]`。 但值得注意的是，这个并不等价于可选参数，当它作为参数类型注解的时候，不代表这个参数可以不传递了，而是说这个参数可以传为 `None`。 如当一个方法执行结果，如果执行完毕就不返回错误信息， 如果发生问题就返回错误信息，则可以这么声明：

```python
def judge(result: bool) -> Optional[str]:
    if result: return 'Error Occurred'
```

### `Generator`

如果想代表一个生成器类型，可以使用 `Generator`，它的声明比较特殊，其后的中括号紧跟着三个参数，分别代表 `YieldType`、`SendType`、`ReturnType`，如：

```python
def echo_round() -> Generator[int, float, str]:
    sent = yield 0
    while sent >= 0:
        sent = yield round(sent)
    return 'Done'
```

在这里 `yield` 关键字后面紧跟的变量的类型就是 `YieldType`，`yield` 返回的结果的类型就是 `SendType`，最后生成器 return 的内容就是 `ReturnType`。 当然很多情况下，生成器往往只需要 `yield` 内容就够了，我们是不需要 `SendType` 和 `ReturnType` 的，可以将其设置为空，如：

```python
def infinite_stream(start: int) -> Generator[int, None, None]:
    while True:
        yield start
        start += 1
```

## 案例实战

接下来让我们看一个实际的项目，看看经常用到的类型一般是怎么使用的。 这里我们看的库是 requests-html，是由 Kenneth Reitz 所开发的，其 GitHub 地址为：[https://github.com/psf/requests-html](https://github.com/psf/requests-html)，下面我们主要看看它的源代码中一些类型是如何声明的。 这个库的源代码其实就一个文件，那就是 [requests_html.py](https://github.com/psf/requests-html/blob/master/requests_html.py)，我们看一下它里面的一些 `typing` 的定义和方法定义。 首先 Typing 的定义部分如下：

```python
from typing import Set, Union, List, MutableMapping, Optional

_Find = Union[List['Element'], 'Element']
_XPath = Union[List[str], List['Element'], str, 'Element']
_Result = Union[List['Result'], 'Result']
_HTML = Union[str, bytes]
_BaseHTML = str
_UserAgent = str
_DefaultEncoding = str
_URL = str
_RawHTML = bytes
_Encoding = str
_LXML = HtmlElement
_Text = str
_Search = Result
_Containing = Union[str, List[str]]
_Links = Set[str]
_Attrs = MutableMapping
_Next = Union['HTML', List[str]]
_NextSymbol = List[str]
```

这里可以看到主要用到的类型有 `Set`、`Union`、`List`、`MutableMapping`、`Optional`，这些在上文都已经做了解释，另外这里使用了多次 `Union` 来声明了一些新的类型，如 `_Find` 则要么是是 Element 对象的列表，要么是单个 Element 对象，`_Result` 则要么是 Result 对象的列表，要么是单个 Result 对象。另外 `_Attrs` 其实就是字典类型，这里用 MutableMapping 来表示了，没有用 `Dict`，也没有用 `Mapping`。 接下来再看一个 `Element` 类的声明：

```python
class Element(BaseParser):
    """An element of HTML.
    :param element: The element from which to base the parsing upon.
    :param url: The URL from which the HTML originated, used for ``absolute_links``.
    :param default_encoding: Which encoding to default to.
    """

    __slots__ = [
        'element', 'url', 'skip_anchors', 'default_encoding', '_encoding',
        '_html', '_lxml', '_pq', '_attrs', 'session'
    ]

    def __init__(self, *, element, url: _URL, default_encoding: _DefaultEncoding = None) -> None:
        super(Element, self).__init__(element=element, url=url, default_encoding=default_encoding)
        self.element = element
        self.tag = element.tag
        self.lineno = element.sourceline
        self._attrs = None

    def __repr__(self) -> str:
        attrs = ['{}={}'.format(attr, repr(self.attrs[attr])) for attr in self.attrs]
        return "<Element {} {}>".format(repr(self.element.tag), ' '.join(attrs))

    @property
    def attrs(self) -> _Attrs:
        """Returns a dictionary of the attributes of the :class:`Element <Element>`
        (`learn more <https://www.w3schools.com/tags/ref_attributes.asp>`_).
        """
        if self._attrs is None:
            self._attrs = {k: v for k, v in self.element.items()}

            # Split class and rel up, as there are ussually many of them:
            for attr in ['class', 'rel']:
                if attr in self._attrs:
                    self._attrs[attr] = tuple(self._attrs[attr].split())

        return self._attrs
```

这里 `__init__` 方法接收非常多的参数，同时使用 `_URL` 、`_DefaultEncoding` 进行了参数类型注解，另外 `attrs` 方法使用了 `_Attrs` 进行了返回结果类型注解。 整体看下来，每个参数的类型、返回值都进行了清晰地注解，代码可读性大大提高。 以上便是类型注解和 `typing` 模块的详细介绍。
