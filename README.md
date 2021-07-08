# zookeeper_load_balance
Zookeeper 版本分布式负载均衡

## 项目介绍

1. 使用flask 作为服务端演示，加多进程开启多个服务
2. 原理使用 **zookeeper**的 临时节点，共享服务负载状态
3. 客户端选择节点负载最小的一个进行连接，目前仅实现该算法

## 安装 kazoo 可能会出现问题

```
  File "D:\environment\python3.6\lib\site-packages\kazoo\handlers\utils.py", line 130, in _set_fd_cloexec
    flags = fcntl.fcntl(fd, fcntl.F_GETFD)
AttributeError: module 'fcntl' has no attribute 'F_GETFD'

```

### 解决方案

```
在 kazoo/hanlders/utils.py 上方

try:
    import fcntl
except ImportError:  # pragma: nocover
    HAS_FNCTL = False

改为 

HAS_FNCTL = False
```

## 博客, 项目说明

```
https://blog.csdn.net/weixin_42290927/article/details/118574217
```

