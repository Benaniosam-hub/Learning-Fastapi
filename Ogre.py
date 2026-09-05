from Enemy import *


class ogre(Enemy):
    def __init__(self,health_points,attack_damage):
            self.__type_of_enemy = 'Ogre'
            self.health_points = health_points
            self.attack_damage = attack_damage

    def talk(self):
            print(f'I am {self.__type_of_enemy},*Humangasword*')

    def walk_forward(self):
            print(f'{self.__type_of_enemy} lets move forward')

    def special(self):
           print(f'I am {self.__type_of_enemy} so i smash the enemy')