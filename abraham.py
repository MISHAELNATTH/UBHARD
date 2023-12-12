import pygame
import random
import inventory_button
from menu_button import MButton
import menu_module
import sys
pygame.init()

panel_width = 150
screen_width = 1000
screen_height = 600
red = (255, 0, 0)
yellow = (255, 255, 0)
white = (255, 255, 255)


screen = pygame.display.set_mode((screen_width, screen_height+panel_width))
pygame.display.set_caption("UBHARD")

attacker_no = 1
total_attacker =3
action_cooldown = 0
action_waittime= 90
attack = False
potion = False 
clicked = False
potion_effect = 10
fang_effect = 2
nail_effect = 2
hide_effect = 1
maango_body = 0



font = pygame.font.SysFont('Times New Roman',26)

clock = pygame.time.Clock()
FPS = 60

menu_bg = pygame.image.load("assets/menu_background.jpg")
bg_image = pygame.image.load("assets/fight_location.png").convert_alpha()
panel_img = pygame.image.load("assets/pannel.png").convert_alpha()
sword_img = pygame.image.load("assets/sword.png").convert_alpha()
potion_img = pygame.image.load("assets/potion.png").convert_alpha()
fang_img = pygame.image.load("assets/fang.png").convert_alpha()
nail_img = pygame.image.load("assets/nail.png").convert_alpha()
hide_img = pygame.image.load("assets/potion.png").convert_alpha()
restart_img = pygame.image.load("assets/restart button.png").convert_alpha()

def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))
   
def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)


def display_bg():
  scaled_bg = pygame.transform.scale(bg_image, (screen_width, screen_height))
  screen.blit(scaled_bg,(0,0))

def display_panel():
  scaled_panel = pygame.transform.scale(panel_img,(1180,250 ))
  screen.blit(scaled_panel,(-85, 560))


  
class Fighter():
    
    def __init__(self,x,y,name,max_health,min_dmg, max_dmg, potions,armour,fangs,nails,hides ):
        self.name=name
        self.max_health = max_health
        self.health = max_health
        self.min_dmg = min_dmg
        self.max_dmg = max_dmg
        self.start_armour = armour
        self.armour = armour
        self.start_potions = potions
        self.potions = potions
        self.fangs = fangs
        self.nails = nails
        self.hides = hides
        self.maango_body = 0
        self.alive = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0 #0:idle , 1:attack, 2:hurt, 3:dead
        self.update_time = pygame.time.get_ticks()
     
     #idle action
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'assets/{self.name}/idle{i}.png')
            img = pygame.transform.scale(img,(img.get_width()*2.5,img.get_height()*2.5))
            temp_list.append(img)
        self.animation_list.append(temp_list)

     #attack action
        temp_list = []
        for i in range(5):
            img = pygame.image.load(f'assets/{self.name}_attack/attack{i}.png')
            img = pygame.transform.scale(img,(img.get_width()*2.5,img.get_height()*2.5))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

     #death animation
        temp_list = []
        for i in range(5):
            img = pygame.image.load(f'assets/{self.name}_death/death{i}.png')
            img = pygame.transform.scale(img,(img.get_width()*2.5,img.get_height()*2.5))
            temp_list.append(img)
        self.animation_list.append(temp_list)


    def idle(self):
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def update(self):
        animation_cooldown = 200 
        self.image = self.animation_list[self.action][self.frame_index]   

        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index +=1
        if self.frame_index >=len(self.animation_list[self.action]):
            if self.action == 2:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.idle()
  



    def attack(self,target):
        damage= random.randint(self.min_dmg,self.max_dmg)-self.armour
        target.health -= damage
        
        if target.health <1:
            target.health = 0
        
            target.alive = False
            

            target.death()
        damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), red)
        damage_text_group.add(damage_text)
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def death(self):
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()


    def reset(self):
        self.alive = True
        self.potions = self.start_potions
        self.health = self.max_health
        self.action = 0
        self.update_time =pygame.time.get_ticks()
        self.armour = 0
        self.fangs = 0
        self.nails = 0
        self.hides = 0


    def draw(self):
        screen.blit(self.image,self.rect)

