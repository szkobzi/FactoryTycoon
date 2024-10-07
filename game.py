import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 750
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (30, 30, 30)
DARK_BACKGROUND = (40, 40, 40)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER_COLOR = (100, 150, 200)
BUTTON_CLICK_COLOR = (50, 100, 160)
FONT_SIZE = 30
LARGE_FONT_SIZE = 50
MIDDLE_FONT_SIZE = 32
CARD_BACKGROUND = (240, 240, 240)
CARD_SHADOW_COLOR = (180, 180, 180)
ACHIEVEMENT_BACKGROUND = (60, 60, 60)
ACHIEVEMENT_MENU_WIDTH = 400
ACHIEVEMENT_MENU_HEIGHT = 400

# Income Animation Class
class IncomeAnimation:
    def __init__(self, amount, position):
        self.amount = amount
        self.position = list(position)
        self.alpha = 255
        self.timer = 60  # Display for 60 frames (~1 second at 60 FPS)

    def update(self):
        self.position[1] -= 1  # Move up
        self.alpha -= 4  # Fade out
        self.timer -= 1

    def is_done(self):
        return self.timer <= 0

# Business class
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

# Game variables
money = 0
prestige_points = 0
income_multiplier = 1.0
upgrade_animation = []
income_animations = []  # List to store income animations
current_event = None
event_duration = 0
bonus_active = False
bonus_duration = 0
error_message = ""
error_message_timer = 0

# Initialize businesses
def initialize_businesses():
    return [
        Business("Café", 50, 2, level=1),
        Business("Bakery", 100, 3),
        Business("Restaurant", 200, 5),
        Business("Clothing Store", 300, 7),
        Business("Tech Startup", 500, 10),
        Business("Real Estate", 1000, 20)
    ]

businesses = initialize_businesses()

# New businesses for the second stage
def initialize_new_businesses():
    return [
        Business("Luxury Hotel", 5000, 50, level=1),
        Business("Private Jet Service", 10000, 100),
        Business("Mega Mall", 20000, 200),
        Business("High-Tech Factory", 50000, 500),
        Business("Space Tourism", 100000, 1000),
        Business("Crypto Mining Farm", 200000, 2000)
    ]

# Achievements tracking
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
        achievements.append("Rebirthed")
        achievements_reached.add("Rebirthed")
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
    global money, prestige_points, income_multiplier, businesses
    if all(b.level == 10 for b in businesses):
        prestige_points += 1
        income_multiplier *= 1.002
        money = 0
        businesses = initialize_new_businesses()  # Switch to new businesses

# Random event and bonus functions
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

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tycoon Game")

# Load fonts
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
    draw_text(f"{business.name}", middle_font, BLACK, screen, x + 120, y + 30)
    draw_text(f"Level: {business.level}", font, BLACK, screen, x + 120, y + 70)
    draw_text(f"Income: ${int(business.income())}/s", font, BLACK, screen, x + 120, y + 100)
    draw_text(f"Upgrade Cost: ${int(business.upgrade_cost)}", font, BLACK, screen, x + 120, y + 130)

