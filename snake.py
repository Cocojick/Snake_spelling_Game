import json
import pygame
import random
import os
import sys
from random import choice

# 遊戲詞典（英文: 中文）
'''words = ["apple蘋果", "banana香蕉", "cat貓", "dog狗", "fish魚", 'number數字', 'about大約', 'print輸入']
words_english = ['apple', 'banana', 'cat', 'dog', 'fish', 'number', 'about', 'print']
words_chinese = ["蘋果", "香蕉", "貓", "狗", "魚", '數字', '大約', '輸入']'''

ENGLISH = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # PyInstaller 暫存路徑
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

with open(resource_path("single_word.json"), "r", encoding="utf-8") as f:
    word_data = json.load(f)

words_english = [w["en"] for w in word_data]
words_chinese = [w["zh"] for w in word_data]
words = [w["en"] + w["zh"] for w in word_data]

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
    font = pygame.font.Font(resource_path("GenSekiGothic2-M.ttc"), size)
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(x, y))
    screen.blit(surface, rect)

def draw_sing(text, size, color, x, y):
    font = pygame.font.Font(resource_path("GenSekiGothic2-M.ttc"), size)
    surface = font.render(text, True, color)
    rect = surface.get_rect(topleft=(x, y))
    screen.blit(surface, rect)