class healthbar():
	def __init__(self, x, y, health, max_health):
		self.x = x
		self.y = y
		self.health = health
		self.max_health = max_health


	def draw(self, health):
		#update with new health
		self.health = health
		#calculate health ratio
		ratio = self.health / self.max_health
		pygame.draw.rect(screen, red, (self.x, self.y, 400, 30))
		pygame.draw.rect(screen, yellow, (self.x, self.y, 400 * ratio, 30))

class DamageText(pygame.sprite.Sprite):

	def __init__(self, x, y, damage, colour):
		pygame.sprite.Sprite.__init__(self)
		self.image = font.render(damage, True, colour)
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.counter = 0


	def update(self):
		#move damage text up
		self.rect.y -= 1
		#delete the text after a few seconds
		self.counter += 1
		if self.counter > 30:
			self.kill()





                    




damage_text_group = pygame.sprite.Group()

  #def draw_health_bar(health, max_health, x, y):
  #  ratio = health / max_health

   # pygame.draw.rect(screen, white, (x - 2, y - 2, 404, 34))
   # pygame.draw.rect(screen, red, (x, y, 400, 30))
   # pygame.draw.rect(screen, yellow, (x, y, 400 * ratio, 30))


peter = Fighter(200,450,'Peter',30,3,6,1,0,0,0,0)
maango_1 = Fighter(700,450,'maango_1',5,1,2,0,0,0,0,0)
maango_2 = Fighter(850,450,'maango_2',5,1,2,0,0,0,0,0)
#maango_3 = Fighter(650,450,'maango',20,6,1)

maango_list = []
maango_list.append(maango_1)
maango_list.append(maango_2)
#maango_list.append(maango_3)

peter_health_bar = healthbar(20, 20, peter.health, peter.max_health)
maango_1_health_bar = healthbar(580, 20, maango_1.health, maango_1.max_health)
maango_2_health_bar = healthbar(580, 50, maango_2.health, maango_2.max_health)



#button
potion_button = inventory_button.Button(screen,100,650,potion_img,70,70) 
fang_button = inventory_button.Button(screen,200 , 650,fang_img,70,70 )
nail_button  = inventory_button.Button(screen,300 , 650,nail_img,70,70 )
hide_button = inventory_button.Button(screen,400 , 650,hide_img,70,70)
restart_button = inventory_button.Button(screen,300 , 120, restart_img,120,30 )

