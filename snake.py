
import pygame
import random
from random import choice

# 遊戲詞典（英文: 中文）
words = ["apple蘋果", "banana香蕉", "cat貓", "dog狗", "fish魚", 'number數字', 'about大約', 'print輸入']
words_english = ['apple', 'banana', 'cat', 'dog', 'fish', 'number', 'about', 'print']
words_chinese = ["蘋果", "香蕉", "貓", "狗", "魚", '數字', '大約', '輸入']

# 定義螢幕
screen_w = 600
screen_h = 400

pygame.init()
screen = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption("Snake Game")

# 顏色
white = (255, 255, 255)
black = (50, 50, 50)
red = (210, 0, 0)

block_size = 20 #尺寸
clock = pygame.time.Clock()

#定義字形
def draw_text(text, size, color, x, y):
    font = pygame.font.Font(None, size)
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(x, y))
    screen.blit(surface, rect)

def draw_sing(text, size, color, x, y):
    font = pygame.font.Font(None, size)
    surface = font.render(text, True, color)
    rect = surface.get_rect(topleft=(x, y))
    screen.blit(surface, rect)

def draw_text_chinese(text, size, color, x, y):
    font = pygame.font.SysFont("Microsoft JhengHei", 120)
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(x, y))
    screen.blit(surface, rect)

#初始、結束頁面
def menu_over_loop():
    waiting = True
    #按鈕座標
    button_w, button_h = 200, 60
    button_x = screen_w // 2 - button_w // 2
    button_y = screen_h // 2

    while waiting:
        screen.fill(white)
        if state == 'menu':
            draw_text("Snake spelling Gamesu ", 60, black, screen_w//2, screen_h//3)
        else:
            draw_text("Game over", 60, black, screen_w // 2, screen_h // 3)

        # 取得滑鼠位置
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        # 判斷滑鼠是否在按鈕範圍內
        if ((button_x <= mouse_pos[0] <= button_x + button_w) and (button_y <= mouse_pos[1] <= button_y + button_h)):
            color = (200, 0, 0)  # 滑過去變紅色
            if mouse_click[0]:   # 左鍵點擊
                return "play"
        else:
            color = (0, 150, 0)  # 平常是綠色

        # 畫按鈕
        pygame.draw.rect(screen, color, (button_x, button_y, button_w, button_h), border_radius=10)
        draw_text("Start Game", 40, white, button_x + button_w//2, button_y + button_h//2)

        draw_text("Press ESC to Quit", 30, black, screen_w//2, button_y + 100)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "quit"

def game_loop():
    snake = [(screen_w // 2, screen_h // 2)]

    food = (random.randint(0, (screen_w // block_size)-1) * block_size,
            random.randint(0, (screen_h // block_size)-1) * block_size)

    single_word = (choice(words_english)) #從字庫中取字串
    text_number = words_english.index(single_word) #取得字串位置
    text = words[text_number]
    number = 0
    draw_text(single_word[number], 10, black, food[0], food[1])

    direction = "right"
    score = 0
    speed = 10

    running = True
    while running:

        # 方向控制
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction = "left"
                elif event.key == pygame.K_RIGHT:
                    direction = "right"
                elif event.key == pygame.K_DOWN:
                    direction = "down"
                elif event.key == pygame.K_UP:
                    direction = "up"

        # 蛇移動
        x, y = snake[-1]
        if direction == "left":
            new_head = (x - block_size, y)
        elif direction == "right":
            new_head = (x + block_size, y)
        elif direction == "down":
            new_head = (x, y + block_size)
        else:
            new_head = (x, y - block_size)
        #添加新頭
        snake.append(new_head)

        #判斷蛇有沒有吃到
        if new_head == food:
            score += 1
            food = (random.randint(0, (screen_w // block_size)-1) * block_size,
                    random.randint(0, (screen_h // block_size)-1) * block_size)

            light = len(single_word)
            if number < len(single_word) -1 :
                #draw_text(single_word[number], 30, black, food[0], food[1])
                number += 1

            else:
                single_word = (choice(words_english))  # 從字庫中取字串
                text_number = words_english.index(single_word) # 取得字串位置
                text = words[text_number]
                number = 0
                draw_text(single_word[number], 10, black, food[0], food[1])

        else:
            snake.pop(0)

        # collision check
        if (new_head[0] < 0 or new_head[0] >= screen_w or
            new_head[1] < 0 or new_head[1] >= screen_h or
            new_head in snake[:-1]):
            return "game over"

        # 清空
        screen.fill(white)

        # 畫蛇
        for X, Y in snake:
            pygame.draw.rect(screen, black, (X, Y, block_size, block_size))

        # 畫食物(字母)
        pygame.draw.rect(screen, red, (food[0], food[1], block_size, block_size))
        draw_text(single_word[number], 20, white, food[0] + block_size // 2, food[1] + block_size // 2)

        # 畫分數
        draw_text(f"Score: {score}", 30, black, screen_w - 70, 35)
        draw_sing(f"Spell :  {single_word[:number]}{'_ ' * (len(single_word)-number)}", 30, black, 20, 20)

        pygame.display.flip()
        clock.tick(speed)


# 遊戲流程
state = "menu"
while True:
    if state == "menu":
        state = menu_over_loop()
    elif state == "play":
        state = game_loop()
    elif state == "game over":
        state = menu_over_loop()
    elif state == "quit":
        break

pygame.quit()
