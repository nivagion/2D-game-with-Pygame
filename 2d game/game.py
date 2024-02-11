import pygame

pygame.init()

WIDTH, HEIGHT = 900, 600
BORDER_THICKNESS = 30
PLAYER_SIZE = 30
PLAYER_SPEED = 200 #in pixels per seconds because of delta time
GRID_COLOR = (200, 200, 200) #light grey color
HIGHLIGHT_COLOR = (200, 230, 200) # v
BACKGROUND_COLOR = (255, 255, 255)
BORDER_COLOR = (0, 0, 0)

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

running = True
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            gridX, gridY = mouse_pos[0] // PLAYER_SIZE, mouse_pos[1] // PLAYER_SIZE #calc grid coords
            if grid_colors[gridX][gridY] != HIGHLIGHT_COLOR:
                grid_colors[gridX][gridY] = HIGHLIGHT_COLOR
            else: 
                grid_colors[gridX][gridY] = BACKGROUND_COLOR
            
        
    dt = clock.tick(60) / 1000 #limits it to 60fps, returns ms so i divide it by 1000 to return seconds

    
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
    

    #DRAWING
    window.fill(BACKGROUND_COLOR) #RGB> white
    
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
    
    pygame.display.update()


pygame.quit()