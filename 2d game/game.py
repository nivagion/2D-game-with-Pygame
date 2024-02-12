import stat
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
pygame.font.init()


WIDTH, HEIGHT = 900, 600
PLAYER_SIZE = 30
BORDER_THICKNESS = PLAYER_SIZE
PLAYER_SPEED = 200 #in pixels per seconds because of delta time
PROJECTILE_SPEED = 300
PROJECTILE_FIRE_RATE = 0.09 #in seconds
last_shot_time = 0

GRID_COLOR = (200, 200, 200) #light grey color
HIGHLIGHT_COLOR = (200, 230, 200) # v
BACKGROUND_COLOR = (255, 255, 255)
BORDER_COLOR = (0, 0, 0)
POINTER_COLOR = (50, 100, 255)
PROJECTILE_COLOR = (0, 230 , 0)

STATUS_FONT = pygame.font.SysFont('Comic Sans MS', int(PLAYER_SIZE // 1.5))
STATUS_FONT_COLOR = (255,255,255)

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

change_grid_color = False
can_you_shoot = True

running = True
while running:
    #important so i put it here
    dt = clock.tick(60) / 1000 #limits it to 60fps, returns ms so i divide it by 1000 to return seconds
    mouse_pos = pygame.mouse.get_pos()
    player_center = (player.x + PLAYER_SIZE // 2, player.y + PLAYER_SIZE // 2)
    
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
            elif event.button == 3: #RMB
                change_grid_color = not change_grid_color
                can_you_shoot = not can_you_shoot
            
    
    #player movement
    keys = pygame.key.get_pressed() #gets state of all keyboard buttons, True when pressed
    newX, newY = player.x, player.y
    if keys[pygame.K_a]:
        newX -= PLAYER_SPEED * dt
    if keys[pygame.K_d]:
         newX+= PLAYER_SPEED * dt
    if keys[pygame.K_w]:
        newY -= PLAYER_SPEED * dt
    if keys[pygame.K_s]:
        newY += PLAYER_SPEED * dt
        
    #if player is in a wall, 2 checks for sliding on walls
    gridX1, gridY1 = int(newX) // PLAYER_SIZE, int(player.y) // PLAYER_SIZE #top left
    gridX2, gridY2 = int(newX + PLAYER_SIZE) // PLAYER_SIZE, int(player.y) // PLAYER_SIZE #top right
    gridX3, gridY3 = int(newX) // PLAYER_SIZE, int(player.y + PLAYER_SIZE) // PLAYER_SIZE #bottom left
    gridX4, gridY4 = int(newX + PLAYER_SIZE) // PLAYER_SIZE, int(player.y + PLAYER_SIZE) // PLAYER_SIZE #bottom left    

    if (grid_colors[gridX1][gridY1] != HIGHLIGHT_COLOR and
        grid_colors[gridX2][gridY2] != HIGHLIGHT_COLOR and
        grid_colors[gridX3][gridY3] != HIGHLIGHT_COLOR and
        grid_colors[gridX4][gridY4] != HIGHLIGHT_COLOR):
        player.x = newX
    
    gridX1, gridY1 = int(player.x) // PLAYER_SIZE, int(newY) // PLAYER_SIZE #top left
    gridX2, gridY2 = int(player.x + PLAYER_SIZE) // PLAYER_SIZE, int(newY) // PLAYER_SIZE #top right
    gridX3, gridY3 = int(player.x) // PLAYER_SIZE, int(newY + PLAYER_SIZE) // PLAYER_SIZE #bottom left
    gridX4, gridY4 = int(player.x + PLAYER_SIZE) // PLAYER_SIZE, int(newY + PLAYER_SIZE) // PLAYER_SIZE #bottom left  
    
    if (grid_colors[gridX1][gridY1] != HIGHLIGHT_COLOR and
        grid_colors[gridX2][gridY2] != HIGHLIGHT_COLOR and
        grid_colors[gridX3][gridY3] != HIGHLIGHT_COLOR and
        grid_colors[gridX4][gridY4] != HIGHLIGHT_COLOR):
        player.y = newY

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
    if can_you_shoot and pygame.mouse.get_pressed()[0] and pygame.time.get_ticks() / 1000 - last_shot_time >= PROJECTILE_FIRE_RATE:
        projectile = Projectile(player_center[0], player_center[1], dx * PROJECTILE_SPEED, dy * PROJECTILE_SPEED, PLAYER_SIZE // 5)
        projectiles.append(projectile)
        last_shot_time = pygame.time.get_ticks() / 1000

    #--DRAWING--
        #window.fill(BACKGROUND_COLOR)
    
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
        newX = projectile.x + projectile.dx * dt
        newY = projectile.y + projectile.dy * dt
        gridX, gridY = int(newX) // PLAYER_SIZE, int(newY) // PLAYER_SIZE # calc grid coords, similar to player mvmnt
        if not (BORDER_THICKNESS + projectile.radius <= projectile.x <= WIDTH - BORDER_THICKNESS - projectile.radius and
                BORDER_THICKNESS + projectile.radius <= projectile.y <= HEIGHT - BORDER_THICKNESS - projectile.radius):
            projectiles.remove(projectile)
        elif grid_colors[gridX][gridY] == HIGHLIGHT_COLOR:
            projectiles.remove(projectile)
        else:
            projectile.x, projectile.y = newX, newY
            pygame.draw.circle(window, PROJECTILE_COLOR, (int(projectile.x), int(projectile.y)), projectile.radius)
    

    #draw UI
    if change_grid_color:
        text_surface = STATUS_FONT.render('BUILDING', False, STATUS_FONT_COLOR)
    else:
        text_surface = STATUS_FONT.render('SHOOTING', False, STATUS_FONT_COLOR)  
    window.blit(text_surface, (WIDTH - text_surface.get_width() * 1.1, HEIGHT - text_surface.get_height() * 1.1 )) #add text_surface on window surface
    
    pygame.display.update()


pygame.quit()
