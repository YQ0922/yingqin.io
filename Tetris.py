import pygame
import cv2
import mediapipe as mp
import os
import random

mpHands = mp.solutions.hands  # mediapipe 偵測手掌方法
hands = mpHands.Hands()  # mediapipe 啟用偵測手掌
mpDraw = mp.solutions.drawing_utils  # mediapipe 繪圖方法

cam = cv2.VideoCapture(0)  # 開啟攝影機

os.environ['SDL_VIDEO_WINDOW_POS'] = "560,30"  # 設定視窗位置
pygame.font.init()  # 初始化字體

s_width = 800
s_height = 600
play_width = 300
play_height = 600
block_size = 30
top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height - 10

# 設定方塊
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

# 設定各種方塊的顏色
shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 230, 115), (255, 51, 51), (0, 204, 255), (255, 255, 128), (0, 102, 255), (255, 140, 26),
                (204, 51, 255)]


# 方塊初始化
class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


# 建立遊戲區域網格
def create_grid(locked_pos={}):
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_pos:
                c = locked_pos[(j, i)]
                grid[i][j] = c
    return grid


# 將方塊形狀轉換成在網格中位置
def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    # 方塊位於中央
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


# 測試下降的方塊是否位於合理/有效的空間
def valid_space(shape, grid):
    # 可接受方塊的位置為網格中顏色為 (0,0,0) 的位置
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convert_shape_format(shape)

    for pos in formatted:
        # 如果方塊位置的行數大於 -1，表示已超出遊戲區域
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True


# 檢查方塊是否超出遊戲區域頂部
def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True

    return False


# 取得隨機方塊
def get_shape():
    return Piece(5, 0, random.choice(shapes))


# 在螢幕中顯示文字
def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont("britannic", size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (
    top_left_x + play_width / 2 - (label.get_width() / 2), top_left_y + play_height / 2 - label.get_height() / 2))


# 繪製網格線
def draw_grid(surface, grid):
    sx = top_left_x
    sy = top_left_y

    # 繪製水平線
    for i in range(len(grid)):
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + i * block_size), (sx + play_width, sy + i * block_size))
        # 繪製垂直線
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128), (sx + j * block_size, sy),
                             (sx + j * block_size, sy + play_height))


# 消除一行
def clear_rows(grid, locked):
    inc = 0
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]  # 取得每一行方塊的狀態

        # 如果沒有空的區塊，則清除
        if (0, 0, 0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue

    # 如果有進行清除
    if inc > 0:
        # 將鎖定的方塊由小到大排序
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            # 如果鎖定的方塊在被清除的行上方，則向下移動 inc 行
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)

    return inc


# 繪製顯示下一個方塊的視窗
def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('britannic', 30)
    label = font.render('Next Shape', 1, (255, 255, 255))

    # 計算下一個方塊的顯示位置
    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    # 繪製方塊
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color,
                                 (sx + j * block_size, sy + i * block_size, block_size, block_size), 0)

    # 顯示文字
    surface.blit(label, (sx + 10, sy - 40))


# 繪製遊戲視窗
def draw_window(surface, grid, score=0):
    surface.fill((0, 0, 0))  # 填充背景色

    pygame.font.init()
    font = pygame.font.SysFont('britannic', 60)
    label = font.render('TETRIS', 1, (255, 255, 255))

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 15))

    # 顯示分數
    font = pygame.font.SysFont('britannic', 30)
    label = font.render('Score: ' + str(score), 1, (255, 255, 255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 100

    surface.blit(label, (sx + 20, sy + 160))

    # 繪製遊戲網格
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j],
                             (top_left_x + j * block_size, top_left_y + i * block_size, block_size, block_size), 0)

    # 繪製遊戲區域的邊框
    pygame.draw.rect(surface, (215, 215, 215), (top_left_x, top_left_y, play_width, play_height), 5)

    draw_grid(surface, grid)


