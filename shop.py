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


class Shop:
    # logging.basicConfig(
    #     filename='shop.log',
    #     format='%(asctime)s - %(levelname)s - %(message)s',
    #
    # )

    def __init__(self):
        self.current_name = []
        self.shop_goods_name = goods.books

    # 注册+充值
    def register(self):
        flag = True
        while flag:
            uname = input('请输入用户名:').strip()
            pwd1 = input('请输入密码:').strip()
            pwd2 = input('请再次输入密码:').strip()
            with open('username', 'r', encoding='utf-8') as f:
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
                with open('username', 'a', encoding='utf-8') as f:
                    f.write('%s,%s,%s\n' % (uname, pwd2, balance))
                    flag = False
                    print('注册成功')

    # 登陆
    def login(self):
        flag = True
        # 判断是否已经有账号登陆了
        if len(self.current_name) == 0:
            while flag:
                uname = input('请输入用户名:').strip()
                pwd = input('请输入密码:').strip()
                with open('username', 'r', encoding='utf-8') as f:
                    for line in f:
                        l = line.strip().split(',')
                        if uname == l[0] and pwd == l[1]:
                            print('登陆成功')
                            self.current_name.append(uname)
                            flag = False
                            break
                    else:
                        print('用户名或密码错误')
        else:
            print('当前已有账号登陆')

    # 余额
    def balance(self):
        if self.current_name:
            with open('username', 'r', encoding='utf-8') as f:
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

    # 商品列表
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

                            with open('username', 'r', encoding='utf-8') as fr,\
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

                            os.remove('username')
                            os.rename('new_username', 'username')
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
                    with open('username', 'r', encoding='utf-8') as fr, \
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

                    os.remove('username')
                    os.rename('new_username', 'username')
                    print('充值成功')
                    flag = False

                else:
                    print('您输入的金额数产生了错误')
        else:
            print('请先选择账户进行登陆')

    def main(self):
        while 1:
            s = {
                1: '注册',
                2: '登陆',
                3: '余额',
                4: '查看商品',
                5: '退出当前账户',
                6: '充值',
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
            elif choice == 'q':
                break
            else:
                print('输入错误请重新输入...')


if __name__ == '__main__':
    s = Shop()
    s.main()
