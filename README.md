# CMStoWechat_opensource_version
自己写的数据库到httpapi接口，去除公司内部信息后开源
## 1. 项目起源
公司内部ERP由PB+Java中间件+oracle组成假三层结构，PB较难进行http调用且没有能够支持的工程师。同时，面对业务需求的扩张，需要提供较多针对业务人员的提醒和告知功能。

在此项目前期，尝试使用MQ制作简单ESB，本项目有一部分代码脱胎于前期的ESB项目。

在此情况下，我利用业余时间学习了python来进行设计和开发这个功能。
## 2. 软件设计

基于需要主动从数据库中抓取数据的现实情况，需要python侧主动去获取oracle内的数据。基于此，同时考虑未来其他数据库取数据的需求，使用python中ORM来进行。ORM使用sqlalchemy来进行操作。

ORM获取到数据后利用MQ将数据传递至发送端，发送端考虑业务逻辑添加了BerkeleyDB用于存储发送端会产生并收集的各种数据。选择BerkeleyDB原因为嵌入式高可靠性，同时体积较为合适且没有无用的tcpip连接，执行效率非常高。

因ERP业务量较大，考虑读写分离将ORM设置为映射模式，没有使用反射。

程序优先考虑解耦，不对任何组件增加过多的粘性。

## 3. 业务流程

业务通过数据写入ERP接口表，python通过ORM连接数据库，轮询获取数据。

获取到的数据提取关键信息序列化后发送至MQ，MQ传递至消费者端后后反序列化并进行数据格式化。

消费者端初始化时获取token，优先从BerkeleyDB内获取Token，Token发送返回错误信息后重新从server获取Token并存入BerkeleyDB，在Token确认到后进行发送。

发送尝试3次，3次内成功将数据计入成功，失败数据计入BerkeleyDB。

以上为大致的业务流程。

## 4. 程序结构

/BSDDB/                         -BDB存储文件

/log/                           -日志文件

/parameter/log_parameter.json   -日志配置文件

/parameter/parameter.json       -程序主配置文件

/parameter/SHA1                 -程序配置校验码

/part_consumer/                 -MQ消费者端程序

/part_producer/                 -MQ生产者端程序

/tools/hashchecker.py           -hash校验程序

/BerkeleyDB.py                  -封装BSDDB类

/getData.py                     -ORM数据获取类

/getToken.py                    -微信平台Token获取类

/hashcheck.py                   -配置文件校验类

/json2para.py                   -配置文件读取类

/logger.py                      -日志类

/mainMessage.py                 -数据库侧主程序，负责抓取数据

/makeDataModel.py               -数据格式化类

/sendMessage.py                 -封装消费者侧类

/sendtoWechatMain.py            -消费者主类

/initial step.md                -安装步骤

## 5. 鸣谢
感谢在本项目中给我各种建议和支持的各位小伙伴，没有你们的建议不会有这个小工具的完工。

*以下排名不分先后*

```
liangxi
yoka24443
NewOnePerson
key
一
mark
春哥
shanping
涛哥
```
