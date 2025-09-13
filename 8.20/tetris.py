import pygame
import sys
import random

# =====================
# === 第1步: 导入包 ===
# =====================
# 已在最上面导入了pygame, sys, random

# ===========================
# === 第2步: 初始化窗口等 ===
# ===========================
# 游戏常量
GRID_WIDTH = 10
GRID_HEIGHT = 20
CELL_SIZE = 30

SCREEN_WIDTH = GRID_WIDTH * CELL_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * CELL_SIZE

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('俄罗斯方块（Tetris）')

# ===========================
# === 第3步: 定义形状颜色 ===
# ===========================
# 形状定义（4x4矩阵）
TETROMINO_SHAPES = {
    'I': [
        [0, 0, 0, 0],
        [1, 1, 1, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ],
    'O': [
        [0, 1, 1, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ],
    'T': [
        [0, 1, 0, 0],
        [1, 1, 1, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ],
    'S': [
        [0, 1, 1, 0],
        [1, 1, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ],
    'Z': [
        [1, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ],
    'J': [
        [1, 0, 0, 0],
        [1, 1, 1, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ],
    'L': [
        [0, 0, 1, 0],
        [1, 1, 1, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ],
}
TETROMINO_COLORS = {
    'I': (0, 240, 240),
    'O': (240, 240, 0),
    'T': (160, 0, 240),
    'S': (0, 240, 0),
    'Z': (240, 0, 0),
    'J': (0, 0, 240),
    'L': (240, 160, 0),
}

# ============================
# === 第4步: 类和场地结构 ===
# ============================
class Tetromino:
    def __init__(self, shape_key, matrix, color):
        self.shape = shape_key
        self.matrix = [row[:] for row in matrix]
        self.color = color
        self.x = GRID_WIDTH // 2 - 2  # 起始中心（矩阵4格宽居中）
        self.y = 0
    def get_cell_positions(self, mx=None, my=None, mtx=None):
        # 返回此方块在场地上的所有格子坐标
        mx = self.x if mx is None else mx
        my = self.y if my is None else my
        mtx = self.matrix if mtx is None else mtx
        cells = []
        for r in range(4):
            for c in range(4):
                if mtx[r][c]:
                    cells.append((my + r, mx + c))
        return cells
    def rotate(self):
        # 顺时针旋转90°（返回一个新的matrix，不更改自身）
        new_matrix = [[0] * 4 for _ in range(4)]
        for r in range(4):
            for c in range(4):
                new_matrix[c][3 - r] = self.matrix[r][c]
        return new_matrix

# 初始化空场地
playfield = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

def create_new_tetromino():
    t = random.choice(list(TETROMINO_SHAPES.keys()))
    m = TETROMINO_SHAPES[t]
    col = TETROMINO_COLORS[t]
    return Tetromino(t, m, col)

# 第5步: 生成新方块
current_tetromino = create_new_tetromino()

def is_valid_position(tetromino, test_x, test_y, test_matrix=None):
    # 检查test_x, test_y, test_matrix下，是否越界/重叠 已落地方块
    positions = tetromino.get_cell_positions(mx=test_x, my=test_y, mtx=test_matrix)
    for row, col in positions:
        if col < 0 or col >= GRID_WIDTH or row < 0 or row >= GRID_HEIGHT:
            return False
        if playfield[row][col] is not None:
            return False
    return True

def move_tetromino(dx):
    global current_tetromino
    new_x = current_tetromino.x + dx
    if is_valid_position(current_tetromino, new_x, current_tetromino.y):
        current_tetromino.x = new_x

def rotate_tetromino():
    global current_tetromino
    rotated_matrix = current_tetromino.rotate()
    if is_valid_position(current_tetromino, current_tetromino.x, current_tetromino.y, rotated_matrix):
        current_tetromino.matrix = rotated_matrix

# ===============================
# === 第8步: 方块加速下落 ===
# ===============================
def move_tetromino_down():
    global current_tetromino
    new_y = current_tetromino.y + 1
    if is_valid_position(current_tetromino, current_tetromino.x, new_y):
        current_tetromino.y = new_y
    else:
        # 方块落地（到底/遇到障碍）
        fix_tetromino()
        spawn_new_tetromino()

# ===============================
# === s-10: 检测方块到底/障碍 ===
# ===============================
def is_tetromino_landed():
    # 如果下移一步就无效，说明到底/遇到障碍
    return not is_valid_position(current_tetromino, current_tetromino.x, current_tetromino.y + 1)

# ===================================
# === s-11: 方块数据写入场地 ===
# ===================================
def fix_tetromino():
    # 将当前方块所有对应格子写入playfield
    for row, col in current_tetromino.get_cell_positions():
        if 0 <= row < GRID_HEIGHT and 0 <= col < GRID_WIDTH:
            playfield[row][col] = current_tetromino.color
    # 实现消行
    clear_lines()

# ===================================
# === s-12: 检查/消除填满的行 ===
# ===================================
def clear_lines():
    global playfield
    new_playfield = []
    lines_cleared = 0
    for row in playfield:
        if all(cell is not None for cell in row):
            # 该行已满，消除
            lines_cleared += 1
        else:
            new_playfield.append(row)
    # 在顶部补充空行
    for _ in range(lines_cleared):
        new_playfield.insert(0, [None for _ in range(GRID_WIDTH)])
    playfield[:] = new_playfield

# ===================================
# === s-13: 检查游戏结束条件 ===
# ===================================
def is_game_over():
    # 新方块初始位置就重叠，判定为游戏结束
    return not is_valid_position(current_tetromino, current_tetromino.x, current_tetromino.y)

game_over = False

def spawn_new_tetromino():
    global current_tetromino, game_over
    current_tetromino = create_new_tetromino()
    if is_game_over():
        game_over = True

# ================================
# === s-9: 方块自然下落事件定时 ===
# ================================
fall_event = pygame.USEREVENT + 1
FALL_DELAY = 500
pygame.time.set_timer(fall_event, FALL_DELAY)

# ================
# 辅助绘制函数   =
# ===============
def draw_grid():
    # 绘制灰色网格线（可选）
    for x in range(GRID_WIDTH + 1):
        pygame.draw.line(screen, (50, 50, 50), (x*CELL_SIZE, 0), (x*CELL_SIZE, SCREEN_HEIGHT))
    for y in range(GRID_HEIGHT + 1):
        pygame.draw.line(screen, (50, 50, 50), (0, y*CELL_SIZE), (SCREEN_WIDTH, y*CELL_SIZE))

# ===================================
# === 游戏主循环与事件处理（s-16） ===
# ===================================
running = True
font = pygame.font.SysFont('SimHei', 36)  # 用于显示Game Over
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_LEFT:
                move_tetromino(-1)
            elif event.key == pygame.K_RIGHT:
                move_tetromino(1)
            elif event.key == pygame.K_UP:
                rotate_tetromino()
            elif event.key == pygame.K_DOWN:
                move_tetromino_down()
        elif event.type == fall_event and not game_over:
            move_tetromino_down()

    # ============================
    # --- 场地绘制（s-14） ---
    # ===========================
    screen.fill((0, 0, 0))

    # --- 绘制已落定的方块（s-14） ---
    for r in range(GRID_HEIGHT):
        for c in range(GRID_WIDTH):
            color = playfield[r][c]
            if color:
                pygame.draw.rect(
                    screen,
                    color,
                    pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                )
                # 绘制方块边框
                pygame.draw.rect(
                    screen,
                    (40, 40, 40),
                    pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                    1
                )

    # --- 绘制下落中的方块（s-15） ---
    if not game_over:
        for row, col in current_tetromino.get_cell_positions():
            if 0 <= row < GRID_HEIGHT and 0 <= col < GRID_WIDTH:
                pygame.draw.rect(
                    screen,
                    current_tetromino.color,
                    pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                )
                pygame.draw.rect(
                    screen,
                    (255, 255, 255),
                    pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                    2
                )

    # 绘制网格线（可选）
    draw_grid()

    # --- 显示Game Over提示 ---
    if game_over:
        text = font.render('游戏结束', True, (255, 0, 0))
        rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        screen.blit(text, rect)

    # 刷新窗口
    pygame.display.flip()
    
    # 稍微降低帧率，避免CPU爆满
    pygame.time.delay(16)
