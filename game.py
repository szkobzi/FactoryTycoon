import pygame
import sys
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 750
WHITE = (255, 255, 255)
BLACK = (30, 30, 30)
LIGHT_GRAY = (220, 220, 220)
DARK_BACKGROUND = (40, 40, 40)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER_COLOR = (100, 150, 200)
BUTTON_CLICK_COLOR = (50, 100, 160)
FONT_SIZE = 30
LARGE_FONT_SIZE = 50
MIDDLE_FONT_SIZE = 18
CARD_BACKGROUND = (240, 240, 240)
CARD_SHADOW_COLOR = (180, 180, 180)
ACHIEVEMENT_BACKGROUND = (60, 60, 60)
ACHIEVEMENT_MENU_WIDTH = 400
ACHIEVEMENT_MENU_HEIGHT = 400

class Business:
    def __init__(self, name, base_cost, base_income, level=0):
        self.name = name
        self.level = level
        self.base_cost = base_cost
        self.base_income = base_income
        self.upgrade_cost = self.calculate_upgrade_cost()

    def calculate_upgrade_cost(self):
        return self.base_cost * (1.5 ** self.level)

    def upgrade(self):
        if self.level < 10:
            self.level += 1
            self.upgrade_cost = self.calculate_upgrade_cost()
            self.base_income *= 1.5

    def income(self):
        return self.base_income * (1.2 ** self.level) if self.level > 0 else 0

money = 0
prestige_points = 0
income_multiplier = 1.0
upgrade_animation = []
current_event = None
event_duration = 0
bonus_active = False
bonus_duration = 0

businesses = [
    Business("Café", 50, 2, level=1),
    Business("Bakery", 100, 3),
    Business("Restaurant", 200, 5),
    Business("Clothing Store", 300, 7),
    Business("Tech Startup", 500, 10),
    Business("Real Estate", 1000, 20)
]

achievements = []
achievements_reached = set()

def check_achievements():
    global achievements_reached
    if money >= 100 and "Reached $100" not in achievements_reached:
        achievements.append("Reached $100")
        achievements_reached.add("Reached $100")
    if money >= 1000 and "Reached $1000" not in achievements_reached:
        achievements.append("Reached $1000")
        achievements_reached.add("Reached $1000")
    if all(b.level == 10 for b in businesses) and "Max Level All Businesses" not in achievements_reached:
        achievements.append("Max Level All Businesses")
        achievements_reached.add("Max Level All Businesses")
    if prestige_points > 0 and "Prestige Points Earned" not in achievements_reached:
        achievements.append("Prestige Points Earned")
        achievements_reached.add("Prestige Points Earned")
    if money >= 5000 and "Reached $5000" not in achievements_reached:
        achievements.append("Reached $5000")
        achievements_reached.add("Reached $5000")
    if any(b.level == 10 for b in businesses) and "One Business at Max Level" not in achievements_reached:
        achievements.append("One Business at Max Level")
        achievements_reached.add("One Business at Max Level")
    if len(achievements) > 5 and "Collector of Achievements" not in achievements_reached:
        achievements.append("Collector of Achievements")
        achievements_reached.add("Collector of Achievements")

def reset_for_prestige():
    global money, prestige_points, income_multiplier
    if all(b.level == 10 for b in businesses):
        prestige_points += 1
        income_multiplier *= 1.002
        money = 0
        for business in businesses:
            business.level = 1 if business.name == "Café" else 0
            business.upgrade_cost = business.calculate_upgrade_cost()

        money += businesses[0].income()  # Generate money from the Coffee Shop

def trigger_random_event():
    global current_event, event_duration
    event_type = random.choice(["Market Boom", "Market Crash"])
    if event_type == "Market Boom":
        current_event = "Market Boom: Income +50%!"
        event_duration = 300
    elif event_type == "Market Crash":
        current_event = "Market Crash: Income -30%!"
        event_duration = 300

def trigger_random_bonus():
    global bonus_active, bonus_duration
    bonus_active = True
    bonus_duration = 180

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tycoon Game")

font = pygame.font.Font(None, FONT_SIZE)
large_font = pygame.font.Font(None, LARGE_FONT_SIZE)
middle_font = pygame.font.Font(None, MIDDLE_FONT_SIZE)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)

