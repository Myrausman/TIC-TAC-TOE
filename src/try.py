import sys
import pygame
import numpy as np
import random
from pygame import mixer



red = (255, 106, 106)
cyan = (0, 238, 238)
white = (255, 255, 255)
black = (0, 0, 0)
a = (183, 135, 192)
gray = (83, 31, 102)
ROWS = 3
COLS = 3
width = 600
height = 600
l_height = height // 5  # 120
line_width = 7
radius = l_height // 4  # 30
circ_width = 10


pygame.init()
pygame.font.init()



#Button and Heading class
class button:
    
    #Button func
    def button(self, main_screen, color, x, y, rec_width, rec_height, font, size, msg, font_color, blit_x, blit_y):
        pygame.draw.rect(main_screen, color, [x, y, rec_width, rec_height])
        font1 = pygame.font.SysFont(font, size)
        fontc = font1.render(msg, True, font_color)
        main_screen.blit(fontc, (blit_x, blit_y))
    
    #Heading Func
    def heading (self,main_screen, font, size, msg, msg_color, y):
        font = pygame.font.SysFont(font, size)
        font1 = font.render(msg, True, msg_color)
        text_rect = font1.get_rect(center=(width / 2, y))

        main_screen.blit(font1, text_rect)


#Main Board Single and Multiplayer functions 
class Board(button):
    def __init__(self, gd):
        self.gd = gd
        global squares
        self.squares = np.zeros((ROWS, COLS))
        self.empty_sqrs = self.squares  # [squares]
        self.marked_sqrs = 0
    
    
    
    #Combine all  empty squares  row col
    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(3):
            for col in range(3):
                if self.empty_sqr(row, col):
                    empty_sqrs.append((row, col))
        return empty_sqrs
    
    
    #Winner popup
    def winner(self, row, col):
        if self.squares[row][col] == 1:
            self.button(self.gd, black, 90, 250, 400, 100, 'cambriacambriamath', 60, 'PLAYER 1 WINNER ', red, 110, 280)

        elif self.squares[row][col] == 2:
            self.button(self.gd, black, 90, 250, 400, 100, 'cambriacambriamath', 60, 'PLAYER 2 WINNER ', cyan, 110, 280)
    
    #Check winner
    def final_state(self):
        # vertical wins
        for col in range(3):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                color = cyan if self.squares[0][col] == 2 else red
                iPos = (col * 100 + 190, 160)
                fPos = (col * 100 + 190, 440)
                pygame.draw.line(self.gd, color, iPos, fPos, line_width)
                self.winner(0, col)
                return self.squares[0][col]
        # horizontal wins
        for row in range(3):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                color = cyan if self.squares[row][0] == 2 else red
                iPos = (150, row * 100 + 200)
                fPos = (430, row * 100 + 200)
                pygame.draw.line(self.gd, color, iPos, fPos, line_width)
                self.winner(row, 0)
                return int(self.squares[row][0])
        # diagonal win
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            color = cyan if self.squares[1][1] == 2 else red
            iPos = (160, 170)
            fPos = (600 - 180, 600 - 170)
            pygame.draw.line(self.gd, color, iPos, fPos, line_width)
            self.winner(1, 1)
            return self.squares[1][1]
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            color = cyan if self.squares[1][1] == 2 else red
            iPos = (600 - 170, 160)
            fPos = (150, 600 - 160)
            pygame.draw.line(self.gd, color, iPos, fPos, line_width)
            self.winner(1, 1)
            return self.squares[1][1]
        return 0

    #Mark square on board
    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1
    
    #Check empty sqaures on baord
    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0
    
    # Check boardfull or not
    def isfull(self):
        return self.marked_sqrs == 9

   
   # Draw or not
    def check_draw(self):
        if self.isfull():
            self.button(self.gd, black, 90, 250, 400, 100, 'cambriacambriamath', 60, 'GAME DRAW ', white, 150, 280)
            
   # Computer input function
    def rand(self):
        b = self.get_empty_sqrs()
        if len(b) != 0:
            c = random.choice(b)
            d = list(c)
            rows = d[0]
            cols = d[1]


            self.squares[rows][cols] = 2
            center = ((cols + 1) * 100 // 2 + 142 + cols * 50, (rows + 1) * 100 // 2 + 150 + rows * 50)
            pygame.draw.circle(gd, cyan, center, radius, circ_width)


# Main board functions and logics
class Game:
    def __init__(self, player=1):
        global gd
        # global squares
        # self.squares=np.zeros((3,3))
        gd = pygame.display.set_mode((width, height))
        pygame.display.set_caption("TIC TAC TOE")
        gd.fill(black)
        window3 = pygame.image.load("bg2.jpeg")
        gd.blit(window3, (0, 0))
        back = pygame.image.load("back.jpeg")
        gd.blit(back, (15, 15))
        
        self.board = Board(gd)
        self.player = player  # 1 cross     #2-circle
        self.running = True
        self.bot = single_player()
        self.show_lines()
    
        
    # Show figures on board
    def show_lines(self):

        pygame.draw.line(gd, white, (140 + 100, 153), (140 + 100, 147 + 300), line_width)

        pygame.draw.line(gd, white, (140 + 200, 153), (140 + 200, 147 + 300), line_width)

        # horizontals
        pygame.draw.line(gd, white, (145, 250), (135 + 300, 250), line_width)
        pygame.draw.line(gd, white, (145, 350), (135 + 300, 350), line_width)
        
        # a=pygame.draw.line(gd,red,(160,180),(220,220),10)
        # b=pygame.draw.line(gd,red,(220,180),(160,220),10)
        
        
        pygame.draw.line(gd,red,(150,60),(210,100),10)
        pygame.draw.line(gd,red,(210,60),(150,100),10)
        center=(400,80)
        pygame.draw.circle(gd,cyan,center,radius,circ_width)
    
    # Draw figures on board after mark
    def draw_fig(self, row, col):
        if self.player == 1:
            center=(400,80)
            pygame.draw.circle(gd,cyan,center,radius,circ_width)
            pygame.draw.line(gd, red, (col * 100 + 160, row * 100 + 180), (col * 100 + 120 + 100, row * 100 + 220), 10)
            pygame.draw.line(gd, red, (col * 100 + 120 + 100, row * 100 + 180), (col * 100 + 160, row * 100 + 220), 10)
            pygame.draw.line(gd,gray,(150,60),(210,100),10)
            pygame.draw.line(gd,gray,(210,60),(150,100),10)
            
            
            
        elif self.player == 2:
            pygame.draw.line(gd,red,(150,60),(210,100),10)
            pygame.draw.line(gd,red,(210,60),(150,100),10)
            center = ((col + 1) * 100 // 2 + 142 + col * 50, (row + 1) * 100 // 2 + 150 + row * 50)
            pygame.draw.circle(gd, cyan, center, radius, circ_width)
            center=(400,80)
            pygame.draw.circle(gd,gray,center,radius,circ_width)
   
    # This function combination of all functions
    def make_move(self, row, col):
        
        self.board.mark_sqr(row, col, self.player)
        self.draw_fig(row, col)
        
        self.next_turn()
        self.board.check_draw()
        

    # Player turn
    def next_turn(self):
        
        self.player = self.player % 2 + 1
    
    # Is game over or not?
      
    def isover(self):
        return self.board.final_state() or self.board.isfull()
    
    
# Main Menuscreen (1st Screen)
class mainmenu():


    def __init__(self):
        
        manu_sound = mixer.Sound('music.wav')
        pygame.mixer.stop()
        manu_sound.play(1)
        manu_sound.set_volume(0.5)
        obj = button()
        pygame.display.set_caption("TIC TAC TOE")
        global main_screen
        main_screen = pygame.display.set_mode((width, height))

        c = pygame.image.load("bg.jpeg")
        main_screen.blit(c, (0, 0))
        obj.button(main_screen, gray, 200, 300, 200, 55,
                   'cambriacambriamath', 70, 'PLAY', white, 240, 306)
        # obj.button(main_screen, gray, 176, 390, 240, 55,'cambriacambriamath', 70, 'OPTIONS', white, 185, 396)
        obj.button(main_screen, gray, 200, 400, 200, 55,
                   'cambriacambriamath', 70, 'EXIT', white, 240, 400)
        obj.heading(main_screen,'javanesetext', 80, 'TIC TAC TOE', white, 130)
        obj.heading(main_screen,'comicsansms', 60, 'Main Menu', white, 200)



        game = True
        while (game == True):

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            if 200 < mouse[0] < 200 + 200 and 300 < mouse[1] < 355:
                obj.button(main_screen, a, 200, 300, 200, 55, 'cambriacambriamath', 70, 'PLAY', white, 240, 306)

                if event.type == pygame.MOUSEBUTTONDOWN:

                    #PLAYSOUND
                    play_sound = mixer.Sound('click.wav')
                    play_sound.play()
                    ob = choose_player()
                    ob.main1()
                    game = False


            else:
                obj.button(main_screen, gray, 200, 300, 200, 55, 'cambriacambriamath', 70, 'PLAY', white, 240, 306)

            if 200 < mouse[0] < 200 + 200 and 400 < mouse[1] < 455:
                obj.button(main_screen, a, 200, 400, 200, 55, 'cambriacambriamath', 70, 'EXIT', white, 240, 406)
                if event.type == pygame.MOUSEBUTTONDOWN:

                    # EXITSOUND
                    exit_sound = mixer.Sound('click.wav')
                    exit_sound.play()
                    ob1 = exit_screen()
                    ob1.main2()
                    game = False
            else:
                obj.button(main_screen, gray, 200, 400, 200, 55, 'cambriacambriamath', 70, 'EXIT', white, 240, 406)

            pygame.display.update()
  
#secondscreeen
class choose_player:
    def __init__(self):
        manu_sound = mixer.Sound('music.wav')
        pygame.mixer.stop()
        manu_sound.play(1)
        manu_sound.set_volume(0.5)
        window2 = pygame.display.set_mode((600, 600))
        window2.fill(black)

        pygame.display.set_caption('TIC TAC TOE ')
        bg = pygame.image.load("bg1.jpeg")
        single = pygame.image.load("single.jpeg")
        multiplayer = pygame.image.load("multiplayer.jpeg")
        back = pygame.image.load("back.jpeg")

        window2.blit(bg, (0, 0))
        window2.blit(single, (170, 300))
        window2.blit(multiplayer, (170, 380))
        window2.blit(back, (15, 15))
        font = pygame.font.SysFont('comicsansms', 60)
        text = font.render('TIC - TAC - TOE ', True, white, None)
        textRect = text.get_rect()
        textRect.center = (width // 2, 150)
        window2.blit(text, textRect)
        

    def main1(self):
        game = True
        while (game == True):

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                   
                    game = False
                mouse1 = pygame.mouse.get_pos()

                if 173 < mouse1[0] < 415 and 303 < mouse1[1] < 300 + 52:

                    if event.type == pygame.MOUSEBUTTONDOWN:

                        #SOUND
                        gameclick = mixer.Sound('click.wav')
                        gameclick.play()

                        
                        obj = single_player()
                        obj.main()

                        game = False

                if 173 < mouse1[0] < 415 and 382 < mouse1[1] < 423:

                    if event.type == pygame.MOUSEBUTTONDOWN:

                        #SOUND
                        gameclick = mixer.Sound('click.wav')
                        gameclick.play()

                        ob = multiplayer()
                        ob.main()

                        game = False
                if 13 < mouse1[0] < 80 and 13 < mouse1[1] < 80:
                            # X&0 sound
                        
                        if event.type==pygame.MOUSEBUTTONDOWN:
                            gameclick = mixer.Sound('click.wav')
                            gameclick.play()
                            
                            obj=mainmenu()
                            
                             
                            game=False
            pygame.display.update()



        
#Single player mode
class single_player():
    def __init__(self):
        self.player = 1

    def draw_figure(self, row, col):
        if self.player == 1:
            pygame.draw.line(gd, red, (col * 100 + 160, row * 100 + 180), (col * 100 + 120 + 100, row * 100 + 220), 10)
            pygame.draw.line(gd, red, (col * 100 + 120 + 100, row * 100 + 180), (col * 100 + 160, row * 100 + 220), 10)
        
 

    def main(self):
        game = Game()
        board = game.board
        over = True
        start=pygame.time.get_ticks()
        while (over == True):
            start1=pygame.time.get_ticks()
            seconds=(start1-start)/1000
            if seconds<=10:
                board.button(gd, black, 230, 80, 120, 30, 'cambriacambriamath', 40, str(int(seconds)), white, 280, 80)
           
                
            if seconds<=10 and game.isover() and board.final_state()==1:
                board.button(gd, black, 230, 80, 120, 30, 'cambriacambriamath', 40, "You won", white, 230, 80)
            if seconds<=10 and game.isover() and board.final_state()==2:
                board.button(gd, black, 220, 80, 140, 30, 'cambriacambriamath', 40, "comp won", white, 220, 80)

            if len(board.get_empty_sqrs() )==0 and board.final_state()==0 and seconds<=10:
                board.button(gd, black, 230, 80, 120, 40, 'cambriacambriamath', 40, "Draw!", white, 250, 85)
                
            
                
            if seconds>=10 and  not game.isover() and len(board.get_empty_sqrs())!=0:
                board.button(gd, black, 90, 250, 400, 100, 'cambriacambriamath', 60, 'TIME OVER ', white, 150, 280)
                window4=pygame.image.load('home.jpeg')
                gd.blit(window4,(140,510))
                window5=pygame.image.load('restart.jpeg')
                gd.blit(window5,(300,510))  
                
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    mouse1 = pygame.mouse.get_pos()
                    if 150<pos[0]< 450 and 150<pos[1]<450:
                        # X&0 sound
                        gameclick = mixer.Sound('click.wav')
                        gameclick.play()
                        
                        
                        if 150 < pos[0] < 250:
                            col = 0
                        elif 250 < pos[0] < 350:
                            col = 1
                        elif 350 < pos[0] < 450:
                            col = 2
                        if 150 < pos[1] < 250:
                            row = 0
                        elif 250 < pos[1] < 350:
                            row = 1
                        elif 350 < pos[1] < 450:
                            row = 2

                        

                        # singleplayer
                        if seconds<=10 and not game.isover():
                            if board.empty_sqr(row, col):
                               board.mark_sqr(row, col, self.player)
                               self.draw_figure(row, col)
                               board.rand()
                            
                        
                            if game.isover() and seconds<=10:
                                board.button(gd, black, 230, 80, 120, 30, 'cambriacambriamath', 40, "You won", white, 230, 80)
                                

                                window4=pygame.image.load('home.jpeg')
                                gd.blit(window4,(140,510))
                                window5=pygame.image.load('restart.jpeg')
                                gd.blit(window5,(300,510))
                            elif seconds>10 and  not game.isover():
                                board.button(gd, black, 90, 250, 400, 100, 'cambriacambriamath', 60, 'TIME OVER ', white, 150, 280)
                                window4=pygame.image.load('home.jpeg')
                                gd.blit(window4,(140,510))
                                window5=pygame.image.load('restart.jpeg')
                                gd.blit(window5,(300,510)) 
                            elif len(board.get_empty_sqrs() )==0 and board.final_state()==0 and seconds<=10:
                                board.button(gd, black, 90, 250, 400, 100, 'cambriacambriamath', 60, 'GAME DRAW ', white, 150, 280)
                                board.button(gd, black, 230, 80, 120, 40, 'cambriacambriamath', 40, "Draw!", white, 250, 85)
                                window4=pygame.image.load('home.jpeg')
                                gd.blit(window4,(140,510))
                                window5=pygame.image.load('restart.jpeg')
                                gd.blit(window5,(300,510))
                               
                    mouse=pygame.mouse.get_pos()           
                    if 140 < mouse[0] < 287 and 513 < mouse[1] < 542:
                        if event.type==pygame.MOUSEBUTTONDOWN:
                                    
                            obj=mainmenu()
                            over=False
                            
                            
                            
                    mouse2=pygame.mouse.get_pos()
                    if 300 < mouse2[0] < 466 and 513 < mouse2[1] < 542:
                        if event.type==pygame.MOUSEBUTTONDOWN:
                            obj=single_player()
                            obj.main()
                            over=False
                               
                        
                                    
                            

                    if 13 < mouse1[0] < 80 and 13 < mouse1[1] < 80:
                            # X&0 sound
                        gameclick = mixer.Sound('click.wav')
                        gameclick.play()
                        if event.type==pygame.MOUSEBUTTONDOWN:
                            
                            obj=choose_player()
                            obj.main1()
                             
                            over=False

            pygame.display.update()


#Multiplayer screen
class multiplayer:   


    #Multiplayer
    def main(self):
        game = Game()
        board = game.board
        start=pygame.time.get_ticks()
        over = True
      
        while (over == True):
            
            mouse=pygame.mouse.get_pos()
            start1=pygame.time.get_ticks()
            seconds=(start1-start)/1000
            if seconds<=10:
                board.button(gd, black, 230, 80, 120, 30, 'cambriacambriamath', 40, str(int(seconds)), white, 280, 80)
                
            if seconds<=10 and game.isover():
                board.button(gd, black, 230, 80, 120, 30, 'cambriacambriamath', 40, "You won", white, 230, 80)
                
            if seconds<=10 and board.final_state()==0 and board.isfull():
                board.button(gd, black, 230, 80, 120, 40, 'cambriacambriamath', 40, "Draw!", white, 250, 80)

            if seconds>10 and  not game.isover():
                board.button(gd, black, 90, 250, 400, 100, 'cambriacambriamath', 60, 'TIME OVER ', white, 150, 280)
                window4=pygame.image.load('home.jpeg')
                gd.blit(window4,(140,510))
                window5=pygame.image.load('restart.jpeg')
                gd.blit(window5,(300,510))
                

               

            #Multiplayer
            for event in pygame.event.get():
            
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                

                if event.type == pygame.MOUSEBUTTONDOWN and seconds<=10:
                    seconds=0
                    pos = event.pos                                      
                    if 150<pos[0]< 450 and 150<pos[1]<450:
                        # X&0 sound
                        gameclick = mixer.Sound('click.wav')
                        gameclick.play()
                        if 150 < pos[0] < 250:
                            col = 0
                        elif 250 < pos[0] < 350:
                            col = 1
                        elif 350 < pos[0] < 450:
                            col = 2
                        if 150 < pos[1] < 250:
                            row = 0
                        elif 250 < pos[1] < 350:
                            row = 1
                        elif 350 < pos[1] < 450:
                            row = 2
                        
                        #Multiplayer
                        if board.empty_sqr(row, col) :
                            if seconds<=10 and not game.isover():
                                game.make_move(row, col)
                            

                            if game.isover():
                                
                                window4=pygame.image.load('home.jpeg')
                                gd.blit(window4,(140,510))
                                window5=pygame.image.load('restart.jpeg')
                                gd.blit(window5,(300,510))    
                
                                
                if 140 < mouse[0] < 287 and 513 < mouse[1] < 542:
                    if event.type==pygame.MOUSEBUTTONDOWN:   
                        
                        obj5=mainmenu()
                        over=False
                        
                        
                
                if 300 < mouse[0] < 466 and 513 < mouse[1] < 542:
                    if event.type==pygame.MOUSEBUTTONDOWN:
                        
                        start=start1       
                        ob=multiplayer()
                    
                        ob.main()
                        game=False
                if 13 < mouse[0] < 80 and 13 < mouse[1] < 80:
                            # X&0 sound
                        gameclick = mixer.Sound('click.wav')
                        
                        if event.type==pygame.MOUSEBUTTONDOWN:
                            gameclick.play()
                            
                            obj=choose_player()
                            obj.main1()
                            
                            game=False    
           
            
            pygame.display.update()
          



# exitscreen
class exit_screen(button):

    def __init__(self):
        manu_sound = mixer.Sound('music.mp3')
        pygame.mixer.stop()
        manu_sound.play(1)
        manu_sound.set_volume(0.5)
        w = pygame.display.set_mode((600, 600))
        w.fill(black)
        pygame.display.set_caption('TIC TAC TOE ')
        c = pygame.image.load('screenshotbg.jpeg')
        w.blit(c, (0, 0))
        self.screen =w
        points = [(180),(265),(240),(230)]
        pygame.draw.rect(self.screen, white, points)

        self.button(self.screen, (128,0,128), 225, 300, 150, 55, 'cambriacambriamath', 30, 'YES', white, 280, 310)
        self.button(self.screen,(128,0,128), 225, 400, 150, 55, 'cambriacambriamath', 30, 'NO', white, 280, 410)
        self.heading(self.screen,"freesansbold.ttf", 18, 'ARE YOU SURE YOU WANT TO EXIT ?', black, 280)

    #Exit
    def main2(self):
        game = True
        while (game == True):

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()                
                mouse = pygame.mouse.get_pos()
                
                if 225 < mouse[0] < 200 + 200 and 300 < mouse[1] < 300 + 55:

                    self.button(self.screen, a, 225, 300, 150, 55, 'cambriacambriamath', 30, 'YES', white, 280, 310)
                    if event.type==pygame.MOUSEBUTTONDOWN:
                        gameclick = mixer.Sound('click.wav')
                        gameclick.play()
                        game = False

                else:
                    self.button(self.screen, (128,0,128), 225, 300, 150, 55, 'cambriacambriamath', 30, 'YES', white, 280, 310)

                if 225 < mouse[0] < 200 + 200 and 400 < mouse[1] < 400 + 55:

                    self.button(self.screen, a, 225, 400, 150, 55, 'cambriacambriamath', 30, 'NO', white, 280, 410)
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        gameclick = mixer.Sound('click.wav')
                        gameclick.play()
                        
                        obj6 = mainmenu()
                        game = False

                else:
                    self.button(self.screen,(128,0,128), 225, 400, 150, 55, 'cambriacambriamath', 30, 'NO', white, 280, 410)

            pygame.display.update()

obj = mainmenu()
