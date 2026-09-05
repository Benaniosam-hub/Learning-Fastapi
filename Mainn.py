from Enemy import *
enemy = Enemy()
enemy.type_of_enemy = 'Zombie'

print(f"{enemy.type_of_enemy} has {enemy.health_points} health points and it deals {enemy.attack_damage} attack damage")

enemy.attack()
enemy.walk_forward()
enemy.talk()