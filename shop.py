import goods
import os
import logging

file_handler = logging.FileHandler('shop.log', 'a', encoding='utf-8')
file_handler.setFormatter(logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(message)s'))
logger1 = logging.Logger('A', level=40)
logger1.addHandler(file_handler)

file_handler2 = logging.FileHandler('recharge.log', 'a', encoding='utf-8')
file_handler2.setFormatter(logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(message)s'))
logger2 = logging.Logger('B', level=40)
logger2.addHandler(file_handler2)

file_handler3 = logging.FileHandler('tixian.log', 'a', encoding='utf-8')
file_handler3.setFormatter(logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(message)s'))
logger3 = logging.Logger('C', level=40)
logger3.addHandler(file_handler3)


# 用户登录的装饰器
class Wrapper:

    def __init__(self, current_name):
        self.current_name = current_name

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            flag = True
            if self.current_name:
                func(*args, **kwargs)
            else:
                while flag:
                    print('当前还没有登陆,请先去登陆...')
                    user_name = input('请输入用户名:').strip()
                    pwd = input('请输入密码:').strip()
                    with open('user_info', 'r', encoding='utf-8') as f:
                        for line in f:
                            li = line.strip().split(',')
                            if user_name == li[0] and pwd == li[1]:
                                print('登陆成功')
                                self.current_name.append(user_name)
                                flag = False
                                break
        return wrapper


class Shop:
    current_name = []

    def __init__(self):
        # self.current_name = []
        self.shop_goods_name = goods.books

    def register(self):
        flag = True
        while flag:
            uname = input('请输入用户名:').strip()
            pwd1 = input('请输入密码:').strip()
            pwd2 = input('请再次输入密码:').strip()
            # 判断当前路径是否存在
            if os.path.isfile('./user_info'):
                with open('user_info', 'r', encoding='utf-8') as f:
                    for line in f:
                        l = line.strip().split(',')
                        if uname == l[0]:
                            print('用户名已存在，请重新输入。')
                            flag = False
            if not uname.isalpha():
                print('用户名必须是全英文的')
                continue
            if pwd1 != pwd2:
                print('两次密码输入不一致，请重新输入')
                continue
            if not pwd2.isdigit():
                print('密码必须是全数字的')
                continue
            while flag:
                balance = input('请输入你要充值的金额:').strip()
                if not balance.isdigit():
                    print('输入的金额必须是数字！！！')
                    continue
                with open('user_info', 'a', encoding='utf-8') as f:
                    f.write('%s,%s,%s\n' % (uname, pwd2, balance,))
                    print('注册成功')
                    flag = False

    # 登陆
    def login(self):
        flag = True
        while flag:
            uname = input('请输入用户名:').strip()
            pwd = input('请输入密码:').strip()
            with open('user_info', 'r', encoding='utf-8') as f:
                for line in f:
                    l = line.strip().split(',')
                    if uname == l[0] and pwd == l[1]:
                        print('登陆成功')

                        self.current_name.append(uname)
                        # self.user_card()
                        flag = False
                        break
                else:
                    print('用户名或密码错误')

    # 余额
    @Wrapper(current_name=current_name)
    def balance(self):
        with open('user_info', 'r', encoding='utf-8') as f:
            for line in f:
                l = line.strip().split(',')
                if self.current_name[0] == l[0]:
                    print('当前余额为：%s' % l[2])  # <class 'str'>
                    return l[2]
            # print(self.current_name[0])

    # 退出当前账户
    @Wrapper(current_name=current_name)
    def out_of_account(self):
            self.current_name.pop()
            print('成功退出当前帐号')

    # 商品列表(购买)
    @Wrapper(current_name=current_name)
    def buy_shop_goods(self):
        flag = True

        for i in self.shop_goods_name:
            print('书名: <%s>' % (i['name']))
        # print(self.shop_goods_name)
        while flag:
            b_name = input('输入书名查看详情(按q退至主页面):').strip()
            for i in self.shop_goods_name:
                if b_name == i['name']:
                    print(i)
                    print('是否进行购买:y/n')
                    choice = input('>>').strip()
                    if choice == 'n':
                        break
                    elif choice == 'y':

                        with open('user_info', 'r', encoding='utf-8') as fr,\
                            open('new_username', 'w', encoding='utf-8') as fw:

                            for line in fr:
                                l = line.strip().split(',')
                                if self.current_name[0] == l[0]:
                                    # 进行一次判断，账户中的余额是否能够支持这次购买
                                    if float(l[2]) >= float(i['price']):
                                        new_balance = float(l[2]) - float(i['price'])
                                        l[2] = round(new_balance, 1)
                                        print('购买成功')
                                        logger1.error('用户名为<%s>的用户购买了<%s>,当前余额还剩<%s>' % (l[0], i['name'], l[2]))
                                        # print(i['name'])
                                        # 插入日志操作
                                    else:
                                        print('当前账户余额应不支持你这次的购买了....')
                                l = [str(i) for i in l]
                                l = ','.join(l)
                                fw.write(l+'\n')

                        os.remove('user_info')
                        os.rename('new_username', 'user_info')
                        break
                    # elif b_name == 'q':
                    #     flag = False
                    else:
                        print('请理性输入')
                elif b_name == "q":
                    flag = False
                    break
            else:
                print('请输入正确的书名...')

    # 充值
    @Wrapper(current_name=current_name)
    def recharge(self):
        flag = True

        while flag:
            price = input('请输入你想充值的金额:').strip()
            if price.isdigit() or float(price) > 0:
                with open('user_info', 'r', encoding='utf-8') as fr, \
                    open('new_username', 'w', encoding='utf-8') as fw:
                    for line in fr:
                        l = line.strip().split(',')
                        if self.current_name[0] == l[0]:
                            l[2] = float(l[2]) + float(price)
                            logger2.error('用户名为<%s>的用户充值了<%s>,当前余额为<%s>' % (l[0], price, l[2]))
                        l = [str(i) for i in l]
                        l = ','.join(l)
                        fw.write(l+'\n')
                        # logger2.error('用户名为<%s>的用户充值了<%s>,当前余额为<%s>' % (l[0], price, l[2]))

                os.remove('user_info')
                os.rename('new_username', 'user_info')
                print('充值成功')
                flag = False

            else:
                print('您输入的金额数产生了错误')

    # 提现(手续费百分之五)
    @Wrapper(current_name=current_name)
    def withdrawal(self):
        flag = True

        while flag:
            t_money = input('请输入你要提现的金额:').strip()
            if not t_money.isdigit():
                print('请理性输入')
                continue
            with open('user_info', 'r', encoding='utf-8') as fr, \
                    open('new_username', 'w', encoding='utf-8') as fw:
                for line in fr:
                    l = line.strip().split(',')
                    # 定位到用户那一行
                    if self.current_name[0] == l[0]:
                        # 对账户内的金额进行一次判断，是否大于要提现的金额
                        if (float(t_money) + float(t_money) * 0.05) > float(l[2]):
                            print('超出当前账户内的金额')

                        else:
                            # print(float(l[2]) + float(t_money) * 0.05)
                            l[2] = round(float(l[2]) - (float(t_money) + float(t_money) * 0.05))
                            logger3.error('<%s>体现了<%s>元，当前账户余额为<%s>' % (l[0], t_money, l[2]))
                            print('提现成功')
                            # print(round(l[2], 2), type(l[2]))
                    l = [str(i) for i in l]
                    l = ','.join(l)
                    fw.write(l + '\n')
            os.remove('user_info')
            os.rename('new_username', 'user_info')

            flag = False
                # print(l)

    # 账户切换
    @Wrapper(current_name=current_name)
    def account_switch(self):
        if len(self.current_name):
            flag = True
            while flag:
                print('当前账户为:%s   可切换账户:%s' % (self.current_name[0], self.current_name[1:]))
                choice = input('切换账户名>>:').strip()
                if choice not in self.current_name[1:]:
                    print('请输入正确的账户名...')
                    continue
                else:
                    self.current_name.remove(choice)
                    self.current_name.insert(0, choice)
                    print('账户切换成功')
                    flag = False
        else:
            print('请先去登陆...')

    # 转账
    @Wrapper(current_name=current_name)
    def transfer_accounts(self):
        flag = True
        if len(self.current_name) > 1:
            while flag:
                print('请选择要转账的用户(q退出):', self.current_name[1:])
                # choice == 'egon'
                choice = input('请输入要转账用户>>:').strip()
                money = float(input('请输入转账金额>>:').strip())
                if choice not in self.current_name[1:]:
                    print('请输入正确的账户名...')
                    continue
                elif choice == self.current_name[0]:
                    print('当前暂不支持给自己转账')
                    continue
                elif choice == 'q':
                    break
                else:

                    with open('user_info', 'r', encoding='utf-8') as fr, \
                            open('new_username', 'w', encoding='utf-8') as fw:
                        for line in fr:
                            l = line.strip().split(',')
                            if self.current_name[0] == l[0]:
                                if money > float(l[2]):
                                    print('当前金额暂不支持本次转账')
                                    flag = False
                                    break
                                else:
                                    l[2] = float(l[2]) - money
                                    print('转账成功')
                            l = [str(i) for i in l]
                            l = ','.join(l)
                            fw.write(l + '\n')

                        os.remove('user_info')
                        os.rename('new_username', 'user_info')

                    with open('user_info', 'r', encoding='utf-8') as file_read, \
                            open('new_username', 'w', encoding='utf-8') as file_write:
                        for lin in file_read:
                            new_l = lin.strip().split(',')
                            if choice == new_l[0]:
                                new_l[2] = float(new_l[2]) + money
                            new_l = [str(i) for i in new_l]
                            new_l = ','.join(new_l)
                            file_write.write(new_l + '\n')
                        os.remove('user_info')
                        os.rename('new_username', 'user_info')
                        flag = False
        else:
            print('当前只有一个账户，无法进行在线转账')

    def main(self):
        while 1:
            s1 = {
                1: '管理用户',
                2: '购物',
            }
            for i in s1:
                print('%s.%s' % (i, s1[i]))
            cho1 = input('请选择序号操作(q退出):').strip()
            if cho1 == '1':
                s3 = {
                    1: '添加账户',
                    2: '切换账户',
                    3: '账户提现',
                    4: '账户转账',
                    5: '查询余额',
                    6: '退出当前账户',
                    7: '账户充值',
                    8: '账户注册'
                }
                for x in s3:
                    print('%s.%s' % (x, s3[x]))
                while 1:

                    cho2 = input('请选择序号操作(q退出):').strip()
                    if cho2 == '1':
                        self.login()
                    elif cho2 == '2':
                        self.account_switch()
                    elif cho2 == '3':
                        self.withdrawal()
                    elif cho2 == '4':
                        self.transfer_accounts()
                    elif cho2 == '5':
                        self.balance()
                    elif cho2 == '6':
                        self.out_of_account()
                    elif cho2 == '7':
                        self.recharge()
                    elif cho2 == '8':
                        self.register()
                    elif cho2 == 'q':
                        print('------退出成功------')
                        break
                    else:
                        print('输入错误请重新输入...')
            elif cho1 == '2':
                s4 = {
                        1: '查询并购买商品'
                    }
                for y in s4:
                    print('%s.%s' % (y, s4[y]))
                while 1:
                    cho3 = input('请选择序号操作(q退出):').strip()
                    if cho3 == '1':
                        self.buy_shop_goods()
                    elif cho3 == 'q':
                        print('------退出成功------')
                        break

            elif cho1 == 'q':
                print('------退出成功------')
                break


if __name__ == '__main__':
    s = Shop()
    s.main()
