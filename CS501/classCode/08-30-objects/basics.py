#!/usr/bin/env python3

class Foo:

    def print(self):
        for attr in dir(self):
            if "__" not in attr[:2]:
                print(attr, getattr(self, attr))

    def __str__(self):
        s = "--("
        for attr in dir(self):
            if "__" not in attr[:2]:
                s+= f"{attr}: {getattr(self, attr)}, "
        s = s[:2] + ")--"
        return s

def print_file(f=__file__):
    print(f)

if __name__ == "__main__":
    print(f"Running tests for {__file__}...")
    print_file()

    foo = Foo()
    foo.a = "apple"

    setattr(foo, "b", "banana")

    print(*[item for item in dir(foo) if item[:2] != "__"], sep="\n")

x = getattr(foo, "b")

print(x)

print("------------------------------")
foo.print()

print("------------------------------")
print(f"Here is my ds: {foo}")
