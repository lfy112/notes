# brief

## 列表初始化

``` c++
init(int x, int y):a(x), b(y){}
```

const和引用必须使用列表初始化

## final & override

如果使用final修饰函数，只能修饰虚函数，这样就能阻止子类重写父类的这个函数

使用final关键字修饰过的类是不允许被继承的，也就是说这个类不能有派生类

override表示一定要在子类重写这个虚函数

## 默认模板参数

``` c++
template <typename T=int>	// C++98/03不支持这种写法, C++11中支持这种写法
void func(T t)
{
    cout << "current value: " << t << endl;
}
```

## 数值与字符串转换

to_string()

stoi()、stol()、stoll()等

## 静态断言

``` c++
static_assert(sizeof(long) == 4, "错误, 不是32位平台...");
```

在编译过程中即可进行断言。

由于静态断言的表达式是在编译阶段进行检测，所以在它的表达式中不能出现变量，也就是说这个表达式必须是常量表达式。

## noexcept

``` c++
double divisionMethod(int a, int b) noexcept(常量表达式);
```

不带常量表达式的noexcept相当于声明了noexcept（true），即不会抛出异常。

与 `throw()`动态异常声明不同的是，在 C++11 中如果`noexcept`修饰的函数抛出了异常，编译器可以选择直接调用`std::terminate()`函数来终止程序的运行，这比基于异常机制的`throw()`在效率上会高一些。

## decltype

用于推导类型，可以返回类型后置

``` c++
auto func(参数1, 参数2, ...) -> decltype(参数表达式)
```

## 基于范围的循环

* 使用普通的for循环方式（基于迭代器）遍历关联性容器， auto自动推导出的是一个迭代器类型，需要使用迭代器的方式取出元素中的键值对（和指针的操作方法相同）：
  it->first
  it->second
* 使用基于范围的for循环遍历关联性容器，auto自动推导出的类型是容器中的value_type，相当于一个对组（std::pair）对象，提取键值对的方式如下：
  it.first
  it.second。

## nullptr

如果源码是C++程序NULL就是0，如果是C程序NULL表示(void*)0。C++ 中，void * 类型无法隐式转换为其他类型的指针，此时使用 0 代替 ((void *)0)。

NULL定义为0，存在转换为int的可能

## 常量

常量表达式和非常量表达式的计算时机不同，非常量表达式只能在程序运行阶段计算出结果，但是常量表达式的计算往往发生在程序的编译阶段，这可以极大提高程序的执行效率。

表达“只读”语义的场景都使用 const，表达“常量”语义的场景都使用 constexpr

## 委托构造函数、继承构造函数

``` c++
class Test
{
public:
    Test() {};
    Test(int max)
    {
        this->m_max = max > 0 ? max : 100;
    }

    Test(int max, int min):Test(max)
    {
        this->m_min = min > 0 && min < max ? min : 1;
    }

    Test(int max, int min, int mid):Test(max, min)
    {
        this->m_middle = mid < max && mid > min ? mid : 50;
    }

    int m_min;
    int m_max;
    int m_middle;
};
```

继承构造函数：`using Base::Base;`

## 右值引用

常量左值引用是一个万能引用类型，它可以接受左值、右值、常量左值和常量右值。

如果是模板参数需要指定为T&&，如果是自动类型推导需要指定为auto &&，在这两种场景下 &&被称作未定的引用类型。==额外注意const T&&表示一个右值引用==

## move

使用std::move方法可以将左值转换为右值。使用这个函数并不能移动任何东西，而是和移动构造函数一样都具有移动语义，将对象的状态或者所有权从一个对象转移到另一个对象，只是转移，没有内存拷贝。

相当于：static_cast<T&&>(lvalue);

list<string> ls1 = ls;        // 需要拷贝, 效率低
list<string> ls2 = move(ls);  // 直接转移所有权，调用移动语义的赋值函数：T&& T::operator=(T&& rhs)

## function

函数指针：int (*func)(int, int)

``` c++
// 绑定一个普通函数
function<int(int, int)> f1 = add;
// 绑定以静态类成员函数
function<int(int, int)> f2 = T1::sub;
// 绑定一个仿函数
T2 t;
function<int(int, int)> f3 = t;
```

## bind

延迟传参数

``` c++
void printSum(int a, int b) {
    std::cout << "Sum: " << a + b << std::endl;
}

int main() {
    // 使用 std::bind 绑定函数和参数
    auto addFunc = std::bind(printSum, 10, std::placeholders::_1);

    // 调用函数对象，提供绑定的参数
    addFunc(5); // 输出 "Sum: 15"

    return 0;
}
```

将类的成员函数和对象绑定为仿函数

``` c++
class Test
{
    public:
    void output(int x, int y)
    {
        cout << "x: " << x << ", y: " << y << endl;
    }
    int m_number = 100;
};

int main(void)
{
    Test t;
    // 绑定类成员函数
    function<void(int, int)> f1 = 
        bind(&Test::output, &t, placeholders::_1, placeholders::_2);
    // 绑定类成员变量(公共)
    function<int&(void)> f2 = bind(&Test::m_number, &t);

    // 调用
    f1(520, 1314);
    f2() = 2333;
    cout << "t.m_number: " << t.m_number << endl;

    return 0;
}
```

