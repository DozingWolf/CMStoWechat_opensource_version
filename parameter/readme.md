## 配置文件说明
### parameter.json
```
parameter.json文件内维护本系统使用的所有可配置参数。
具体项目请参见json文件。
因程序变动配置文件会变更，请注意使用的version编号。
更新维护配置文件后请使用hashcheker.py重新生成文件校验hashcode。
```
### SHA1
```
SHA1文件内存储系统需要校验的文件的hashcode。
以json形式存储。正确维护后将可以被系统自动读取。
因程序变更需要校验的文件也会随之变更，请注意校验信息。
```
