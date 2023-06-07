# JS介绍

*   JavaScript 是一种运行在客户端（浏览器）的编程语言
*   包含ECMAScript( 基础语法 )、web APIs （DOM、BOM）

## 书写位置

### 内部JavaScript

直接写在html文件里，用script标签包住，

script标签写在\</body>上面

### 外部JavaScript

写在以.js结尾的文件里，通过script标签引入

### 内联JavaScript

代码写在标签内部

## 输入输出

```javascript
// 输出
document.write('xxx')
alart('xxx')
console.log('xxx')
```

```javascript
// 输入
prompt('input')
```

## 变量

### 声明变量

`let age`声明一个age变量

新版本js使用let，不使用var

数组 `let arr = []`

常量 `const G = 9.8`

模板字符串 `document.write('hello, my name is${name}.')`

检测数据类型 `typeof x`

变量声明优先使用const，对象是引用类型，里面存储的是地址

## 运算符

### 比较运算符

\==：左右值是否相等

\===：左右类型和值是否相等

> 推荐使用===来进行判断

## 语句

### 分支语句

*   if
*   ?  : &#x20;
*   switch

## 数组

### 删除

pop() 方法从数组中删除最后一个元素，并返回该元素的值

shift() 方法从数组中删除第一个元素，并返回该元素的值

splice() 方法 删除指定元素

## 函数

```javascript
function func(){
	xxx
}

func();
```

如果形参过多 会自动填上undefined

如果实参过多 那么多余的实参会被忽略

```javascript
// 匿名函数
let fn = function() {
}
```

立即执行函数，避免全局变量之间的污染

```javascript
(function () {console.log(111) })();

(function () {console.log(111) }());
```

> 多个立即执行函数要用 ; 隔开，要不然会报错

## 对象

```javascript
let obj = {
	name: 'Sandman',
	age: 18,
	gander: '女'
}
```

增加属性：对象名.新属性 = 新值

删除属性：delete 对象名.属性

遍历对象：`for k in obj`

# Web APIs

DOM (文档对象模型)、BOM（浏览器对象模型）

## Dom获取&属性操作

### 获取DOM

`querySelectorAll()`
`querySelector()`
`querySelector()` 只能选择一个元素， 可以直接操作
`querySelectorAll()` 可以选择多个元素，得到的是伪数组，需要遍历得到每一个元素

里面写css选择器
必须是字符串，也就是必须加引号

### 操作元素内容

*   `innerText`：将文本内容添加/更新到任意标签位置，显示纯文本，不解析标签
*   `innerHTML`：将文本内容添加/更新到任意标签位置，会解析标签，多标签建议使用模板字符

### 操作元素属性

```javascript
// 1. 获取图片对象
const img = document.querySelector('img')
// 2. 随机得到序号
const random = getRandom(1, 6)
// 3. 更换路径
img.src = `./images/${random}.webp`
```

## Dom事件

### 事件监听

`元素对象.addEventListener('事件类型'， 要执行的函数)`
事件监听三要素：

*   事件源：哪个dom元素被事件触发了，要获取dom元素
*   事件类型：用什么方式触发，比如鼠标单击 click、鼠标经过 mouseover 等
*   事件调用的函数：要做什么事

### 事件类型

*   鼠标事件：click, mouseenter, mouseleave
*   焦点事件：focus, blur
*   键盘事件：Keydown, Keyup
*   文本事件：input

### 事件对象

在事件绑定的回调函数的第一个参数就是事件对象

```JavaScript
元素.addEventListener('click', function (e))

const input = document.querySelector('input')
input.addEventListener('keyup', function (e) {
  // console.log(11)
  // console.log(e.key)
  if (e.key === 'Enter') {
    console.log('我按下了回车键')
  }
})
```

### 事件流

事件流指的是事件完整执行过程中的流动路径
假设页面里有个div，当触发事件时，会经历两个阶段，分别是捕获阶段、冒泡阶段，捕获阶段是从父到子，冒泡阶段是从子到父

事件冒泡：当一个元素触发事件后，会依次向上调用所有父级元素的**同名事件**

# 正则表达式

定义：`const reg = /表达式/`
判断：`reg.test(被检测字符串)`，返回true/false
检索：`reg.exec(被检测字符串)`，返回数组/null

## 元字符

### 边界符

^ 表示开始位置
`$表示结束位置
如果 ^ 和$` 在一起，表示必须是精确匹配

```JavaScript
console.log(/^哈/.test('哈')) // true
console.log(/^哈/.test('哈哈')) // true
console.log(/^哈/.test('二哈')) // flase
console.log(/^哈$/.test('哈')) // true  只有这种情况为true 否则全是false
console.log(/^哈$/.test('哈哈')) // false
console.log(/^哈$/.test('二哈')) // false
```

### 量词

\* 重复0次或更多次
\+ 重复1次或更多次
? 重复0次或1次
{n} 重复n次
{n,} 重复n次或更多次
{n,m} 重复n到m次

### 字符类

\[ ] 匹配字符集合
\[a-z] 匹配a-z
\[a-zA-Z] 表示大小写都可以
\[^a-z] 匹配除了小写字母以外的字符
. 匹配除换行符之外的任何单个字符

\d 匹配0-9的任一数字，\[0-9]
\D \[^0-9]
\w 匹配任意字母数字下划线\[A-Za-z0-9\_]
\W \[^A-Za-z0-9\_]
\s 匹配空格（换行符、制表符）\[\t\r\n\v\f]
\S \[^\t\r\n\v\f]

## 修饰符

`/表达式/修饰符`
i 正则匹配时字母不区分大小写
g 匹配所有满足正则表达式的结果
