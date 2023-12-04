import random

Peter=[20,3,6,1] #life points, weapon damage min, weapon damage max and armor
mongoose=[10,1,2,0] #life points and weapon damage min, weapon damage max and armor

def fight (Peter,ennemy):
    print("Peter just encountered an enemy act quick !")
    Petes_attack=int(input("tap 1 to give a normal attack !"))
    while Petes_attack!=1 :
        print ("tap 1 only")
        Petes_attack=int(input("tap 1 to give a normal attack !"))
    if Petes_attack==1:
        damage= random.randint(Peter[1],Peter[2])-ennemy[3]
        while damage<= ennemy[0]:
            print("the ennemy took the damage but survived !")
            Peter[0]= random.randint(ennemy[1],ennemy[2])-Peter[3]
            petes_attack=int(input("you need to react ! tap 1 to give a normal attack!"))
            damage= damage+random.randint(Peter[1],Peter[2])-ennemy[3]
            if damage >=ennemy[0]:
                 print("you just stroke down this ennemy !")
                 break
        if damage>=ennemy[0]:
            print("you just took down this ennemy !!")
   
        
        



fight(Peter,mongoose)
