# CMake学习

## 1.单个源文件

单个源文件编写CMakeLists.txt，且保存在源文件同一个目录下

```cmake
# CMake 最低版本号要求
cmake_minimum_required (VERSION 2.8)

# 项目信息
project (Demo1)

# 指定生成目标
add_executable(Demo main.cpp)
```

之后执行在当前目录执行cmake.，生成Makefile后执行make即可进行编译。

## 2.单个目录，多个源文件

    ./Demo2
    	|
    	+--- main.cpp
    	|
    	+---func.cpp
    	|
    	+---func.h

此时的CMakeLists.txt编写为

```cmake
# CMake 最低版本号要求
cmake_minimum_required (VERSION 2.8)

# 项目信息
project (Demo2)

# 指定生成目标
add_executable(Demo main.cpp func.cpp)
```

可以使用`aux_source_directory(<dir> <variable>)`方法将dir内的源文件都加近来。

```cmake
# CMake 最低版本号要求
cmake_minimum_required (VERSION 2.8)

# 项目信息
project (Demo2)

# 查找当前目录下的所有源文件
# 并将名称保存到 DIR_SRCS 变量
aux_source_directory(. DIR_SRCS)

# 指定生成目标
add_executable(Demo ${DIR_SRCS})
```

## 3.多个目录，多个源文件

    ./Demo3
        |
        +--- main.cpp
        |
        +--- math/
              |
              +--- func.cpp
              |
              +--- func.h

可以将math目录内的文件编译成静态库，由main.cpp进行调用，需要在根目录和math目录下都编写CMakeLists.txt。

根目录下的CMakeLists.txt为

```cmake
# CMake 最低版本号要求
cmake_minimum_required (VERSION 2.8)

# 项目信息
project (Demo3)

# 查找当前目录下的所有源文件
# 并将名称保存到 DIR_SRCS 变量
aux_source_directory(. DIR_SRCS)

# 添加 math 子目录
add_subdirectory(math)

# 指定生成目标 
add_executable(Demo main.cpp)

# 添加链接库
target_link_libraries(Demo func)
```

使用命令`add_subdirectory`指明本项目包含一个子目录 math，这样 math 目录下的 CMakeLists.txt 文件和源代码也会被处理。

使用命令`target_link_libraries`指明可执行文件 main 需要连接一个名为 func 的链接库 。

math目录下的CMakeLists.txt

```cmake
# 查找当前目录下的所有源文件
# 并将名称保存到 DIR_LIB_SRCS 变量
aux_source_directory(. DIR_LIB_SRCS)

# 生成链接库
add_library (func ${DIR_LIB_SRCS})
```

使用命令`add_library`将 src 目录中的源文件编译为静态链接库。

## 杂项

### set

set用于定义变量，之后使用\${}方式取得变量中的值

### project

用来指定工程的名字和支持的语言，默认支持所有语言

### message

向终端输出用户自定义的信息

主要包含三种信息：

*   SEND_ERROR，产生错误，生成过程被跳过。
*   SATUS，输出前缀为-的信息。
*   FATAL_ERROR，立即终止所有 cmake 过程.

### add_executable

生成可执行文件

### add_subdirectory

`ADD_SUBDIRECTORY(source_dir [binary_dir] [EXCLUDE_FROM_ALL])`

*   这个指令用于向当前工程添加存放源文件的子目录，并可以指定中间二进制和目标二进制存放的位置
*   EXCLUDE_FROM_ALL函数是将写的目录从编译中排除，如程序中的example
*   ADD_SUBDIRECTORY(src bin)

    将 src 子目录加入工程并指定编译输出(包含编译中间结果)路径为bin 目录

    如果不进行 bin 目录的指定，那么编译结果(包括中间结果)都将存放在build/src 目录

### option

用于控制编译流程，类似宏定义`option(<variable> "<help_text>" [value])`

### add_definitions

类似于`#define`，可以转换为C中的define

[链接](https://blog.csdn.net/qq_35699473/article/details/115837708)

### foreach

foreach命令为list中的每个值评估一组命令

[链接](https://blog.csdn.net/fengbingchun/article/details/127819743)

### if

```cmake
if(<condition>)
  <commands>
elseif(<condition>) # optional block, can be repeated
  <commands>
else()              # optional block
  <commands>
endif()
```

> 注意：需要使用endif

[链接](https://blog.csdn.net/fengbingchun/article/details/127946047)

### string

[链接](https://blog.csdn.net/weixin_41923935/article/details/122155064)

#### 查找

```cmake
string(FIND <string> <substring> <output_variable> [REVERSE])
```

在`<string>`中查找`<substring>`，返回值存放于`<output_variable>`，找到则返回在`<string>`中的下标，找不到返回-1。默认为首次出现的匹配，如果使用了`REVERSE`则为最后一次匹配。注：下标从0开始，以字节做为单位，因此遇到中文时下标表示字符编码第一字节的位置。

#### 替换

```cmake
string(REPLACE <match_string> <replace_string> 
    		<output_variable> <input> [<input>...])
```

从所有`<input>`中查找`<match_string>`并使用`<replace_string>`替换，替换后的字符串存放于`<output_variable>`。多个输入时，先将所有输入连接后，再做查找替换。

#### 尾部追加

```cmake
string(APPEND <string_variable> [<input>...])
```

#### 头部追加

```cmake
string(PREPEND <string_variable> [<input>...])
```

#### 连接

```cmake
string(JOIN <glue> <output_variable> [<input>...])
```

使用`<glue>`作为连接符，连接所有`<input>`，输出于`<output_variable>`

#### 大小写转换

```cmake
string(TOLOWER <string> <output_variable>)
string(TOUPPER <string> <output_variable>)
```

#### 长度

```cmake
string(LENGTH <string> <output_variable>)
```

> 注意：中文这种多字节编码的字符，字节长度大于字符长度。

#### 取子串

```cmake
string(SUBSTRING <string> <begin> <length> <output_variable>)
```

> 注意：如果`<length>`为-1或大于源字符串长度则子串为余下全部字符串。

#### 正则查找

```cmake
string(REGEX MATCH <regular_expression> <output_variable> <input> [<input>...])
```

> 注意：使用match后，可以使用CMAKE\_MATCH\_1来获取匹配到的第一个内容

### strequal

**STREQUAL** 用于比较字符串，相同返回**true**。

### function

[链接](https://blog.csdn.net/wctzhong/article/details/124999633)

```cmake
function(<name> [<arg1> ...])
  <commands>
endfunction([<name>])
```

> 注意：调用function时，传入参数不能小于定义函数时规定的参数，但可以大于规定的参数数量，此时会只保留前几个

### add_custom_target

CMake中一切都是基于target的，如`add_library`会产生一个library的target，`add_executable`会产生一个exe的target等。`add_custom_target`会根据命令的参数生成一个target，这个target相对的可以更定制化一点。
如果`add_custom_target`只有一个参数，那么会将该参数视为要运行的命令

### add_dependencies

[链接](https://blog.csdn.net/BeanGuohui/article/details/120217097)

依赖指定
