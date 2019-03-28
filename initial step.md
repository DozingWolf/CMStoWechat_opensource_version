## 微信推送接口部署手册

*ver 20190214.1440*

**以下文件使用MD撰写，请注意。**

****

**数据库版本：Oracle11GR2及以上**

**OracleClient版本：12.2及以上**

**Python版本：3.6.5**

**MQ版本：3.7.9**

**Erlang版本：21.1**

**BerkeleyDB版本：Berkeley db-12.1.6.2.38_64**

*接口部署顺序请以数据库==>MQ==>Python==>Py包依赖顺序进行*

****

### 建立SQL

#### 建立接口表
```
    -- Create table
    create table ALM_WECHAT_LIST
    (
    id           NUMBER not null,
    compid       NUMBER,
    ownerid      NUMBER,
    bustype      VARCHAR2(5),
    generatetime DATE,
    message      VARCHAR2(4000),
    transflag    VARCHAR2(2) default '00',
    usercd       VARCHAR2(20) default '0000',
    usergrp      VARCHAR2(10) default '0000'
    )
    tablespace USERS
    pctfree 10
    initrans 1
    maxtrans 255
    storage
    (
        initial 64K
        next 1M
        minextents 1
        maxextents unlimited
    );
    -- Create/Recreate indexes
    create index IDX_ALM_WECHAT_LIST_TRANSFLAG on ALM_WECHAT_LIST (TRANSFLAG)
    tablespace USERS
    pctfree 10
    initrans 2
    maxtrans 255
    storage
    (
        initial 64K
        next 1M
        minextents 1
        maxextents unlimited
    );
    -- Create/Recreate primary, unique and foreign key constraints
    alter table ALM_WECHAT_LIST
    add constraint PK_ALM_WECHAT_LIST primary key (ID)
    using index
    tablespace USERS
    pctfree 10
    initrans 2
    maxtrans 255
    storage
    (
        initial 64K
        next 1M
        minextents 1
        maxextents unlimited
    );
```
#### 建立DBMS_JOB监控表
```
    -- Create table
    create table DBMS_MONITOR_PARAMETER
    (
    id           NUMBER not null,
    jobid        NUMBER,
    jobuse       VARCHAR2(20),
    generatetime DATE,
    usememo      VARCHAR2(200),
    createid     NUMBER,
    createuser   VARCHAR2(10),
    createdate   DATE,
    usergrp      VARCHAR2(10) default '0000',
    schemaname   VARCHAR2(30),
    ischack      VARCHAR2(1) default 'Y'
    )
    tablespace USERS
    pctfree 10
    initrans 1
    maxtrans 255
    storage
    (
        initial 64K
        next 1M
        minextents 1
        maxextents unlimited
    );
    -- Create/Recreate indexes
    create index IDX_DBMS_MONITOR_PARAMETER on DBMS_MONITOR_PARAMETER (JOBID)
    tablespace USERS
    pctfree 10
    initrans 2
    maxtrans 255
    storage
    (
        initial 64K
        next 1M
        minextents 1
        maxextents unlimited
    );
    -- Create/Recreate primary, unique and foreign key constraints
    alter table DBMS_MONITOR_PARAMETER
    add constraint PK_DBMS_MONITOR_PARAM primary key (ID)
    using index
    tablespace USERS
    pctfree 10
    initrans 2
    maxtrans 255
    storage
    (
        initial 64K
        next 1M
        minextents 1
        maxextents unlimited
    );
    alter table DBMS_MONITOR_PARAMETER
    add constraint UQ_DBMS_MONITOR_PARAM unique (JOBID);
```
#### 建立SEQ
```
    -- Create sequence
    create sequence SEQ_ALM_WECHAT_LIST
    minvalue 1
    maxvalue 9999999999999999999999999999
    start with 1
    increment by 1
    cache 20;

    -- Create sequence
    create sequence SEQ_DBMS_MONITOR_PARAMETER
    minvalue 1
    maxvalue 9999999999999999999999999999
    start with 1
    increment by 1
    cache 20;
```
#### 建立监控JOB
```
    declare
    an_qty     number;
    begin
    select count(1) into an_qty from dba_jobs sysjob
    inner join dbms_monitor_parameter monit on sysjob.JOB = monit.jobid
    where 1=1
        and sysjob.SCHEMA_USER = monit.schemaname
        and sysjob.BROKEN = 'Y'
        and monit.ischack = 'Y'
        and sysjob.next_date = to_date('4000/1/1','YYYY/MM/DD');
    if an_qty = 0 then
        null;
    else
        insert into ALM_WECHAT_LIST
        (id,compid,ownerid,bustype,generatetime,message,transflag,usercd,usergrp)
        select
        SEQ_ALM_WECHAT_LIST.NEXTVAL,1,1,
        'SYS',sysdate,'DBMS'||sysjob.JOB||'and JOBNAME'||monit.jobuse||'was broken,please check it asap. Now time is:'||to_char(sysdate,'YYYY/MM/DD hh24:mi'),
        '00','0000','0000'
        from dba_jobs sysjob
        inner join dbms_monitor_parameter monit on sysjob.JOB = monit.jobid
        where 1=1
        and sysjob.SCHEMA_USER = monit.schemaname
        and sysjob.BROKEN = 'Y'
        and monit.ischack = 'Y'
        and sysjob.next_date = to_date('4000/1/1','YYYY/MM/DD');
    end if;
    commit;
    end;
```
### 查询用例
```
select * from alm_wechat_list;

select * from dbms_monitor_parameter;
```
### 插入用例
```
insert into dbms_monitor_parameter
values(seq_dbms_monitor_parameter.nextval,643,'CMS定时任务监控','',
       '用于监控配置标记的CMS定时任务，本任务不自监控',0,'陈圣俞',sysdate,'0000','GRYL','N')

insert into ALM_WECHAT_LIST
(id,compid,ownerid,bustype,generatetime,message,transflag,usercd,usergrp,SCHEMANAME,ISCHECK
)
VALUES(SEQ_ALM_WECHAR_LIST.NEXTVAL,1,1,'SYS',sysdate,
'这是一条CMS测试信息，现在时间是'||to_char(sysdate,'YYYY/MM/DD hh24:mi')||'，您收到的这条消息来自CMS接口，收到这条信息代表MQ与接口服务器一切正常。',
'00','0000','0000','GRYL_TEST','N');
```
### 部署MQ
```
略，请自行查找相关资料
```
### Python3.6
#### 部署
```
略，请自行查找相关资料
```
#### 依赖包
**使用pip install或手动安装以下包文件，建议使用pip install**
```
pip(或手动安装以下包)
pika 0.12.0(必须0.12.0版本，1.0.0版本代码有区别 使用pip install pika==0.12.0命令安装)
cx_Oracle
sqlalchemy
json
cPickel
time
requests
bsddb3
```
### 部署Berkeley DB
```
Windows： 安装Berkeley db-12.1.6.2.38_64.msi文件，记录安装路径，即可
```
### 部署Oracle client
```
Windows： 安装winx64_12201_client，配置tnsnames.ora文件即可
```
