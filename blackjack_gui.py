import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blackjack")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
RED = (255, 0, 0)

# Card values
card_values = {
    'Ace': 11, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'Jack': 10, 'Queen': 10, 'King': 10
}

# Create a deck of cards
def create_deck():
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = list(card_values.keys())
    return [f"{rank} of {suit}" for suit in suits for rank in ranks]

# Calculate hand value
def hand_value(hand):
    value = sum(card_values[card.split()[0]] for card in hand)
    aces = sum(card.startswith('Ace') for card in hand)
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value

# Deal a card
def deal_card(deck):
    return deck.pop(random.randint(0, len(deck) - 1))

# Draw text
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

# Button class
class Button:
    def __init__(self, x, y, width, height, text, color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.Font(None, 32)
        text_surf = font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Game state
class GameState:
    def __init__(self):
        self.balance = 1000
        self.bet = 0
        self.deck = create_deck()
        self.player_hand = []
        self.dealer_hand = []
        self.game_over = False
        self.message = ""

    def start_new_round(self):
        self.deck = create_deck()
        self.player_hand = [deal_card(self.deck), deal_card(self.deck)]
        self.dealer_hand = [deal_card(self.deck), deal_card(self.deck)]
        self.game_over = False
        self.message = ""

    def hit(self):
        self.player_hand.append(deal_card(self.deck))
        if hand_value(self.player_hand) > 21:
            self.game_over = True
            self.balance -= self.bet
            self.message = f"You bust! You lose ${self.bet}"

    def stand(self):
        while hand_value(self.dealer_hand) < 17:
            self.dealer_hand.append(deal_card(self.deck))
        
        player_value = hand_value(self.player_hand)
        dealer_value = hand_value(self.dealer_hand)

        if dealer_value > 21:
            self.balance += self.bet
            self.message = f"Dealer busts! You win ${self.bet}"
        elif dealer_value > player_value:
            self.balance -= self.bet
            self.message = f"Dealer wins! You lose ${self.bet}"
        elif dealer_value < player_value:
            self.balance += self.bet
            self.message = f"You win ${self.bet}!"
        else:
            self.message = "It's a tie!"
        
        self.game_over = True

# Create buttons
hit_button = Button(300, 500, 100, 50, "Hit", GREEN, WHITE)
stand_button = Button(450, 500, 100, 50, "Stand", RED, WHITE)
new_game_button = Button(350, 500, 150, 50, "New Game", BLACK, WHITE)

# Create game state
game_state = GameState()

# Main game loop
running = True
betting = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if betting:
                if event.button == 1:  # Left click
                    game_state.bet += 10
                elif event.button == 3:  # Right click
                    game_state.bet = max(0, game_state.bet - 10)
                if game_state.bet > 0 and game_state.bet <= game_state.balance:
                    betting = False
                    game_state.start_new_round()
            elif not game_state.game_over:
                if hit_button.is_clicked(event.pos):
                    game_state.hit()
                elif stand_button.is_clicked(event.pos):
                    game_state.stand()
            else:
                if new_game_button.is_clicked(event.pos):
                    betting = True
                    game_state.bet = 0

    # Clear the screen
    screen.fill(GREEN)

    # Draw game state
    font = pygame.font.Font(None, 36)
    draw_text(f"Balance: ${game_state.balance}", font, WHITE, WIDTH // 2, 30)

    if betting:
        draw_text(f"Current Bet: ${game_state.bet}", font, WHITE, WIDTH // 2, HEIGHT // 2)
        draw_text("Left click to increase bet, Right click to decrease", font, WHITE, WIDTH // 2, HEIGHT // 2 + 50)
    else:
        draw_text(f"Player Hand: {', '.join(game_state.player_hand)} (Value: {hand_value(game_state.player_hand)})", font, WHITE, WIDTH // 2, 100)
        if game_state.game_over:
            draw_text(f"Dealer Hand: {', '.join(game_state.dealer_hand)} (Value: {hand_value(game_state.dealer_hand)})", font, WHITE, WIDTH // 2, 200)
        else:
            draw_text(f"Dealer Hand: {game_state.dealer_hand[0]}, Hidden", font, WHITE, WIDTH // 2, 200)
        
        draw_text(game_state.message, font, WHITE, WIDTH // 2, 300)

        if not game_state.game_over:
            hit_button.draw()
            stand_button.draw()
        else:
            new_game_button.draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()