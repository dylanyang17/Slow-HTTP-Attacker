# Slow-HTTP-Attacker

将三种 slow HTTP 攻击移植到了 python 上，包括 Header 型、POST 型、Read 型，实现了多线程。

参考 repo：

* slowhttptest：参考该仓库功能进行开发，https://github.com/shekyan/slowhttptest
* slowloris：Header 型，为 python 代码，以该代码为基础开发，https://github.com/gkbrk/slowloris

## 运行

### 例子

* `python main.py https://target.com:1234/target/path` 即可使用 Header 型攻击以默认配置攻击 target.com 的 1234 端口，并且攻击路径为 `/target/path`，且使用了 HTTPS。
* `python main.py -m=READ --sockets=1000 http://target.com` 即可使用 READ 型攻击用 1000 个线程攻击 target.com

### 详细说明

详细使用说明如下：

```
usage: main.py [-h] [-m MODE] [-s SOCKETS] [-v] [-ua] [--sleeptime SLEEPTIME]
               [-w WINDOW]
               [url]

Slow HTTP Attacker, a tool providing three types of slow HTTP attack.

positional arguments:
  url                   URL to perform stress test on.
                        ("http[s]://<host>[:port][/path]")

optional arguments:
  -h, --help            show this help message and exit
  -m MODE, --mode MODE  Mode of attack. The supported options are "HEADER",
                        "POST" and "READ". ("header" by default)
  -s SOCKETS, --sockets SOCKETS
                        Number of sockets to use in the test (150 by default)
  -v, --verbose         Increases logging
  -ua, --randuseragents
                        Randomizes user-agents with each request (False by
                        default)
  --sleeptime SLEEPTIME
                        Time to sleep between beats used in HEADER and POST
                        mode (15 by default)
  -w WINDOW, --window WINDOW
                        The window size used in READ mode (1 by default)
```