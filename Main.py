import string

from BacktrackingSearch import BacktrackingSearch
from MinConflicts import MinConflicts
from utils import *

def draw_start_button(button_rect, label: string):
    pygame.draw.rect(display, colors["BLACK"], button_rect, 3, 3)
    font = pygame.font.Font(None, 25)
    text = font.render(label, True, colors["BLACK"])
    text_rect = text.get_rect(center=button_rect.center)
    display.blit(text, text_rect)


def draw_reset_button(button_rect):
    pygame.draw.rect(display, colors["BLACK"], button_rect, 3, 3)
    font = pygame.font.Font(None, 25)
    text = font.render("reset", True, colors["BLACK"])
    text_rect = text.get_rect(center=button_rect.center)
    display.blit(text, text_rect)


def main():
    display.fill(colors["GRAY"])
    running = True
    clock = pygame.time.Clock()

    # empty board
    board = [[0 for _ in range(n)] for _ in range(n)] #board to place queens on
    constraints_board = [[0 for _ in range(n)] for _ in range(n)] #board to show locked cells

    #start button
    start_minconflicts_button_rect = pygame.Rect(20, 50, 200, 40)
    start_backtracking_search_button_rect = pygame.Rect(20, 110, 200, 40)
    reset_button_rect = pygame.Rect(20, 170, 200, 40)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_minconflicts_button_rect.collidepoint(event.pos):
                    algorithm = MinConflicts(board, constraints_board, n, display, max_steps)
                    res = algorithm.solve()
                    if res is None: print("The algorithm stopped without being able to solve the CSP.")
                if start_backtracking_search_button_rect.collidepoint(event.pos):
                    algorithm = BacktrackingSearch(board, constraints_board, n, display)
                    res = algorithm.solve()
                    if not res: print("The algorithm stopped without being able to solve the CSP.")
                if reset_button_rect.collidepoint(event.pos): board, constraints_board = reset(display)

        display.fill(colors["GRAY"])
        draw_board(board, constraints_board, display)
        draw_start_button(start_minconflicts_button_rect, "minconflicts")
        draw_start_button(start_backtracking_search_button_rect, "backtracking search")
        draw_reset_button(reset_button_rect)
        pygame.display.flip()
        clock.tick(1)

pygame.init()
display = pygame.display.set_mode((900, 700))
main()