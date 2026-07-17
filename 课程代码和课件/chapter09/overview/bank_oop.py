# ========== 面向对象版本：银行账户类 ==========

import datetime

class Account:
    """
    银行账户类
    定义了"银行账户"这种数据类型
    """
    
    __transaction_shared_attrs = set(["time", "type", "amount", "balance"])
    __accounts = {}        # 所有账户都存储在这里
    
    def __new__(cls, *args, **kwargs):
        """
        自定义 __new__ 方法
        用于在实例化对象时进行一些自定义操作

        参数：
        - cls: 类对象本身
        - args, kwargs: 传递给 __init__ 方法的参数
        
        返回：
        - 创建的实例对象
        """
        # 1. 调用父类的 __new__ 方法创建对象
        instance = super().__new__(cls)
        
        # 2. 自定义操作：生成并设置账户号
        account_num = f"{len(cls.__accounts) + 1:03d}"
        instance.account_num = account_num

        # 3. 自定义操作：将新创建的实例添加到私有类字段 __accounts 中
        cls.__accounts[account_num] = instance 

        # 4. 返回创建的对象
        return instance

    def __init__(self, name, initial_deposit=0.0, timestamp=None):
        """
        初始化方法（构造函数）
        当创建 Account 对象时自动调用
        
        参数说明：
        - self: 表示对象自身（重要！）
        - name: 户主姓名
        - initial_deposit: 初始存款金额
        """
        
        # 1. 基本账户信息
        self.name = name                               # 户主姓名
        
        # 2. 余额相关（使用私有属性保护）
        self.__balance = 0.0  # 私有属性，外部不能直接访问
        
        # 3. 交易记录（列表存储）
        self.__transactions = []  # 私有属性，外部不能直接访问
        
        # 验证并设置初始存款
        if initial_deposit < 0:
            raise ValueError("初始存款不能为负数")
        
        self.__balance = initial_deposit
        
        # 记录开户交易
        self.__record_transaction("开户", initial_deposit, timestamp)

        print(f"账户创建成功: {self.name} ({self.account_num})")
    
    # ========== 私有方法==========
    def __record_transaction(self, trans_type, amount, timestamp, **kwargs):
        """
        私有方法：记录交易
        外部不能直接调用，只能在类内部使用
        """
        transaction = {
            'time': timestamp if timestamp else datetime.datetime.now(),
            'type': trans_type,
            'amount': amount,
            'balance': self.__balance
        }
        transaction.update(kwargs)
        self.__transactions.append(transaction)
    
    # ========== 公共方法==========
    def get_balance(self):
        """查询余额"""
        return self.__balance

    def deposit(self, amount, timestamp=None):
        """
        存款方法
        
        参数：
        - amount: 存款金额
        
        返回：
        - 成功返回 True，失败返回 False
        """
        
        # 验证1：金额必须为正数
        if amount <= 0:
            print("错误：存款金额必须大于0")
            return False
        
        # 执行存款
        self.__balance += amount
        
        # 记录交易
        self.__record_transaction("存款", amount, timestamp)
        
        print(f"存款成功！余额: {self.__balance}")
        return True

    def withdraw(self, amount, timestamp=None):
        """
        取款方法
        
        参数：
        - amount: 取款金额
        
        返回：
        - 成功返回 True，失败返回 False
        """
        
        # 验证1：金额必须为正数
        if amount <= 0:
            print("错误：取款金额必须大于0")
            return False
        
        # 验证2：余额必须足够
        if amount > self.__balance:
            print("错误：余额不足")
            return False
        
        # 执行取款
        self.__balance -= amount
        
        # 记录交易
        self.__record_transaction("取款", amount, timestamp)
        
        print(f"取款成功！余额: {self.__balance}")
        return True

    def transfer(self, target_account, amount, timestamp=None):
        """
        转账方法
        
        参数：
        - target_account: 目标账户对象
        - amount: 转账金额
        
        返回：
        - 成功返回 True，失败返回 False
        """
        # 验证1：金额必须为正数
        if amount <= 0:
            print("错误：转账金额必须大于0")
            return False
        
        # 验证2：余额必须足够
        if amount > self.__balance:
            print("错误：余额不足")
            return False
        
        # 执行转账
        self.__balance -= amount
        target_account.__balance += amount
        
        # 记录交易
        self.__record_transaction("转账", -amount, timestamp, target_account=target_account.account_num)
        target_account.__record_transaction("转账", amount, timestamp, source_account=self.account_num)
        
        print(f"转账成功！{self.name} ({self.account_num}) 转账 {amount} 到 {target_account.name} ({target_account.account_num})")
        return True

    def display_transactions(self):
        """
        显示交易记录方法
        打印最近的几笔交易记录
        """
        print(f"{self.name} ({self.account_num}) 的交易记录:")
        for trans in self.__transactions:
            info = f"{trans['time'].strftime('%Y-%m-%d %H:%M:%S')} {trans['type']} {trans['amount']} 余额: {trans['balance']}"
            info += ' ' + ' '.join([f"{k}: {v}" for k, v in trans.items() if k not in self.__transaction_shared_attrs])
            print(info)

    def __repr__(self):
        """
        自定义 __repr__ 方法
        返回对象的字符串表示，用于调试和显示
        """
        return f"Account({self.name}, {self.account_num}, 现金余额：{self.__balance})"

    @classmethod
    def get_accounts(cls):
        """
        类方法：显示所有账户对象
        """
        return cls.__accounts

    @classmethod
    def empty_accounts(cls):
        """
        类方法：清空所有账户对象
        """
        cls.__accounts.clear()
        print("所有账户对象已清空")


