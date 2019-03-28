# CMS2Wechat
**cms微信消息接口**
## 待优化项目
****
*20190214*
1. 配置项目拉出来单独使用配置文件来维护
2. 使用logging模块记录log数据到文件
3. 将access_token和失败数据提交到某一个数据库内进行持久化（SQLlite或BerkeleyDB）
4. 制作一个守护进程
5. 编译打包成可执行文件
****
*20190216*
1. *20190214.1* 已实现
2. *20190214.2* 已实现
3. 新增优化项目
```
制作一个新的消费端适配器
```
****
*20190221*
1. *20190214.3* 模块已实现，等待完善
****
*20190223*
1. 完善BerkeleyDB操作包，封装class
****
*20190224*
1. 完善logger操作包，封装class
****
*20190226*
1. 新增优化项目
```
1. 取token后缓存token，每次发送数据从BSDDB内取token
2. 发送成功后，成功数据计入BSDDB成功表内
3. 发送失败三次后，失败数据计入BSDDB失败表内
```
****
*20190309*
1. 优化json2para包，封装配置项目装载类，增加了一个可变参数。
2. 优化hashcheck包，封装配置检查类。
3. 优化getToken包，调用新封装的json2para和BerkeleyDB类，遗留一部分未全部完成。
4. getToken代码逻辑优化，未全部完成。
****
*20190320*
1. 优化getToken包，TokenOperator类getToken方法优化。
****
*20190325*
1. 完成getToken包优化，添加getTokenFromDB和getTokenFromServer方法，并封装至getToken方法内进行调用。
****
*20190326*
1. 开始对sendmessage包进行封装优化。
