def say_hello(name):
    return f"Hello {name}!"
def say_goodbye(name):
    return f"Goodbye {name}!"
# 顶层代码
print("Greetings module is loaded.")

# 可执行语句
if __name__ == "__main__":
    # 测试模块功能
    print(say_hello("Alice"))
    print(say_goodbye("Bob"))