#初始、結束頁面
def menu_over_loop(score=0):
    waiting = True
    #按鈕座標
    button_w, button_h = 200, 60
    button_x = screen_w // 2 - button_w // 2
    button_y = 190

    while waiting:
        screen.fill(white)
        if state == 'menu':
            draw_text("Snake spelling Gamesu ", 45, black, screen_w//2, button_y-50)
        else:
            draw_text("Game over", 50, black, screen_w // 2, button_y-50)
            draw_text(f"Score: {score}", 30, black, screen_w // 2, button_y-100)

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
        draw_text("Start Game", 30, white, button_x + button_w//2, button_y + button_h//2)

        draw_text("Press ESC to Quit", 20, black, screen_w//2, button_y + 110)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "quit"

def game_loop():
    snake = [(screen_w // 2, screen_h // 2)]
    food = (random.randint(0, (screen_w // block_size) - 1) * block_size,
            random.randint((screen_h // 2) // block_size, (screen_h // block_size) - 1) * block_size)
    food2 = food
    while food2 == food :
        food2 = (random.randint(0, (screen_w // block_size) - 1) * block_size,
                 random.randint((screen_h // 2) // block_size, (screen_h // block_size) - 1) * block_size)

    single_word = (choice(words_english)) #從字庫中取字串
    text_number = words_english.index(single_word) #取得字串位置
    text_chinese = words_chinese[text_number]
    text_new = words[text_number]
    text_old = None
    number = 0
    random_english = single_word[number]
    while random_english == single_word[number]:
        random_english = ENGLISH[random.randint(0, 25)]
        #print(random_english)

    draw_text(single_word[number], 10, black, food[0], food[1])
    draw_text(random_english, 10, black, food2[0], food2[1])
    draw_text('_'*44, 20, black, screen_w //2, 55)

    direction = "right"
    score = 0
    speed = 10

    running = True
    while running:

        #測試
        AUTO = False
        if AUTO:

            boby_x = boby_y = []
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

            # 自動控制蛇（追正確食物 food）
            head_x, head_y = snake[-1]
            #print(head_x)
            boby_temporary_x = boby_temporary_y = None
            target_x, target_y = food
            distance_x = int(head_x) - int(target_x)
            distance_y = int(head_y) - int(target_y)
            count = 0
            '''while count < len(snake):
                boby_temporary_x, boby_temporary_y = snake[count]
                print(boby_temporary_x)
                boby_x.append(boby_temporary_x)
                boby_y.append(boby_temporary_y)
                boby_x.pop()
                boby_y.pop()
                count += 1
                print(boby_x)'''

            if distance_x < 0 and direction != "left" and head_x + block_size != snake:
                direction = "right"
            elif distance_x > 0 and direction != "right" and head_x - block_size != snake:
                direction = "left"
            elif distance_y < 0 and direction != "up" and head_y + block_size != snake:
                direction = "down"
            else:
                direction = "up"

            '''if head_x < target_x and direction != "left" and head_x <= screen_w:
                direction = "right"
            elif head_x > target_x and direction != "left" and head_x > 0:
                direction = "left"
            elif head_y < target_y and direction != "up" and head_y  <= screen_h:
                direction = "down"
            elif head_y > target_y and direction != "down":
                direction = "up"'''

        else:
            # 方向控制
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and direction != "right":
                        direction = "left"
                    elif event.key == pygame.K_RIGHT and direction != "left":
                        direction = "right"
                    elif event.key == pygame.K_DOWN and direction != "up":
                        direction = "down"
                    elif event.key == pygame.K_UP and direction != "down":
                        direction = "up"

        # 蛇移動
        x, y = snake[-1]
        new_direction = direction

        if direction == "left":
            new_head = (x - block_size, y)
        elif direction == "right":
            new_head = (x + block_size, y)
        elif direction == "down":
            new_head = (x, y + block_size)
        else:
            new_head = (x, y - block_size)

        direction = new_direction
        #添加新頭
        snake.append(new_head)
        count = 0
        #print(snake,'snake')

        #判斷蛇有沒有吃到
        if new_head == food:
            score += 1
            #創建新食物
            food = (random.randint(0, (screen_w // block_size)-1) * block_size,
                    random.randint((screen_h // 2) // block_size, (screen_h // block_size) - 1) * block_size)
            food2 = food
            while food2 == food:
                food2 = (random.randint(0, (screen_w // block_size) - 1) * block_size,
                         random.randint((screen_h // 2) // block_size, (screen_h // block_size) - 1) * block_size)
            while random_english == single_word[number]:
                random_english = ENGLISH[random.randint(0, 25)]
            #計算單字
            if number < len(single_word) -1 :
                #draw_text(single_word[number], 30, black, food[0], food[1])
                number += 1

            else:
                single_word = (choice(words_english))  # 從字庫中取字串
                text_number = words_english.index(single_word) # 取得字串位置
                text_chinese = words_chinese[text_number]
                text_old = text_new
                text_new = words[text_number]
                number = 0
                random_english = single_word[number]
                while random_english == single_word[number]:
                    random_english = ENGLISH[random.randint(0, 25)]

                draw_text(single_word[number], 10, black, food[0], food[1])
                draw_text(random_english, 10, black, food2[0], food2[1])
                draw_text('_' * 44, 20, black, screen_w // 2, 55)

        elif new_head == food2:
            score -= 1
            food = (random.randint(0, (screen_w // block_size) - 1) * block_size,
                    random.randint((screen_h // 2) // block_size, (screen_h // block_size) - 1) * block_size)
            food2 = food
            while food2 == food:
                food2 = (random.randint(0, (screen_w // block_size) - 1) * block_size,
                         random.randint((screen_h // 2) // block_size, (screen_h // block_size) - 1) * block_size)
            while random_english == single_word[number]:
                random_english = ENGLISH[random.randint(0, 25)]

        else:
            snake.pop(0)

        # collision check
        if (new_head[0] < 0 or new_head[0] >= screen_w or
            new_head[1] < 0 or new_head[1] >= screen_h or
            new_head in snake[:-1]):
            return "game over", score

        # 清空
        screen.fill(white)

        # 畫蛇
        for X, Y in snake:
            pygame.draw.rect(screen, black, (X, Y, block_size, block_size))

        # 畫食物(字母)
        pygame.draw.rect(screen, red, (food[0], food[1], block_size, block_size))
        pygame.draw.rect(screen, red, (food2[0], food2[1], block_size, block_size))
        draw_text(single_word[number], 20, white, food[0] + block_size // 2, food[1] + block_size // 2)
        draw_text(random_english, 20, white, food2[0] + block_size // 2, food2[1] + block_size // 2)
        draw_text('_' * 44, 20, black, screen_w // 2, 55)

        # 畫分數
        draw_text(f"Score: {score}", 25, black, screen_w - 70, 35)
        draw_sing(f"Spell :  {single_word[:number]}{'_ ' * (len(single_word)-number)}{text_chinese}", 25, black, 20, 20)
        #draw_text(text_old, 15, black, screen_w // 2 , 35)

        pygame.display.flip()
        clock.tick(speed)


# 遊戲流程
state = "menu"
while True:
    if state == "menu":
        state = menu_over_loop()
    elif state == "play":
        state, score = game_loop()
    elif state == "game over":
        state = menu_over_loop(score)
    elif state == "quit":
        break

pygame.quit()
