
import pygame
import sys
import random
import time

pygame.init() # pygame 모듈 초기화

img_neko = [ 
    None,
    pygame.image.load("neko1.png"),
    pygame.image.load("neko2.png"),
    pygame.image.load("neko3.png"),
    pygame.image.load("neko4.png"),
    pygame.image.load("neko5.png"),
    pygame.image.load("neko6.png"),
    pygame.image.load("neko_niku.png"),
]




map_y = 10
map_x = 8
display_width = 912
display_height = 768
bg = pygame.image.load("neko_bg.png")
cursor = pygame.image.load("neko_cursor.png")

neko = [[] for _ in range(map_y)]
check = [[0 for _ in range(map_x)] for _ in range(map_y)]
search= [[0 for _ in range(map_x)] for _ in range(map_y)]
for y in range(map_y):
    for x in range(map_x):
        neko[y].append(random.choice(range(1,7)))


gameDisplay = pygame.display.set_mode((display_width, display_height)) #스크린 초기화
pygame.display.set_caption("애니팡")  # 타이틀
clock = pygame.time.Clock() #Clock 오브젝트 초기화

class Mouse :
    def __init__(self,cursor,map_y,map_x):
        self.turn = 0
        self.cursor = cursor
        self.map_y = map_y
        self.map_x = map_x

    def get_mouse(self):
        position = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        for y in range(map_y):
            for x in range(map_x):
                if x*72+20 < position[0] < (x+1)*72+20 and y*72+20 < position[1] < (y+1)*72+20 :
                    if self.turn == 0 :
                        gameDisplay.blit(self.cursor,(x*72+20,y*72+20))
                        if click[0] :
                            self.turn = 1
                            check[y][x] = 1
                    else :
                        if (0 <= y-1 and check[y-1][x] == 1) or (y+1 < self.map_y and check[y+1][x] == 1) \
                            or (self.map_x > x+1 and check[y][x+1] == 1) or (0 <= x-1 and check[y][x-1] == 1):
                            gameDisplay.blit(self.cursor,(x*72+20,y*72+20)) 
                            if click[0] :
                                self.turn = 0
                                check[y][x]=1
                                switch_neko()
                                if not check_switch(y,x):
                                    switch_neko()
                                cursor_set()

                        if click[2] :
                            self.turn=0
                            cursor_set()
                            # 초기화 시켜주기

def switch_neko():
    stack=[]
    for y in range(map_y):
        for x in range(map_x):
            if check[y][x]==1:
                stack.append((y,x))
    print(stack)
    neko[stack[0][0]][stack[0][1]],neko[stack[1][0]][stack[1][1]]=neko[stack[1][0]][stack[1][1]],neko[stack[0][0]][stack[0][1]]
    ...

def check_neko(idx):
    global neko
    for y in range(map_y-2):
        for x in range(map_x):
            
            if neko[y][x]>0 and neko[y][x]==neko[y+1][x]==neko[y+2][x]:
                neko[y][x],neko[y+1][x],neko[y+2][x]=7,7,7
                idx=1
    for y in range(map_y):
        for x in range(map_x-2):
            if neko[y][x]>0 and neko[y][x]==neko[y][x+1]==neko[y][x+2]:
                neko[y][x],neko[y][x+1],neko[y][x+2]=7,7,7
                idx=1
    return idx

# 상화좌우 3 조건 맞추면 7로 바꿔주기 
def neko_pop():
    global neko
    for y in range(map_y):
        for x in range(map_x):
            if neko[y][x]==7:
            
                neko[y][x]=0

    
def cursor_set():
    global check
    for y in range(map_y):
        for x in range(map_x):
            check[y][x] = 0
    # 커서 초기화 시켜주기

def cursor_draw():
    for y in range(map_y):
        for x in range(map_x):
            if check[y][x] == 1:
                gameDisplay.blit(cursor,(x*72+20, y*72+20))

def neko_draw():
    for y in range(map_y):
        for x in range(map_x):
            if neko[y][x] > 0 :
                gameDisplay.blit(img_neko[neko[y][x]], (x*72+20, y*72+20))

def drop_neko(): # game 함수 while 이 한 번 돌때마다 
    for y in range(map_y):
        for x in range(map_x):
            if neko[y][x] == 0 :
                if y==0:
                    neko[y][x]=random.choice(range(1,7))
                else:
                    neko[y-1][x],neko[y][x]=neko[y][x],neko[y-1][x]
                # 빈 공간(0)이 있을 시 위에 있는 네코가 밑으로 내려와야 됨
                 # 맨위에 있는 칸이 빈공간일 경우는 랜덤으로 생성시켜야 됨
    

def check_switch(y,x):
    for y in range(10):
        for x in range(8):
            search[y][x] = neko[y][x]

    for y in range(1, 9):
        for x in range(8):
            if search[y][x] > 0:
                if search[y-1][x] == search[y][x] and search[y+1][x] == search[y][x]:
                    return True

    for y in range(10):
        for x in range(1, 7):
            if search[y][x] > 0:
                if search[y][x-1] == search[y][x] and search[y][x+1] == search[y][x]:
                    return True
    return False


def game(): # 메인 게임 함수
    
    tmr = 0 # 시간 관리 변수
    # 마우스 클래스 부르기
    m = Mouse(cursor,map_y,map_x)
    idx = 0
    while True:
        tmr += 1 # 매 시간 1초 증가
        for event in pygame.event.get(): # 윈도운 X 누를 시 나오게끔
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        gameDisplay.blit(bg,(0,0))
        neko_draw()
        m.get_mouse()
        cursor_draw()
        if idx == 0:
            idx = check_neko(idx)
        if 1 <= idx < 3 :
            idx += 1
        if idx == 3 :
            neko_pop()
            idx=0  
        drop_neko()
        pygame.display.update()
        clock.tick(20)

        

game()
