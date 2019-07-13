# simple_block_chain
一个简单的区块链系统，实现了分布式的区块链信息存储，服务器数据库只保存状态信息供用户选择，而具体数据则是由服务器与客户端交互从客户端获取

*A block_chain system*

resource: https://github.com/kelekle/simple_block_chain

![Screenshot](https://github.com/kelekle/simple_block_chain/blob/master/screenshots/login.png)

![Screenshot](https://github.com/kelekle/simple_block_chain/blob/master/screenshots/view1.png)

![Screenshot](https://github.com/kelekle/simple_block_chain/blob/master/screenshots/view2.png)

![Screenshot](https://github.com/kelekle/simple_block_chain/blob/master/screenshots/view3.png)


## Installation

```
$ git clone https://github.com/kelekle/simple_block_chain.git
$ cd cimple_block_chain
$ install the env for this project
$ python run.py
$ python client.py as a client(of course, you can make a copy for this directory for as many clients as you want)
* Running on http://127.0.0.1:5000/
````

## Introduction

这个仓库目前实现了一个简单的区块链系统
主要采用的是flask框架搭建，使用了Jinja2语法
### 1.数据存储及防篡改
    状态数据以及用户信息保存在服务器数据库(mysql)， 区块链数据则是分布式的存储在各个客户端，客户端启动时会定时(about 1 minute))向服务器发送自身区块数据，服务器接受每个客户端的数据，并进行对比，最高相同数量超过数据库中用户数目的一半，则认为数据合法，发布给各个客户端强制更新。
### 2.数据状态
    三种状态： 新建、处理中、完成。
    数据凡是未加入区块链之前都是保存在自身数据库，为新建状态，可以修改和删除，加入区块链之后，状态更新未处理中，此后将不能修改，直至状态更新为完成，方可以进行下一阶段
### 3.登录
    由于短信验证需要支付费用，故而采用了简单的邮箱验证码验证，提供通过邮箱找回密码功能，以及邮箱注册
### 4.多链
    可以生成多个商品的区块链，以商品的唯一id：pid区别
### 5.提供二维码展示
    对商品的信息有一个简单的二维码结果展示，暂时未对数据清洗处理，展示的是简单的json格式的数据

## Finally
欢迎访问和交流[《simple_block_chain》](https://github.com/kelekle/simple_block_chain)
