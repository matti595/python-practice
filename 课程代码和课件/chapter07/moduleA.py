class A:
    def foo(self):
        from moduleB import B
        print("A foo")
        b = B()
        b.bar()

print("moduleA.__name__:", __name__)