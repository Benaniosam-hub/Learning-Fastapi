class Enemy:
    def __init__(self,type_of_enemy,health_points,attack_damage):
        self.__type_of_enemy = type_of_enemy
        self.health_points = health_points
        self.attack_damage = attack_damage
    

    def talk(self):
        print(f'I am {self.__type_of_enemy}')

    def walk_forward(self):
        print(f'{self.__type_of_enemy} lets move forward')

    def attack(self):
        print(f'enimes gonna get {self.attack_damage} damage cause thats our power while we attack them')

    def special_attack(self):
        return f'Enemy has no special attack'

    def get_type_of_enemy(self):
        return self.__type_of_enemy

    