def play():
    attacker_no = 1
    total_attacker =3
    action_cooldown = 0
    action_waittime= 90
    attack = False
    potion = False 
    clicked = False
    potion_effect = 10
    fang_effect = 2
    nail_effect = 2
    hide_effect = 1
    victory = 0

    run = True
    while run:

        clock.tick(FPS)

        display_bg()
        display_panel()
        #Fighter.draw_health_bar(peter.health, 30, 20,20)
        #Fighter.draw_health_bar(maango_1.health,20, 580,20)
        #Fighter.draw_health_bar(maango_2.health, 20, 580,50)
        peter_health_bar.draw(peter.health)
        maango_1_health_bar.draw(maango_1.health)
        maango_2_health_bar.draw(maango_2.health) 

        peter.update()
        peter.draw()
        for maango in maango_list:
            maango.update()
            maango.draw()

        damage_text_group.update()
        damage_text_group.draw(screen)

        

        attack = False
        potion = False
        target = None
        fang = False
        nail = False
        hide =False

        pygame.mouse.set_visible(True)
        pos = pygame.mouse.get_pos()
        for count, maango in enumerate(maango_list):
            if maango.rect.collidepoint(pos):
                pygame.mouse.set_visible(False)
                screen.blit(sword_img, pos)
                if clicked == True and maango.alive == True:
                    attack = True
                    target = maango_list[count]

        if potion_button.draw():
            potion = True

        draw_text(str(peter.potions),font, red, 150, screen_height+25)
        draw_text(str(peter.fangs), font,red,250, screen_height+25)
        draw_text(str(peter.nails), font,red,350, screen_height+25)
        draw_text(str(peter.hides), font,red,450, screen_height+25)

        if fang_button.draw():
            fang =True
        if nail_button.draw():
            nail = True
        if hide_button.draw():
            hide = True


        if victory == 0:
        #player action
            if peter.alive == True:
                if attacker_no == 1:
                    action_cooldown += 1
                    if action_cooldown >= action_waittime:
                        if attack == True and target != None:
                            peter.attack(target)
                            attacker_no +=1
                            action_cooldown = 0
                    
                        if potion == True:
                            if peter.potions > 0:
                                heal_amount = potion_effect + (peter.max_health - peter.health)
                                peter.health += heal_amount
                                peter.potions -=1
                                heal_text = DamageText(peter.rect.centerx, peter.rect.y, str(heal_amount), yellow)
                                damage_text_group.add(heal_text)
                                attacker_no += 1
                                action_cooldown = 0

                        if fang == True:
                            if peter.fangs>0:
                                peter.max_dmg += fang_effect
                                peter.fangs -=1
                                attacker_no+=1
                                action_cooldown = 0

                        if nail == True:
                            if peter.nails>0:
                                peter.min_dmg += nail_effect
                                peter.nails -=1
                                attacker_no +=1
                                action_cooldown = 0
                        if hide ==True:
                            if peter.hides>0:
                                peter.armour +=hide_effect
                                peter.hides -=1
                                attacker_no+=1
                                action_cooldown =0 

            else:
                victory = -1 



                        
                        
                       
                    




            for count, maango in enumerate(maango_list):
                if attacker_no == 2 +count:
                    if maango.alive == True:
                        action_cooldown +=1
                        if action_cooldown>=action_waittime:
                            maango.attack(peter)
                            attacker_no +=1
                            action_cooldown=0
                    else:
                        attacker_no +=1

            if attacker_no > total_attacker:
                attacker_no =1

        alive_maango = 0
        for maango in maango_list:
            if maango.alive == True:
                alive_maango +=1
        if alive_maango == 0:
            victory = 1
        

        
    

        if victory != 0:
            if victory ==1:
                screen.blit(potion_img,(250,50))
            if victory ==-1:
                screen.blit(potion_img,(290,50))
            if restart_button.draw():
                peter.reset()
                for maango in maango_list:
                    maango.resent()
                attacker_no = 1
                action_cooldown = 0
                victory = 0
        


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            else:
                clicked = False
        pygame.display.update()
    pygame.QUIT()
        
def best_scores():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        screen.fill("white")

        OPTIONS_TEXT = get_font(45).render("This is the Best Scores screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = MButton(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()



def credits():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        #Part of speech tagging lo q hace es una tarea que asigna a cada palabra de un texto
        #le asigna una categoria gramatical 
        screen.fill("black")
        credits_bg=pygame.image.load("assets/The Story of Peter Thon.png")
        screen.blit(credits_bg,(0,0))

#blit dibuja una imagen sobre otra, contenido de uno a otra, es un metodo para interactuar 
        PLAY_BACK = MButton(image=None, pos=(580, 620), 
                            text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        pygame.display.update()
    
def main_menu():
    while True:
        screen.blit(menu_bg, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = MButton(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 200), 
                            text_input="New Game", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = MButton(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 350), 
                            text_input="Best Scores", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        CREDITS_BUTTON = MButton(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 500), 
                            text_input="Credits", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = MButton(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 650), 
                            text_input="Quit", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON,CREDITS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    best_scores()
                if CREDITS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    credits()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()


        

        pygame.display.update()
        





main_menu()