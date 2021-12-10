# xlcmdb

### 本人初学python和前端知识，利用Bootstrap + saltstack + paramiko + python 做了一个简单的CMDB平台。

#### 此软件由本人独立完成，本人笔名：君惜(xinlei3166)

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

#### 使用说明
> 使用前请安装好python 2.7和搭建好saltsatck服务器
，安装并运行salt-api可以使用salt界面功能，salt-api接口地址在salt.yaml配置文件中进行修改。

#### 效果图展示：
1.用户界面

![注册.png](https://tva1.sinaimg.cn/large/008i3skNly1gx8seq9tpoj30yg0itt9f.jpg)

![登录.png](https://tva1.sinaimg.cn/large/008i3skNly1gx8sepwhdfj30yg0imgm7.jpg)


![首页.png](https://tva1.sinaimg.cn/large/008i3skNly1gx8seophphj30yg0il40g.jpg)


![个人信息页.png](https://tva1.sinaimg.cn/large/008i3skNly1gx8sem223qj30yg0f03z5.jpg)


![个人信息页-2.png](https://tva1.sinaimg.cn/large/008i3skNly1gx8sekprwtj30yg0ghjrw.jpg)


2.salt界面

![salt-minion列表页.png](https://tva1.sinaimg.cn/large/008i3skNly1gx8seitztdj30yg0ioabq.jpg)


![salt执行命令页.png](https://tva1.sinaimg.cn/large/008i3skNly1gx8sehfaasj30yg0im75i.jpg)


![salt文件分发页.png](https://tva1.sinaimg.cn/large/008i3skNly1gx8sefly9xj30yg0j1q4c.jpg)


![paramiko-webssh页.png](https://tva1.sinaimg.cn/large/008i3skNly1gx8see81mrj30yg0i3402.jpg)



3.主机界面

![主机列表页.png](https://tva1.sinaimg.cn/large/008i3skNly1gx8secwiesj30yg0ipdhj.jpg)


![单台主机详情页.png](https://tva1.sinaimg.cn/large/008i3skNly1gx8sebfdisj30yg0c3mxt.jpg)


![主机修改页.png](https://tva1.sinaimg.cn/large/008i3skNly1gx8se9ztsjj30yg0c8t97.jpg)


4.用户管理界面


![用户列表页.png](https://tva1.sinaimg.cn/large/008i3skNly1gx8se8lna7j30yg0i3jt1.jpg)


![用户添加页.png](https://tva1.sinaimg.cn/large/008i3skNly1gx8se79282j30yg0hz750.jpg)


![组列表页.png](https://tva1.sinaimg.cn/large/008i3skNly1gx8se5ct5ij30yg0iiq3x.jpg)


![修改权限页.png](https://tva1.sinaimg.cn/large/008i3skNly1gx8se23s9bj30yg0h5gmf.jpg)


![组添加页.png](https://tva1.sinaimg.cn/large/008i3skNly1gx8sdy1zb9j30yg0gnq3k.jpg)

