---
blogpost: true
date: Jul 03, 2021
author: 子川
category: 程序语言
tags: python, pathlib
---

# Python 中 `pathlib` 模块的使用

`pathlib` 是 python 3.4 才引进的一个较新的模块，`pathlib` 把每一个 `path` 封装成一个对象，通过操作对象来操作路径，非常体现类和对象的封装思想，而且通过对象操作，可以使用链式编程，非常方便。

## 实例化一个 `Path` 对象

使用方法：`Path([path字符串])` -> `Path` 对象

```python
>>> from pathlib import Path

#默认是当前目录‘.’
>>> Path()

#将path路径实例化对象
>>> Path('/etc/fstab')

#将path路径实例化对象
>>> Path('a/b')
```

## `Path` 路径查看

使用方法：`str(Path对象)` -> `Path` 路径字符

```python
>>> str(Path('/etc/fs'))
'/etc/fs'

>>> str(Path())
'.'

>>> str(Path('a/b'))
'a/b'
```

## 路径拼接操作符 `/`

Path实例化后的路径对象可以通过操作符 `/` 进行路径拼接

- `Path对象 / Path对象` -> `Path对象`
- `Paht对象 / 路径字符串` 或者 `路径字符串 / Paht对象` -> `Path对象`

```python
>>> P1 = Path('/root')
>>> P2 = Path('/data')
>>> P3 = Path('data')

>>> str(P1 / P2)
'/data'

>>> str(P1 / P3)
'/root/data'

>>> P1 / '/data'
PosixPath('/data')

>>> P1 / 'data'
PosixPath('/root/data')

>>> '/home' / P3
PosixPath('/home/data')
```

## 路径拼接方法

使用方法：`Path对象.joinpath(Path对象|path字符串)` -> `Path` 对象

实现的功能跟操作符 `/` 一样，也可以进行Path对象和字符串的拼接

```python
>>> P1 = Path('/root')
>>> P2 = Path('/data')
>>> P3 = Path('data')

>>> str(P1.joinpath(P2))
'/data'

>>> str(P1.joinpath(P3))
'/root/data'

>>> str(P1.joinpath('data'))
'/root/data'

>>> str(P1.joinpath('/data'))
'/data'
```

## 路径分解

使用方法：`Path对象.parts` -> `Tuple`

说明：

1. `parts` 是属性，不是方法
2. 将 `Path` 对象的路径分解成各个部分，然后封装成一个元组

```python
>>> P1 = Path('/root/dir1/test1.py')

>>> P1.parts
('/', 'root', 'dir1', 'test1.py')
```

## 一级父目录

使用方法：`Path对象.parent` -> `Path对象`

说明：

1. `parent` 是属性，不是方法
2. 返回的是一个 `Path` 对象，所以又可以进行对象操作

```python
>>> P1 = Path('/root/dir1/test1.py')

>>> P1.parent
PosixPath('/root/dir1')

>>> str(P1.parent.parent)
'/root'
```

## 多级父目录

使用方法：`Path对象.parents` -> `sequence`

说明：

1. 返回的是一个有序序列，可以通过 `list` 查看，或者 `for` 循环迭代
2. 序列的每一个元素都是 `Path` 对象
3. 既然是有序的，就可以用 `index`，`index` 为 0 的是父目录，`index` 为 1 的是祖父目录，以此类推到根目录

```python
>>> P1 = Path('/root/dir1/test1.py')

>>> P1.parents
<PosixPath.parents>

>>> list(P1.parents)
[PosixPath('/root/dir1'), PosixPath('/root'), PosixPath('/')]

>>> for i in P1.parents:
>>>     print(i)

/root/dir1
/root
/
```

## 查看Path对象的文件名称

使用方法：`Path对象.name` -> `文件名称`

说明：查看路径最后一部分的文件名称

```python
>>> P1 = Path('/root/dir1/test1.py')
>>> P1.name
'test1.py'

>>> P2 = Path('/root/dir1/test1.py/')
>>> P2.name
'test1.py'

>>> P3 = Path('/')
>>> P3.name
''
```

## 查看Path对象的文件名称

使用方法：`Path对象.stem` -> 不带后缀的文件名称

说明：

1.  查看路径最后一部分的不带后缀的文件名称
2.  不带后缀就是文件名称去掉 `.xxx` 的内容，只会去掉最后一个后缀名称

```python
>>> P1 = Path('/root/dir1/test1.py')
>>> P1.stem
'test1'

#如果有多个后缀，只会去掉最后一个后缀
>>> P2 = Path('/root/dir1/test1.tar.gz')
>>> P2.stem
'test1.tar'

>>> P3 = Path('/')
>>> P3.stem
''
```

