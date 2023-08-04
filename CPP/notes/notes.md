# 1. do while(0)

作用1：用于宏函数

```c++
#define WHERE_AM_I()                          \
    do                                        \
    {                                         \
        printf("%14p[%s]\n", this, __func__); \
    } while (0);
```

如果宏函数内部有多个函数，以下方式会导致错误

```c++
#define FUNC() func1();func2();

if (xxx)
    FUNC() // 错误


#define FUNC2() {func1(); func2();}
FUNC2(); // 多一个;
```
