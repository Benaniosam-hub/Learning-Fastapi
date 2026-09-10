from Enemy import *
import random

class ogre(Enemy):
    def __init__(self,health_points,attack_damage):
            super().__init__(type_of_enemy = 'Ogre',
                             health_points = health_points,
                             attack_damage = attack_damage)

    def talk(self):
            print(f'I am {self.get_type_of_enemy()},*Humangasword*')

    def walk_forward(self):
            print(f'{self.get_type_of_enemy()} lets move forward')

    def special(self):
           print(f'I am {self.get_type_of_enemy()} so i smash the enemy')

    def special_attack(self):
           attack_work = random.random() < 0.20
           if attack_work:
                self.attack_damage += 4
                print('Ogre gets angery!')