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


class Shop:

    def __init__(self):
        self.current_name = []
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
    def balance(self):
        if self.current_name:
            with open('user_info', 'r', encoding='utf-8') as f:
                for line in f:
                    l = line.strip().split(',')
                    if self.current_name[0] == l[0]:
                        print('当前余额为：%s' % l[2])  # <class 'str'>
                        return l[2]
                # print(self.current_name[0])
        else:
            print('请先登录...')

    # 退出当前账户
    def out_of_account(self):
        if self.current_name:
            self.current_name.pop()
            print('成功退出当前帐号')
        else:
            print('当前你还没有进行登录...')
        # print(self.current_name)

    # 商品列表(购买)
    def buy_shop_goods(self):
        flag = True
        if self.current_name:
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
        else:
            print('请先登录...')

    # 充值
    def recharge(self):
        flag = True
        if self.current_name:
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
        else:
            print('请先选择账户进行登陆')

    # 提现(手续费百分之五)
    def withdrawal(self):
        flag = True
        if self.current_name:
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
        else:
            print('请先去登陆')

    # 账户切换
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
    def transfer_accounts(self):
        flag = True
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

    def main(self):
        while 1:
            s = {
                1: '注册',
                2: '登陆',
                3: '余额',
                4: '查看商品',
                5: '退出当前账户',
                6: '充值',
                7: '提现',
                8: '切换登陆',
                9: '转账',

            }
            for i in s:
                print('%s.%s' % (i, s[i]))
            choice = input('请选择序号操作(q退出):').strip()
            if choice == '1':
                self.register()
            elif choice == '2':
                self.login()
            elif choice == '3':
                self.balance()
            elif choice == '4':
                self.buy_shop_goods()
            elif choice == '5':
                self.out_of_account()
            elif choice == '6':
                self.recharge()
            elif choice == '7':
                self.withdrawal()
            elif choice == '8':
                self.account_switch()
            elif choice == '9':
                self.transfer_accounts()
            elif choice == 'q':
                break
            else:
                print('输入错误请重新输入...')


if __name__ == '__main__':
    s = Shop()
    s.main()