## 查看Path对象的文件名称后缀

使用方法：`Path对象.suffix` -> 后缀名称

说明：

1. 如果一个文件有多个后缀，只会查看最后一个后缀的名称

```python
>>> P1 = Path('/root/dir1/test1.py')
>>> P1.suffix
'.py'

#如果有多个后缀，只会返回最后一个后缀名称
>>> P2 = Path('/root/dir1/test1.tar.gz')
>>> P2.suffix
'.gz'
```

## 查看Path对象的文件名称后缀

使用方法：`Path对象.suffixes` -> 后缀名称组成的列表

说明：

1. 将文件名的一个或多个后缀放到列表中
2. 适合有多个后缀名称的文件

```python
>>> P1 = Path('/root/dir1/test1.py')
>>> P1.suffixes
['.py']

>>> P2 = Path('/root/dir1/test1.tar.gz')
>>> P2.suffixes
['.tar', '.gz']
```

## 添加后缀名到路径尾部

使用方法：`Path对象.with_suffix(suffix)` -> `Path` 对象

① 给文件名添加指定后缀

② 如果文件名已经存在后缀，则替换

```python
#如果后缀已经存在，则替换
>>> P1 = Path('/root/dir1/test1.py')
>>> P1.with_suffix('.gz')
PosixPath('/root/dir1/test1.gz')

>>> P2 = Path('/root/dir1/test1')
>>> P2.with_suffix('.gz')
PosixPath('/root/dir1/test1.gz')

>>> P3 = Path('/root/dir1/test1/')
>>> P3.with_suffix('.gz')
PosixPath('/root/dir1/test1.gz')
```

## 替换路径的文件名

使用方法：`Path对象.with_name(name)` -> `Path` 对象

```python
>>> P1 = Path('/root/dir1/test1.py')
>>> P1.with_name('.gz')
PosixPath('/root/dir1/.gz')

>>> P2 = Path('/root/dir1/test1/')
>>> P2.with_name('good')
PosixPath('/root/dir1/good')
```

## 返回当前工作目录

使用方法：`Path.cwd()` -> `Path` 对象

```python
>>> P1.cwd()
PosixPath('/home/python/jupyter')
```

## 返回当前家目录

使用方法：`Path.home()` -> `Path` 对象

```python
>>> P1.home()
PosixPath('/home/python')
```

## `is` 系列的判断

① `exists()`：判断Path对象路径是否存在

② `is_dir()`：判断Path对象是否是目录

③ `is_file()`：判断Path对象是否是文件

④ `is_symlink()`：判断Path对象是否是链接文件

⑤ `is_socket()`：判断Path对象是否是套接字文件

⑥ `is_block_device()`：判断Path对象是否是块设备文件

⑦ `is_char_device()`：判断Path对象是否是字符设备文件

⑧ `is_absolute()`：判断Path对象是否是绝对路径

说明：判断的时候，要有查看的权限，不然会抛出异常

```python
>>> P1 = Path('/root/dir1/test1/')
>>> P1.is_file()
PermissionError: [Errno 13] Permission denied: '/root/dir1/test1'

>>> P2 = Path('/tmp/dirt/test1')
>>> P2.is_dir()
False

>>> P3 = Path('/etc/rc.local')
>>> P3.is_file()
True
>>> P3.is_symlink()
True
```

## 解析一个路径

使用方法：`Path对象.resolve()` -> `Path` 对象

说明：

① 如果Path对象是一个普通文件，则返回自身

② 如果Path对象是一个链接文件，则返回源文件

```python
#链接文件，返回源文件
>>> P1 = Path('/etc/rc.local')
>>> P1.resolve()
PosixPath('/etc/rc.d/rc.local')

#普通文件，返回自身
>>> P2 = Path('/etc/rc.d/rc.local')
>>> P2.resolve()
PosixPath('/etc/rc.d/rc.local')
```

## 删除一层空目录

使用方法：`Path对象.rmdir()`

说明：

① Path对象必须是一个空目录

```python
>>> P1 = Path('/tmp/test1.py')

#Path对象必须是一个空目录
>>> P1.rmdir()
NotADirectoryError: [Errno 20] Not a directory: '/tmp/test1.py'

#Path对象必须是一个空目录
>>> P2 = Path('/tmp/test_go')
>>> P2.rmdir()
OSError: [Errno 39] Directory not empty: '/tmp/test_go'

#成功删除
>>> P3 = Path('/tmp/test_go/dir2')
P3.rmdir()
```

## 创建一个文件

使用方法：`Paht对象.touch(mode=0oxxx)`

