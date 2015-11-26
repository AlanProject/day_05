#-*- coding:utf-8 -*-
#/usr/bin/env python
import os
import json
import hashlib
import fileinput
#密码hash加密模块
def passwd_hash(passwd):
        m = hashlib.md5()
        m.update(passwd)
        return m.hexdigest()
def user_ack(name):
    with open('users','r') as file_read:
        for i in file_read:
            user_info = i.strip().split('|')
            if name == user_info[0]:
                return user_info
        return False
#注册模块
def regist(name,passwd):
    if name and passwd:
        user_tage = False
        #判断user文件是否存在如果存在则追加用户信息
        if os.path.isfile('users'):
            user_info = user_ack(name)
            with open('users','a') as file_write:
                #判断用户是否已经存在
                if user_info:
                    user_tage = True
                if user_tage:
                    print  '用户已存在'
                #如果用户不存在则添加用户并初始化用户金额15000
                else:
                    users ='%s|%s|%d|%d'%(name,passwd_hash(passwd),15000,0)
                    file_write.write(users+'\n')
        #如果不存在users文件则w模式创建文件并写入用户信息
        else:
            with open('users','w') as file_write:
                #初始化用户信息写入文件 用户初始金额为15000
                users ='%s|%s|%d|%d'%(name,passwd_hash(passwd),15000,0)
                file_write.write(users+'\n')
    else:
        print '账户或者密码不能为空'
#登陆模块（基础模块多方调用）
def login(name,passwd):
    user_info = user_ack(name)
    with open('users','r') as file_read:
        if user_info:
            if passwd_hash(passwd) == user_info[1]:
                print '登陆成功'
                return True
            #如果验证失败则登陆失败函数返回False
            else:
                print '登陆失败 密码错误'
                return False
        #用户不存在 输出提示信息
        else:
            print '用户不存在'
#查询
def select():
    pass
#购物（调用登陆模块）
def shoping(name):
    #商品信息
    shoping_list = {'Iphone':5288,'Ipad':3288,'Bike':500,'Coffie':10}
    #存放已购买的商品
    shop_list = {}
    #获取所有商品的名称并赋值给shop_name列表
    shop_name = shoping_list.keys()
    #获取所有商品的价格并赋值给shop_price列表
    shop_price = shoping_list.values()
    #获取用户信息
    user_info = user_ack(name)
    #判断是否存在用户信息如果不存在则表明没有此用户 如果存在则进行下一步操作
    if user_info:
        #根据用户信息列表的下标定位用户的余额（注意这里的余额为str类型）
        print '用户当前余额：%s'%user_info[2]
        #开始购买商品
        while True:
            #通过enumerate函数获取商品名称并对其进行有序排列，id从1开始排列 打印商品信息
            for k,v in  enumerate(shop_name,1):
                print k,'|',v,shoping_list.get(v)
            try:
                #选择商品id进行商品购买
                shoping_tage = int(raw_input('请选择你要购买的商品id：'))
                #判断商品id是否存在
                if shoping_tage in range(len(shop_name)+1):
                    #判断用户的余额是否够购买商品
                    if int(user_info[2]) - shop_price[shoping_tage-1] >0:
                        #进行扣款处理根据下标替换掉用户信息中的余额值
                        user_info[2] = str(int(user_info[2]) - shop_price[shoping_tage-1])
                        #格式化打印已购买商品
                        print ''.ljust(20,'=')
                        print '已经购买%s'%shop_name[shoping_tage-1]
                        if shop_name[shoping_tage-1] in shop_list.keys():
                            shop_list[shop_name[shoping_tage-1]] = [shop_price[shoping_tage-1],shop_list.get(shop_name[shoping_tage-1])[1]+1]
                        else:
                            shop_list[shop_name[shoping_tage-1]] = [shop_price[shoping_tage-1],1]
                        #格式化打印购买之后账户余额
                        print '当前余额%s'%user_info[2]
                        print ''.ljust(20,'=')
                        #退出接口 当用户选择exit退出时可以直接退出程序
                        exit_arg = raw_input('注:退出请输入 exit ,按任意键继续...')
                        if exit_arg == 'exit':
                            break
                    else:
                        #如果余额不足告知用户并退出程序
                        print '余额不足'
                        break
                else:
                    #如果输入的id不存在则进行提示
                    print '请输入正确id值'
            except ValueError:
                #如果输入的id值不是int类型则抛出异常输出友好提示
                print '请输入正确id值'
    user_data = '%s|%s|%s|%s'%(user_info[0],user_info[1],user_info[2],user_info[3])
    for i in fileinput.input('users',inplace=1):
        print i.strip().replace(i,user_data)
    fileinput.close()
    #利用json将账单dump到文件中
    json.dump(shop_list,open('list','w'))
    #输出账单
    print '您购买的商品如下：'
    print ''.ljust(20,'-')
    print '商品 单价 数量'
    for i in shop_list:
        print '%s %d x%d'%(i,shop_list.get(i)[0],shop_list.get(i)[1])
    print ''.ljust(20,'-')
    print '总计：%d'%(15000-int(user_info[2]))
#提现（手续费5%）
def withdraw():
    pass
#还款（10号 过期未还按欠款额5%计息）
#转账
def transfer():
    pass
if __name__ == '__main__':
    #name = raw_input('请输入用户名')
    #passwd = raw_input('请输入密码')
    shoping('Alan')
