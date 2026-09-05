from Enemy import *
import random

class zombie(Enemy):
    def __init__(self,health_points,attack_damage):
            super().__init__(type_of_enemy = 'Zombie',
                             health_points = health_points,
                             attack_damage = attack_damage)

    def talk(self):
        print(f'I am {self.get_type_of_enemy()}, *Gurrrrrr*')

    def walk_forward(self):
        print(f'{self.get_type_of_enemy()} lets move forward')

    def special(self):
        print(f'I am {self.get_type_of_enemy()} so i spread my power')

    def special_attack(self):
           attack_work = random.random() < 0.50
           if attack_work:
                self.health_points += 2
                print('Zombie regenerated 2HP!')