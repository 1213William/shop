class Shop:

    def __init__(self):
        self.current_name = []

    # 注册+充值
    def register(self):
        flag = True
        while flag:
            uname = input('请输入用户名').strip()
            pwd1 = input('请输入密码').strip()
            pwd2 = input('请再次输入密码').strip()
            if not uname.isalpha():
                print('用户名必须是全英文的')
                continue
            if pwd1 != pwd2:
                print('两次密码输入不一致，请重新输入')
                continue
            if not pwd2.isdigit():
                print('密码必须是全数字的')
                continue
            balance = input('请输入你要充值的金额').strip()
            if not balance.isdigit():
                print('输入的金额必须是数字！！！')
                continue
            with open('username', 'a', encoding='utf-8') as f:
                f.write('%s,%s,%s\n' % (uname, pwd2, balance))
                flag = False

    # 登陆
    def login(self):
        flag = True
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

    # 余额
    def balance(self):
        if self.current_name:
            with open('username', 'r', encoding='utf-8') as f:
                for line in f:
                    l = line.strip().split(',')
                    if self.current_name[0] == l[0]:
                        print('当前余额为：%s' % l[2])
                # print(self.current_name[0])
        else:
            print('请先登录...')

    # 商品列表
    def goods(self):
        print('this is goods')

    def main(self):
        while 1:
            s = {
                1: '注册',
                2: '登陆',
                3: '余额',
                4: '查看商品',
            }
            for i in s:
                print('%s.%s' % (i, s[i]))
            choice = input('请选择序号操作:').strip()
            if choice == '1':
                self.register()
            elif choice == '2':
                self.login()
            elif choice == '3':
                self.balance()
            else:
                print('输入错误请重新输入...')


if __name__ == '__main__':
    s = Shop()
    s.main()