def draw_button(text, x, y, width, height, color=BUTTON_COLOR):
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, color, button_rect, border_radius=15)
    pygame.draw.rect(screen, BLACK, button_rect, 2, border_radius=15)  # Border
    draw_text(text, font, WHITE, screen, x + width // 2, y + height // 2)
    return button_rect

def draw_business_card(business, x, y):
    card_rect = pygame.Rect(x, y, 240, 200)
    pygame.draw.rect(screen, CARD_BACKGROUND, card_rect, border_radius=15)
    pygame.draw.rect(screen, CARD_SHADOW_COLOR, card_rect.move(5, 5), border_radius=15)
    draw_text(f"{business.name}", large_font, BLACK, screen, x + 120, y + 30)
    draw_text(f"Level: {business.level}", font, BLACK, screen, x + 120, y + 70)
    draw_text(f"Income: ${int(business.income())}/s", font, BLACK, screen, x + 120, y + 100)
    draw_text(f"Upgrade Cost: ${int(business.upgrade_cost)}", font, BLACK, screen, x + 120, y + 130)

def animate_upgrade():
    upgrade_animation.append({"pos": [SCREEN_WIDTH // 2 + 150, 40], "alpha": 255})

def splash_screen():
    fade_in_duration = 2
    fade_out_duration = 1
    fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade_surface.fill(BLACK)

    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(DARK_BACKGROUND)
        draw_text("Factory Tycoon", large_font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        draw_text("Created by: Scopsy", middle_font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40)

        if fade_in_duration > 0:
            alpha = int((1 - (fade_in_duration / 2)) * 255)
            fade_surface.set_alpha(alpha)
            screen.blit(fade_surface, (0, 0))
            fade_in_duration -= clock.get_time() / 1000
        else:
            if fade_out_duration > 0:
                alpha = int((fade_out_duration / 1) * 255)
                fade_surface.set_alpha(alpha)
                screen.blit(fade_surface, (0, 0))
                fade_out_duration -= clock.get_time() / 1000
            else:
                running = False

        pygame.display.flip()
        clock.tick(60)

clock = pygame.time.Clock()
income_rate = 0.1
frames_since_last_event = 0
frames_since_last_bonus = 0
show_achievements = False

splash_screen()

while True:
    screen.fill(DARK_BACKGROUND)

    mouse_pos = pygame.mouse.get_pos()
    mouse_clicked = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_clicked = True

    income_multiplier_effect = 1.0
    if current_event == "Market Boom":
        income_multiplier_effect = 1.5
    elif current_event == "Market Crash":
        income_multiplier_effect = 0.7

    if bonus_active:
        income_multiplier_effect *= 1.2

    income = businesses[0].income() * income_multiplier_effect * income_rate
    money += income

    for anim in upgrade_animation[:]:
        anim["pos"][1] -= 1
        anim["alpha"] -= 5
        if anim["alpha"] <= 0:
            upgrade_animation.remove(anim)

    check_achievements()

    draw_text(f"Money: ${int(money)}", large_font, WHITE, screen, SCREEN_WIDTH // 2, 40)

    for anim in upgrade_animation:
        draw_text(f"Upgrade bought!", large_font, (255, 255, 0), screen, anim["pos"][0], anim["pos"][1])

    draw_text("Businesses:", font, WHITE, screen, SCREEN_WIDTH // 2, 100)

    x = SCREEN_WIDTH // 2 - 150
    y = 150
    for business in businesses:
        draw_business_card(business, x, y)
        x += 260  # Space between cards
        if x >= SCREEN_WIDTH - 100:  # Reset x to the beginning if it exceeds screen width
            x = SCREEN_WIDTH // 2 - 150
            y += 250  # Move down to the next row

    prestige_button_rect = draw_button("Prestige", 50, SCREEN_HEIGHT - 100, 200, 50)
    if prestige_button_rect.collidepoint(mouse_pos) and mouse_clicked:
        reset_for_prestige()

    random_event_button_rect = draw_button("Trigger Event", 300, SCREEN_HEIGHT - 100, 200, 50)
    if random_event_button_rect.collidepoint(mouse_pos) and mouse_clicked:
        trigger_random_event()

    random_bonus_button_rect = draw_button("Trigger Bonus", 550, SCREEN_HEIGHT - 100, 200, 50)
    if random_bonus_button_rect.collidepoint(mouse_pos) and mouse_clicked:
        trigger_random_bonus()

    if event_duration > 0:
        draw_text(current_event, font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40)
        event_duration -= 1

    if bonus_duration > 0:
        draw_text("Bonus active!", font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70)
        bonus_duration -= 1
        if bonus_duration <= 0:
            bonus_active = False

    pygame.display.flip()
    clock.tick(60)