def animate_upgrade():
    upgrade_animation.append({"pos": [SCREEN_WIDTH // 2 + 150, 40], "alpha": 255})

# Splash Screen Function
def splash_screen():
    fade_in_duration = 0  # Duration for fade-in (seconds)
    fade_out_duration = 2  # Duration for fade-out (seconds)
    fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade_surface.fill(BLACK)

    # Splash screen loop
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Draw the splash screen
        screen.fill(DARK_BACKGROUND)
        draw_text("Factory Tycoon", large_font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        draw_text("Created by: Scopsy", middle_font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40)

        # Handle fade-in effect
        if fade_in_duration > 0:
            alpha = int((1 - (fade_in_duration / 2)) * 255)
            fade_surface.set_alpha(alpha)
            screen.blit(fade_surface, (0, 0))
            fade_in_duration -= clock.get_time() / 1000  # Update duration
        else:
            # Fade out effect
            fade_out_alpha = min(255, (fade_out_duration / 2) * 255)
            fade_surface.set_alpha(fade_out_alpha)
            screen.blit(fade_surface, (0, 0))
            fade_out_duration -= clock.get_time() / 1000  # Update duration

        if fade_out_duration <= 0:
            running = False

        pygame.display.flip()
        clock.tick(60)

# Main Game Loop
clock = pygame.time.Clock()
income_generation_interval = 60  # 1 income every 60 frames
frames_since_last_income = 0  # Counter for income generation
frames_since_last_event = 0
frames_since_last_bonus = 0
show_achievements = False

# Run splash screen
splash_screen()

while True:
    screen.fill(DARK_BACKGROUND)
    mouse_pos = pygame.mouse.get_pos()
    mouse_clicked = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_clicked = True

    # Income generation
    income_multiplier_effect = 1.0
    if current_event == "Market Boom":
        income_multiplier_effect = 1.5
    elif current_event == "Market Crash":
        income_multiplier_effect = 0.7

    # Accumulate income over time
    income = sum(b.income() for b in businesses) * income_multiplier_effect
    frames_since_last_income += 1  # Increment the frame counter

    if frames_since_last_income >= income_generation_interval:
        money += income
        # Create an income animation
        income_animations.append(IncomeAnimation(income, (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)))
        frames_since_last_income = 0  # Reset the counter

    # Update income animations
    for anim in income_animations[:]:
        anim.update()
        if anim.is_done():
            income_animations.remove(anim)

    for anim in upgrade_animation[:]:
        anim["pos"][1] -= 1
        anim["alpha"] -= 5
        if anim["alpha"] <= 0:
            upgrade_animation.remove(anim)

    check_achievements()

    draw_text(f"Money: ${int(money)}", large_font, WHITE, screen, SCREEN_WIDTH // 2, 40)

    # Draw income animations
    for anim in income_animations:
        draw_text(f"+${int(anim.amount)}", large_font, (0, 255, 0), screen, anim.position[0], anim.position[1])

    for anim in upgrade_animation:
        draw_text("Upgrade bought!", large_font, (0, 255, 0), screen, anim["pos"][0], anim["pos"][1])

    draw_text(f"Rebirths: {prestige_points}", font, WHITE, screen, SCREEN_WIDTH // 2, 80)

    if current_event:
        draw_text(current_event, font, (255, 0, 0), screen, SCREEN_WIDTH // 2, 650)

    num_columns = 3  # Number of cards per row
    card_height = 200  # Height of each card
    spacing = 60  # Increased spacing between rows to avoid overlap

    for i, business in enumerate(businesses):
        col = i % num_columns
        row = i // num_columns
        x_offset = 20 + col * 260  # X position for business card
        y_offset = 100 + row * (card_height + spacing)  # Y position for business card

        # Drawing business card
        draw_business_card(business, x_offset, y_offset)

        # Determine button text based on business level
        button_text = "Buy" if business.level == 0 else "Upgrade"

        # Adjusting the button position based on row and column
        upgrade_button = draw_button(button_text, x_offset + 50, y_offset + card_height + 10, 140, 40)

        if upgrade_button.collidepoint(mouse_pos):
            draw_button(button_text, x_offset + 50, y_offset + card_height + 10, 140, 40, BUTTON_HOVER_COLOR)

        # Handle button click for buying or upgrading
        if mouse_clicked and upgrade_button.collidepoint(mouse_pos):
            if business.level == 0 and money >= business.base_cost:  # Check if buying
                money -= business.base_cost
                business.level = 1  # Set level to 1 after purchase
                business.upgrade_cost = business.calculate_upgrade_cost()  # Update the upgrade cost
                error_message = ""  # Clear error message if purchase is successful
            elif business.level >= 1:
                if money >= business.upgrade_cost:  # Check if upgrading
                    money -= business.upgrade_cost
                    business.upgrade()
                    animate_upgrade()
                    error_message = ""  # Clear error message if the upgrade is successful
                else:
                    error_message = "You don't have enough money!"  # Set error message if not enough money
                    error_message_timer = 120  # Start the timer (assuming 60 FPS, 2 seconds)

    # Update the error message timer
    if error_message_timer > 0:
        error_message_timer -= 1  # Decrement timer

    # Achievements button on the left
    achievements_button = draw_button("Achievements", 20, SCREEN_HEIGHT - 100, 150, 40)
    if achievements_button.collidepoint(mouse_pos):
        draw_button("Achievements", 20, SCREEN_HEIGHT - 100, 150, 40, BUTTON_HOVER_COLOR)

    if mouse_clicked and achievements_button.collidepoint(mouse_pos):
        show_achievements = not show_achievements

    # Prestige button on the right
    prestige_button = draw_button("Prestige", SCREEN_WIDTH - 150, SCREEN_HEIGHT - 100, 120, 40)
    if prestige_button.collidepoint(mouse_pos):
        draw_button("Prestige", SCREEN_WIDTH - 150, SCREEN_HEIGHT - 100, 120, 40, BUTTON_HOVER_COLOR)

    if mouse_clicked and prestige_button.collidepoint(mouse_pos):
        reset_for_prestige()

    frames_since_last_event = 0
    frames_since_last_bonus = 0
    if frames_since_last_event >= 600:
        trigger_random_event()
        frames_since_last_event = 0
    if frames_since_last_bonus >= 1200:
        trigger_random_bonus()
        frames_since_last_bonus = 0

    if bonus_active:
        bonus_duration -= 1
        if bonus_duration <= 0:
            bonus_active = False

    # Display achievements menu if toggled
    if show_achievements:
        achievement_rect = pygame.Rect((SCREEN_WIDTH - ACHIEVEMENT_MENU_WIDTH) // 2,
                                       (SCREEN_HEIGHT - ACHIEVEMENT_MENU_HEIGHT) // 2, ACHIEVEMENT_MENU_WIDTH,
                                       ACHIEVEMENT_MENU_HEIGHT)
        pygame.draw.rect(screen, ACHIEVEMENT_BACKGROUND, achievement_rect)
        draw_text("Achievements", large_font, WHITE, screen, SCREEN_WIDTH // 2,
                  SCREEN_HEIGHT // 2 - ACHIEVEMENT_MENU_HEIGHT // 2 + 30)

        # Draw the close button (X) in the top-right corner
        close_button_rect = pygame.Rect(achievement_rect.right - 40, achievement_rect.top + 10, 30, 30)
        pygame.draw.rect(screen, BLACK, close_button_rect)
        draw_text("X", font, RED, screen, close_button_rect.centerx, close_button_rect.centery)

        for idx, achievement in enumerate(achievements):
            draw_text(achievement, font, WHITE, screen, SCREEN_WIDTH // 2,
                      SCREEN_HEIGHT // 2 - ACHIEVEMENT_MENU_HEIGHT // 2 + 70 + idx * 30)

        # Check for close button click
        if mouse_clicked and close_button_rect.collidepoint(mouse_pos):
            show_achievements = False

    # Draw the error message if it exists and the timer hasn't expired
    if error_message and error_message_timer > 0:
        draw_text(error_message, font, (255, 0, 0), screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)

    pygame.display.flip()
    clock.tick(60)
