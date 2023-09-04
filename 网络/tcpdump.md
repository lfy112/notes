# tcpdump

## 常用过滤规则

### 基于IP的过滤：host

只截取这个ip的数据包：tcpdump host (ip)

捕获src\dst的数据包：tcpdump src\dst (ip)

### 基于网段的过滤：net

tcpdump net 192.168.1.0/24

### 基于端口的过滤：port

只抓取tcp协议的80端口：tcpdump tcp port 80

指定多个端口：tcpdump port 22 or port 80、tcpdump portrange 80-808

### 基于协议的过滤

tcpdump icmp

## 常用参数

### 指定网卡：-i

-i all

-i eth0

### 保存文件中：-w

-w filename

### 读取文件：-r

### 不将ip转域名：-n

### 不将端口和协议转名字：-nn

### 不打印host的域名部分：-N

### 不输出每一行的时间：-t

### 输出时间戳：-tt

### 输出两行之间的时间间隔：-ttt

### 输出时间戳之前添加日期：-tttt

### 输出更详细：-v，-vv，-vvv

### 抓指定数量的包：-c xxx

### 指定写入文件的最大大小：-C xx(MB)