class WealthManagementAccount(Account):
    """
    理财金账户类
    继承自Account类，增加了理财产品功能
    """
    
    def __init__(self, name, initial_deposit=0.0, timestamp=None):
        """
        初始化理财金账户
        
        参数说明：
        - name: 户主姓名
        - initial_deposit: 初始存款金额
        """
        # 调用父类的初始化方法
        super().__init__(name, initial_deposit, timestamp)
        
        # 新增理财产品相关属性
        self.__fund_shares = 0.0  # 理财产品份额
        self.__fund_nav = 1.0     # 理财产品最新净值（默认1.0）
    
    def __record_transaction(self, trans_type, amount, timestamp=None, **kwargs):
        """
        重写私有方法：记录交易
        扩展父类方法，增加理财产品相关信息
        """
        transaction = {
            'time': timestamp if timestamp else datetime.datetime.now(),
            'type': trans_type,
            'amount': amount,
            # 子类访问父类私有属性，需要使用 _Account__balance
            'balance': self._Account__balance, 
            'fund_shares': self.__fund_shares,
            'fund_nav': self.__fund_nav,
            'total_value': self.get_total_value()
        }
        transaction.update(kwargs)
        # 子类访问父类私有属性，需要使用 _Account__transactions
        self._Account__transactions.append(transaction)
    
    def get_fund_shares(self):
        """
        查询理财产品份额
        """
        return self.__fund_shares
    
    def get_fund_nav(self):
        """
        查询理财产品最新净值
        """
        return self.__fund_nav
    
    def update_fund_nav(self, new_nav, timestamp=None):
        """
        更新理财产品净值
        
        参数：
        - new_nav: 新的净值
        """
        if new_nav <= 0:
            print("错误：理财产品净值不能为负数")
            return False
        
        old_nav = self.__fund_nav
        self.__fund_nav = new_nav
        
        # 记录净值更新交易
        self.__record_transaction("净值更新", 0, timestamp, old_nav=old_nav, new_nav=new_nav)
        
        print(f"理财产品净值已更新：{old_nav} → {new_nav}")
        return True
    
    def buy_fund(self, amount, timestamp=None):
        """
        购买理财产品
        
        参数：
        - amount: 购买金额
        
        返回：
        - 成功返回 True，失败返回 False
        """
        # 验证1：金额必须为正数
        if amount <= 0:
            print("错误：购买金额必须大于0")
            return False
        
        # 验证2：余额必须足够
        if amount > self._Account__balance:
            print("错误：余额不足")
            return False
        
        # 计算购买的份额（金额 / 当前净值）
        shares = amount / self.__fund_nav
        
        # 执行购买
        self._Account__balance -= amount
        self.__fund_shares += shares
        
        # 记录交易
        self.__record_transaction("购买理财", amount, timestamp, shares=shares)
        
        print(f"购买成功！花费 {amount}，获得 {shares:.4f} 份额，当前净值: {self.__fund_nav}")
        return True
    
    def redeem_fund(self, shares, timestamp=None):
        """
        赎回理财产品
        
        参数：
        - shares: 赎回份额
        
        返回：
        - 成功返回 True，失败返回 False
        """
        # 验证1：份额必须为正数
        if shares <= 0:
            print("错误：赎回份额必须大于0")
            return False
        
        # 验证2：份额必须足够
        if shares > self.__fund_shares:
            print("错误：理财份额不足")
            return False
        
        # 计算赎回金额（份额 * 当前净值）
        amount = shares * self.__fund_nav
        
        # 执行赎回
        self.__fund_shares -= shares
        self._Account__balance += amount
        
        # 记录交易
        self.__record_transaction("赎回理财", amount, timestamp, shares=shares)
        
        print(f"赎回成功！赎回 {shares:.4f} 份额，获得 {amount:.2f}，当前净值: {self.__fund_nav}")
        return True
    
    def get_total_value(self):
        """
        查询账户总价值（现金余额 + 理财产品价值）
        
        返回：
        - 账户总价值
        """
        fund_value = self.__fund_shares * self.__fund_nav
        return self._Account__balance + fund_value
    
    def __repr__(self):
        """
        自定义 __repr__ 方法
        返回对象的字符串表示，包含总价值
        """
        return f"WealthManagementAccount({self.name}, {self.account_num}, 现金余额: {self._Account__balance:.2f}, 理财份额: {self.__fund_shares:.4f}, 理财净值: {self.__fund_nav:.4f}, 总价值: {self.get_total_value():.2f})"
