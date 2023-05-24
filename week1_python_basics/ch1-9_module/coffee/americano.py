from .espresso import Espresso


class Americano(Espresso):
    def __init__(self, bean, shots, is_hot, size):
        print("americano 객체를 생성합니다.")
        self.bean = bean
        self.shots = shots
        self.is_hot = is_hot
        self.size = size

    def print_americano(self):
        print("아메리카노 정보")
        print("bean", self.bean)
        print("shots", self.shots)
        print("is_hot", self.is_hot)
        print("size", self.size)
        print("-----------------------")

    def print_info(self):
        self.print_americano()