说明：

① 如果文件已经存在，则不会重新创建

② 指定文件权限使用八进制格式

```python
>>> P1 = Path('/tmp/test1.py')
>>> P1.touch()

>>> P2 = Path('/tmp/test3.py')
>>> P2.touch(0o777)
```

## 创建目录

使用方法：`Paht对象.mkdir(mode=0oxxx, parents=False,exist_ok=Fasle)`

说明：

① `mode`：指定目录权限，使用八进制格式

② `parents`：如果父目录不存在，是否创建，True 等同于 linux 的 `mkdir -p` 命令

③ `exist_ok`：Fasle表示，如果目录已经存在，则抛出异常，True 表示，如果目录存在不抛出异常

```python
>>> P1 = Path('/tmp/test_do')
>>> P1.mkdir(mode=0o744)

#默认只能创建一层空目录
>>> P2 = Path('/tmp/test_do/a/b/c')
>>> P2.mkdir()
FileNotFoundError: [Errno 2] No such file or directory: '/tmp/test_do/a/b/c'

#使用parents=True，可以递归创建目录
>>> P2.mkdir(parents=True)

#目录已经存在，再创建抛出异常
>>> P2.mkdir(parents=True)
FileExistsError: [Errno 17] File exists: '/tmp/test_do/a/b/c'

#目录已经存在，指定了exitst_ok=True，所以不抛出异常
>>> P2.mkdir(parents=True,exist_ok=True)
```

## 迭代当前目录

使用方法：`Path对象.iterdir()` -> `Generator`

说明：

① 只对当前目录进行迭代，不会渗透入到每个子目录

② 返回一个生成器，可以使用for循环进行迭代

```shell
[root@jimmy tmp]# tree test_go/
test_go/
|-- dir1
|   `-- dir1.py
|-- dir3
|-- test.p3
|-- test.py1
`-- test.py2

#对当前目录的所有文件（文件和目录）进行迭代
>>> P1 = Path('/tmp/test_go')
>>> for i in P1.iterdir():
>>>     print(i)

/tmp/test_go/dir1
/tmp/test_go/test.py2
/tmp/test_go/dir3
/tmp/test_go/test.py1
/tmp/test_go/test.p3
```

## 通过通配符查询指定路径下的文件

使用方法：`Path对象.glob(pattern)` -> `Generator`

说明：

① 只会查询指定目录的文件，不会递归

② 返回的是一个生成器，可以使用for循环，或者用list

③ 生成器的每一个元素都是一个 `Path` 对象

```shell
[root@jimmy tmp]# tree test_go/
test_go/
|-- dir1
|   |-- dir1.py
|   `-- test.py
|-- dir3
|-- test.p3
|-- test.py1
`-- test.py2

>>> P1 = Path('/tmp/test_go')

>>> list(P1.glob("py*"))
[]

#当前目录只有两个以test.py开头的文件，不会递归子目录
>>> list(P1.glob("test.py*"))
[PosixPath('/tmp/test_go/test.py2'), PosixPath('/tmp/test_go/test.py1')]
```

## 通过通配符查询指定路径下的文件

使用方法：`Path对象.rglob(pattern)` -> `Generator`

说明：

① 只会查询指定目录的文件，会递归每一个子目录

② 返回的是一个生成器，可以使用for循环，或者用list

③ 生成器的每一个元素都是一个 `Path` 对象

```shell
#当前所有目录有三个以test.py开头的文件，递归了子目录
>>> list(P1.rglob("test.py*"))
[PosixPath('/tmp/test_go/test.py2'),
 PosixPath('/tmp/test_go/test.py1'),
 PosixPath('/tmp/test_go/dir1/test.py')]
```

## 查看文件详细信息

使用方法：`Path对象.stat()`

说明：

① 等同于 linux 的 `stat` 命令，返回一个 `stat` 对象

② 如果是链接文件，会跟踪到源文件，使用 `lstat()` 查看的是文件本身

```python
>>> P1 = Path('/tmp/test_go')
>>> P1.stat()
os.stat_result(st_mode=16893, st_ino=256377, st_dev=64769, st_nlink=4, st_uid=1000, st_gid=1000, st_size=4096, st_atime=1554106724, st_mtime=1554186613, st_ctime=1554186613)

#返回一个stat对象，通过属性相关数值
>>> P1.stat().st_uid
100
```

## `Path` 使用总结

① 核心就是把一个路径封装成一个对象，通过对象的属性或者方法来操作路径

② 很多方法返回的仍然是一个 `Path` 对象，通过 `Path` 对象又可以访问属性或者调用访问，实现链式编程
