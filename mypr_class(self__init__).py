class Human1():
    def set_name_like(self, age, like):
        self.age = age
        self.like = like
        
    def info(self):
        print(f"나이:{self.age} 좋아하는것:{self.like}")
        
jang = Human1()
lee = Human1()

jang.set_name_like(15,"apple")
jang.info()

lee.set_name_like(10,"banana")
lee.info()

class Human2():
    def __init__(self, age, like):
        self.age = age
        self.like = like
        
    def info(self):
        print(f"나이:{self.age} 좋아하는것:{self.like}")

dain = Human2(7, "시나모롤")
kim = Human2(7, "축구")

dain.info()
kim.info()