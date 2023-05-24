class Espresso:
    def __init__(self, bean, shots):
        print("espresso 객체를 생성합니다.")
        self.bean = bean
        self.shots = shots
    
    def print_espresso(self):
        print("에스프레소 정보")
        print("bean", self.bean if self.bean else "지정 안함")
        print("shot", self.shots if self.shots else "지정 안함")
        print("-----------------------")
        
    def print_info(self):
        self.print_espresso()