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

## POD

1. 使用默认的构造函数与析构函数
2. 没有虚函数或虚基类
3. 内存布局连续

可以使用memcpy等内存操作的函数

## 6个默认函数

1. 无参构造函数：创建类对象
2. 拷贝构造函数：拷贝类对象
3. 移动构造函数：拷贝类对象
4. 拷贝赋值函数：类对象赋值
5. 移动赋值函数：类对象赋值
6. 析构函数 ：销毁类对象

## shared_ptr

是线程安全的吗？

* 通过引用计数管理对象时是线程安全的
* 自身不是线程安全的，需要数据自身去保证安全，例如加锁或者原子操作

## thread

* join：主线程等待子线程结束
* detach：在线程分离之后，主线程退出也会一并销毁创建出的所有子线程，在主线程退出之前，它可以脱离主线程继续独立的运行，任务执行完毕之后，这个子线程会自动释放自己占用的系统资源

## call_once

定义once_flag g_flag;

call_once(g_flag, do_once);可以保证该函数只被调用一次

## mutex

* std::mutex：独占的互斥锁，不能递归使用
* std::timed_mutex：带超时的独占互斥锁，不能递归使用
* std::recursive_mutex：递归互斥锁，不带超时功能
* std::recursive_timed_mutex：带超时的递归互斥锁

## condition_variable

``` c++
mutex mtx;
condition_variable cv;
int cnt = 1;

int main() {
    auto func = [](int num) {
        unique_lock<mutex> lock(mtx);
        while(cnt!=num){
            cv.wait(lock);
        }
        cout << num << endl;
        cnt++;
        cv.notify_all();
    };
    thread t1(func, 1);
    thread t2(func, 2);
    thread t3(func, 3);
    thread t4(func, 4);

    t1.join();
    t2.join();
    t3.join();
    t4.join();
    return 0;
}
```

## atomic

内存约束模型

* `memory_order_relaxed`， 这是最宽松的规则，它对编译器和CPU不做任何限制，可以乱序
* `memory_order_release` **释放**，设定内存屏障(Memory barrier)，保证它之前的操作永远在它之前，但是它后面的操作可能被重排到它前面
* `memory_order_acquire` **获取**, 设定内存屏障，保证在它之后的访问永远在它之后，但是它之前的操作却有可能被重排到它后面，往往和Release在不同线程中联合使用
* `memory_order_consume`：改进版的`memory_order_acquire` ，开销更小
* `memory_order_acq_rel`，它是Acquire 和 Release 的结合，同时拥有它们俩提供的保证。比如你要对一个 atomic 自增 1，同时希望该操作之前和之后的读取或写入操作不会被重新排序
* `memory_order_seq_cst` **顺序一致性**， `memory_order_seq_cst` 就像是memory_order_acq_rel的加强版，它不管原子操作是属于读取还是写入的操作，只要某个线程有用到`emory_order_seq_cst` 的原子操作，线程中该`memory_order_seq_cst` 操作前的数据操作绝对不会被重新排在该`memory_order_seq_cst` 操作之后，且该`memory_order_seq_cst` 操作后的数据操作也绝对不会被重新排在`memory_order_seq_cst` 操作前。

## 多线程异步

使用future和async

```c++
int funv(void){
    return 100;
} 
std::future<int> result=std::async(std::launch::async, func); 
std::cout<<result.get();
```

使用packaged_task包装任务

```c++
int add(int a, int b, int c) {    
    std::cout << "call add\n";    
    return a + b + c; 
} 
void do_other_things() {    
    std::cout << "do_other_things" << std::endl; 
} 
int main() {    
    std::packaged_task<int(int, int, int)> task(add); // 封装任务    
    do_other_things();    
    std::future<int> result = task.get_future();    
    task(1, 1, 2); //必须要让任务执行，否则在get()获取future的值时会一直阻塞    
    std::cout << "result:" << result.get() << std::endl;    
    return 0; 
}
```

promise：手动从子线程内发出一个结果。创建promise时，会获得一个future，持有promise的线程可以从这个future里面get到结果。

在主线程中创建std::promise对象

将这个std::promise对象通过引用的方式传递给子线程的任务函数

在子线程任务函数中给std::promise对象赋值

在主线程中通过std::promise对象取出绑定的future实例对象

通过得到的future对象取出子线程任务函数中返回的值。

``` c++
void print(std::promise<std::string>& p) {  
    p.set_value("There is the result whitch you want."); } 
void do_some_other_things() { 
    std::cout << "Hello World" << std::endl; 
} 
int main() {  
    std::promise<std::string> promise;  
    std::future<std::string> result = promise.get_future();   
    std::thread th(print, std::ref(promise));   
    do_some_other_things();  
    std::cout << result.get() << std::endl;   
    th.join();  
    return 0; 
}
```
