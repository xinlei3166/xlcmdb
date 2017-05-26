# primumest-cmdb

### 本人初学python和前端知识，利用Bootstrap + saltsatck + paramiko + python 做了一个简单的CMDB平台。

#### 软件介绍
> 软件在win10下开发，linux主机使用Centos 7
>
> 本软件使用python 2.7开发
> 
> saltstack二次开发使用的是salt-api接口
> 
#### 已完成功能：
> 1.登录、注册、修改个人信息、修改密码
> 
> 2.主机添加、主机修改、主机删除
>
> 3.salt批量执行命令、批量安装salt-minion、批量认证、salt文件分发、paramiko-webssh
>
> 4.用户添加、用户删除、用户权限修改、组添加、组权限修改
#### 待完成功能
> 1.zabbix监控集成
>
> 2.数据使用图表动态展示
>
> 3.操作日志审计
>
> 4.Cobbler自动安装主机
>
> 5.自动探查主机并添加到集群

#### 使用说明
> 使用前请安装好python 2.7和搭建好saltsatck服务器
，安装并运行salt-api可以使用salt界面功能，salt-api接口地址在salt.yaml配置文件中进行修改。

#### 效果图展示：
1.用户界面

![注册.png](http://upload-images.jianshu.io/upload_images/4262139-7ad6fd1772adbed0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![登录.png](http://upload-images.jianshu.io/upload_images/4262139-acf6740a9378c15e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


![首页.png](http://upload-images.jianshu.io/upload_images/4262139-770709fa11c915f6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


![个人信息页.png](http://upload-images.jianshu.io/upload_images/4262139-2bf21cf0c0785da7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


![个人信息页-2.png](http://upload-images.jianshu.io/upload_images/4262139-508c02b275cb9a67.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


2.salt界面

![salt-minion列表页.png](http://upload-images.jianshu.io/upload_images/4262139-21596ed2b511c2ec.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


![salt执行命令页.png](http://upload-images.jianshu.io/upload_images/4262139-ee2e4f861163c332.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


![salt文件分发页.png](http://upload-images.jianshu.io/upload_images/4262139-dd453dd18f582608.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


![paramiko-webssh页.png](http://upload-images.jianshu.io/upload_images/4262139-4259014351571486.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



3.主机界面

![主机列表页.png](http://upload-images.jianshu.io/upload_images/4262139-75607e7c5c4fde9b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


![单台主机详情页.png](http://upload-images.jianshu.io/upload_images/4262139-b38e2fa4007de335.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


![主机修改页.png](http://upload-images.jianshu.io/upload_images/4262139-fe5604c4fe942f55.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


4.用户管理界面


![用户列表页.png](http://upload-images.jianshu.io/upload_images/4262139-6d83bf683aed8798.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


![用户添加页.png](http://upload-images.jianshu.io/upload_images/4262139-7961dd2511246b1c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


![组列表页.png](http://upload-images.jianshu.io/upload_images/4262139-c3ac443c22b08f3c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


![修改权限页.png](http://upload-images.jianshu.io/upload_images/4262139-c57d396549ce61d3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


![组添加页.png](http://upload-images.jianshu.io/upload_images/4262139-bfef9abe9fceb634.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


#### 未完待续
![未完待续.png](http://upload-images.jianshu.io/upload_images/4262139-b6ff1551737a40df.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
