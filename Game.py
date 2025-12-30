import pygame
import random
import sys
import time

# 初始化pygame
pygame.init()

# 游戏常量
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

# 创建窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("贪吃蛇游戏")
clock = pygame.time.Clock()

# 字体
font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 24)

class Snake:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.length = 3
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        self.score = 0
        self.grow_pending = 2  # 初始长度为3，所以需要增长2次
        
    def get_head_position(self):
        return self.positions[0]
    
    def update(self):
        head = self.get_head_position()
        x, y = self.direction
        new_position = (((head[0] + x) % GRID_WIDTH), ((head[1] + y) % GRID_HEIGHT))
        
        # 检查是否撞到自己
        if new_position in self.positions[1:]:
            return False
            
        self.positions.insert(0, new_position)
        
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.positions.pop()
            
        return True
    
    def grow(self):
        self.grow_pending += 1
        self.score += 10
    
    def render(self, surface):
        for i, pos in enumerate(self.positions):
            color = GREEN if i == 0 else (0, 200, 0)  # 头部颜色稍深
            rect = pygame.Rect(pos[0] * GRID_SIZE, pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position()
        
    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
    
    def render(self, surface):
        rect = pygame.Rect(self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, RED, rect)
        pygame.draw.rect(surface, BLACK, rect, 1)

def draw_grid(surface):
    for y in range(0, HEIGHT, GRID_SIZE):
        for x in range(0, WIDTH, GRID_SIZE):
            rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, GRAY, rect, 1)

def draw_timer(surface, remaining_time):
    timer_text = font.render(f"时间: {remaining_time}s", True, WHITE)
    surface.blit(timer_text, (10, 10))

def draw_score(surface, score):
    score_text = font.render(f"得分: {score}", True, WHITE)
    surface.blit(score_text, (WIDTH - 150, 10))

def draw_game_over(surface, score, time_up):
    surface.fill(BLACK)
    if time_up:
        game_over_text = font.render("游戏结束！时间到！", True, RED)
    else:
        game_over_text = font.render("游戏结束！撞到自己了！", True, RED)
    
    score_text = font.render(f"最终得分: {score}", True, WHITE)
    restart_text = small_font.render("按 R 键重新开始", True, WHITE)
    
    surface.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 60))
    surface.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
    surface.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 60))

def main():
    snake = Snake()
    food = Food()
    game_over = False
    time_up = False
    start_time = time.time()
    total_time = 60  # 60秒倒计时
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if game_over and event.key == pygame.K_r:
                    snake.reset()
                    food.randomize_position()
                    game_over = False
                    time_up = False
                    start_time = time.time()
                elif not game_over:
                    if event.key == pygame.K_UP and snake.direction != (0, 1):
                        snake.direction = (0, -1)
                    elif event.key == pygame.K_DOWN and snake.direction != (0, -1):
                        snake.direction = (0, 1)
                    elif event.key == pygame.K_LEFT and snake.direction != (1, 0):
                        snake.direction = (-1, 0)
                    elif event.key == pygame.K_RIGHT and snake.direction != (-1, 0):
                        snake.direction = (1, 0)
        
        if not game_over:
            # 更新游戏逻辑
            if not snake.update():
                game_over = True
                time_up = False
            
            # 检查是否吃到食物
            if snake.get_head_position() == food.position:
                snake.grow()
                food.randomize_position()
                # 确保食物不在蛇身上
                while food.position in snake.positions:
                    food.randomize_position()
            
            # 检查倒计时
            elapsed_time = int(time.time() - start_time)
            remaining_time = max(0, total_time - elapsed_time)
            
            if remaining_time <= 0:
                game_over = True
                time_up = True
        
        # 绘制游戏画面
        screen.fill(BLACK)
        draw_grid(screen)
        
        if not game_over:
            snake.render(screen)
            food.render(screen)
            draw_timer(screen, remaining_time)
            draw_score(screen, snake.score)
        else:
            draw_game_over(screen, snake.score, time_up)
        
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()