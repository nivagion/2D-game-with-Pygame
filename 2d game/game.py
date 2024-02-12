from turtle import distance
import pygame

class Projectile:
    def __init__(self, x, y, dx, dy, radius):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.radius = radius

pygame.init()

WIDTH, HEIGHT = 900, 600
PLAYER_SIZE = 30
BORDER_THICKNESS = PLAYER_SIZE
PLAYER_SPEED = 200 #in pixels per seconds because of delta time
PROJECTILE_SPEED = 300
PROJECTILE_FIRE_RATE = 0.2 #in seconds
last_shot_time = 0

GRID_COLOR = (200, 200, 200) #light grey color
HIGHLIGHT_COLOR = (200, 230, 200) # v
BACKGROUND_COLOR = (255, 255, 255)
BORDER_COLOR = (0, 0, 0)
POINTER_COLOR = (50, 100, 255)
PROJECTILE_COLOR = (0, 230 , 0)



window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The game")

player = pygame.Rect(WIDTH // 2, HEIGHT // 2, PLAYER_SIZE, PLAYER_SIZE)

clock = pygame.time.Clock()#>dt

grid_colors = []
for _ in range (WIDTH // PLAYER_SIZE):
    row_colors = []
    for _ in range(HEIGHT // PLAYER_SIZE):
        row_colors.append(BACKGROUND_COLOR)
    grid_colors.append(row_colors)
    
projectiles = []

running = True
while running:
    #important so i put it here
    dt = clock.tick(60) / 1000 #limits it to 60fps, returns ms so i divide it by 1000 to return seconds
    mouse_pos = pygame.mouse.get_pos()
    player_center = (player.x + PLAYER_SIZE // 2, player.y + PLAYER_SIZE // 2)
    change_grid_color = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: #only for LMB
                gridX, gridY = mouse_pos[0] // PLAYER_SIZE, mouse_pos[1] // PLAYER_SIZE #calc grid coords
                if change_grid_color:
                    if grid_colors[gridX][gridY] != HIGHLIGHT_COLOR:
                        grid_colors[gridX][gridY] = HIGHLIGHT_COLOR
                    else: 
                        grid_colors[gridX][gridY] = BACKGROUND_COLOR
            
    
    #player movement
    keys = pygame.key.get_pressed() #gets state of all keyboard buttons, True when pressed
    if keys[pygame.K_a]:
        player.x -= PLAYER_SPEED * dt
    if keys[pygame.K_d]:
        player.x += PLAYER_SPEED * dt
    if keys[pygame.K_w]:
        player.y -= PLAYER_SPEED * dt
    if keys[pygame.K_s]:
        player.y += PLAYER_SPEED * dt
    
    #keep in borders
    player.x = max(BORDER_THICKNESS, min(player.x, WIDTH - BORDER_THICKNESS - PLAYER_SIZE)) 
    player.y = max(BORDER_THICKNESS, min(player.y, HEIGHT - BORDER_THICKNESS - PLAYER_SIZE))
    
    #direction vectors, needed for line pointers and projectiles
    dx, dy = mouse_pos[0] - player_center[0], mouse_pos[1] - player_center[1]
    line_lenght = (dx**2 + dy**2)**0.5
    if line_lenght !=0: #div by 0
        dx /= line_lenght #setting vector lenghts to 1
        dy /= line_lenght


    #projectiles
    if pygame.mouse.get_pressed()[0] and pygame.time.get_ticks() / 1000 - last_shot_time >= PROJECTILE_FIRE_RATE:
        projectile = Projectile(player_center[0], player_center[1], dx * PROJECTILE_SPEED, dy * PROJECTILE_SPEED, PLAYER_SIZE // 5)
        projectiles.append(projectile)
        last_shot_time = pygame.time.get_ticks() / 1000

    #--DRAWING--
    window.fill(BACKGROUND_COLOR)
    
    #draw grid squares
    for x in range(WIDTH // PLAYER_SIZE):
        for y in range(HEIGHT // PLAYER_SIZE):
            pygame.draw.rect(window, grid_colors[x][y], pygame.Rect(x * PLAYER_SIZE, y * PLAYER_SIZE, PLAYER_SIZE, PLAYER_SIZE))
    #grid lines    
    for x in range(0, WIDTH, PLAYER_SIZE):
        pygame.draw.line(window, GRID_COLOR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, PLAYER_SIZE):
        pygame.draw.line(window, GRID_COLOR, (0, y), (WIDTH, y))

    #draw borders;                                     (x, y, width,  height          )
    pygame.draw.rect(window, BORDER_COLOR, pygame.Rect(0, 0, WIDTH, BORDER_THICKNESS)) #top
    pygame.draw.rect(window, BORDER_COLOR, pygame.Rect(0, HEIGHT - BORDER_THICKNESS, WIDTH, BORDER_THICKNESS)) #bottom 
    pygame.draw.rect(window, BORDER_COLOR, pygame.Rect(0, 0, BORDER_THICKNESS, HEIGHT)) #top
    pygame.draw.rect(window, BORDER_COLOR, pygame.Rect(WIDTH - BORDER_THICKNESS, 0, BORDER_THICKNESS, HEIGHT)) #top
    
    #draw player
    pygame.draw.rect(window, (255, 0, 0), player)
    
    #draw line pointer
    start_pos = (player_center[0] + dx * PLAYER_SIZE // 3, player_center[1] + dy * PLAYER_SIZE // 3)
    end_pos = (start_pos[0] + dx * PLAYER_SIZE * 1, start_pos[1] + dy * PLAYER_SIZE * 1)
    pygame.draw.line(window, POINTER_COLOR, start_pos, end_pos, PLAYER_SIZE // 10)
    
    #move and draw projectiles
    for projectile in projectiles[:]:
        projectile.x += projectile.dx * dt
        projectile.y += projectile.dy * dt
        if not (BORDER_THICKNESS + projectile.radius <= projectile.x <= WIDTH - BORDER_THICKNESS - projectile.radius and
                BORDER_THICKNESS + projectile.radius <= projectile.y <= HEIGHT - BORDER_THICKNESS - projectile.radius):
            projectiles.remove(projectile)
        else:
            pygame.draw.circle(window, PROJECTILE_COLOR, (int(projectile.x), int(projectile.y)), projectile.radius)


    pygame.display.update()


pygame.quit()
