import pygame
import chess

pygame.init()

# Define screen dimensions and colors
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_SQUARE = (240, 217, 181)  # Light square color
DARK_SQUARE = (181, 136, 99)   # Dark square color

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Chessboard")

# Load chess piece images
piece_images = {
    'P': pygame.image.load('graph/wP.png'),
    'N': pygame.image.load('graph/wN.png'),
    'B': pygame.image.load('graph/wB.png'),
    'R': pygame.image.load('graph/wR.png'),
    'Q': pygame.image.load('graph/wQ.png'),
    'K': pygame.image.load('graph/wK.png'),
    'p': pygame.image.load('graph/bP.png'),
    'n': pygame.image.load('graph/bN.png'),
    'b': pygame.image.load('graph/bB.png'),
    'r': pygame.image.load('graph/bR.png'),
    'q': pygame.image.load('graph/bQ.png'),
    'k': pygame.image.load('graph/bK.png'),
}

def scale_piece_images():
    for piece in piece_images:
        piece_images[piece] = pygame.transform.scale(piece_images[piece], (SCREEN_WIDTH // 8, SCREEN_HEIGHT // 8))

def draw_chessboard():
    for row in range(8):
        for col in range(8):
            color = LIGHT_SQUARE if (row + col) % 2 == 0 else DARK_SQUARE
            pygame.draw.rect(screen, color, pygame.Rect(col * SCREEN_WIDTH // 8, (7 - row) * SCREEN_HEIGHT // 8, SCREEN_WIDTH // 8, SCREEN_HEIGHT // 8))

def draw_pieces(board):
    for row in range(8):
        for col in range(8):
            piece = board.piece_at(8 * row + col)
            if piece is not None:
                piece_img = piece_images[piece.symbol()]
                screen.blit(piece_img, pygame.Rect(col * SCREEN_WIDTH // 8, (7 - row) * SCREEN_HEIGHT // 8, SCREEN_WIDTH // 8, SCREEN_HEIGHT // 8))


def get_square_from_mouse(pos):
    x, y = pos
    col = x // (SCREEN_WIDTH // 8)
    row = y // (SCREEN_HEIGHT // 8)
    return chess.square(col, 7 - row)  # Invert the row to match chess notation

def main():
    scale_piece_images()

    running = True
    board = chess.Board()

    selected_square = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    square = get_square_from_mouse(event.pos)
                    piece = board.piece_at(square)

                    if selected_square is None and piece is not None:
                        selected_square = square
                    elif selected_square is not None:
                        move = chess.Move(selected_square, square)

                        if move in board.legal_moves:
                            board.push(move)
                        selected_square = None

        draw_chessboard()
        draw_pieces(board)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
