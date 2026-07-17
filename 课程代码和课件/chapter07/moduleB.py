class B:
    def bar(self):
        from moduleA import A
        print("B bar")
        a = A()
        a.foo()