# 根據消除的行數增加分數
def add_score(rows):
    conversion = {
        0: 0,
        1: 40,
        2: 100,
        3: 300,
        4: 1200
    }
    return conversion.get(rows)


# 主程式
def main(win):
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed_real = 0.45
    fall_speed = fall_speed_real
    level_time = 0
    score = 0

    left_wait = 0
    right_wait = 0
    rotate_wait = 0
    down_wait = 0
    fall_speed_down = 0.8  # 方塊下降速度

    while run:
        grid = create_grid(locked_positions)

        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        success, img = cam.read()  # 持續抓取影像
        imgg = cv2.flip(img, 1)
        imgRGB = cv2.cvtColor(imgg, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = imgg.shape
                    if id == 0:
                        x = []
                        y = []
                    x.append(int((lm.x) * w))
                    y.append(int((1 - lm.y) * h))

                    # 偵測手勢
                    if len(y) > 20:
                        # 左移
                        if (x[0] > x[3] > x[4]) and not (y[20] > y[17]):
                            left_wait += 1
                        # 右移
                        if not (x[0] > x[3] > x[4]) and (y[20] > y[17]):
                            right_wait += 1
                        # 旋轉
                        if (x[0] > x[3] > x[4]) and (y[20] > y[17]):
                            rotate_wait += 1

                # 繪製手部節點
                mpDraw.draw_landmarks(imgg, handLms, mpHands.HAND_CONNECTIONS)

        else:
            down_wait += 1

        cv2.namedWindow("WebCam")
        cv2.moveWindow("WebCam", 20, 121)
        cv2.imshow("WebCam", imgg)
        cv2.waitKey(1)

        # 每隔 10 秒，下降速度增加 0.03 秒（上限 0.25 秒）
        if level_time / 1000 > 10:
            level_time = 0
            if fall_speed_real > 0.25:
                fall_speed_real -= 0.03

        # 如果超過時間，方塊下降一格
        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            # 是否位於有效區域
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        # 左移
        if left_wait >= 4:
            current_piece.x -= 1
            if not (valid_space(current_piece, grid)):
                current_piece.x += 1
            left_wait = 0
            right_wait = 0
            rotate_wait = 0
            down_wait = 0

        # 右移
        if right_wait >= 4:
            current_piece.x += 1
            if not (valid_space(current_piece, grid)):
                current_piece.x -= 1
            left_wait = 0
            right_wait = 0
            rotate_wait = 0
            down_wait = 0

        # 旋轉
        if rotate_wait >= 4:
            current_piece.rotation += 1
            if not (valid_space(current_piece, grid)):
                current_piece.rotation -= 1
            left_wait = 0
            right_wait = 0
            rotate_wait = 0
            down_wait = 0

        # 螢幕上沒有手時，加速下降
        if down_wait >= 5:
            fall_speed = fall_speed_down
            left_wait = 0
            right_wait = 0
            rotate_wait = 0
            down_wait = 0

        shape_pos = convert_shape_format(current_piece)

        # 將方塊位置轉為網格座標
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        # 如果變換方塊
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                # 將當前方塊加入鎖定位置
                locked_positions[p] = current_piece.color
            # 取得下一個方塊
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            # 根據消除行樹更新得分
            score += add_score(clear_rows(grid, locked_positions))
            fall_speed = fall_speed_real
            down_wait = 0

        draw_window(win, grid, score)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        if check_lost(locked_positions):
            draw_text_middle(win, "I am Ying-Qin Chen",24, (255, 255, 255))
            pygame.display.update()
            pygame.time.delay(1500)
            run = False

        if cv2.waitKey(1) == ord('q'):  # 按 q 結束遊戲
            run = False
            break


def main_menu(win):
    run = True
    while run:
        win.fill((0, 0, 0))
        draw_text_middle(win, 'Press Any Key To Start', 60, (255, 255, 255))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(win)

    pygame.display.quit()


win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('TETRIS')
main_menu(win)