
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 17:52:25 2023

@author: radek
"""

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
import pygame
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtCore import pyqtSignal
import chess
import berserk

N=None

class ChessboardWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.board = chess.Board()
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 400, 400
        self.square_size = self.SCREEN_WIDTH // 8
        self.selected_square = None  # Add this line to define the selected_square attribute
        self.target_square = None
        self.error_highlight_color = Qt.red  # Domyślny kolor zaznaczania błędu
        self.highlighted_squares = []
        self.highlighted_squares2=[]
        self.piece_images = {
           'P': pygame.image.load('graph/wP.png'),  # White pawn
           'N': pygame.image.load('graph/wN.png'),  # White knight
           'B': pygame.image.load('graph/wB.png'),  # White bishop
           'R': pygame.image.load('graph/wR.png'),  # White rook
           'Q': pygame.image.load('graph/wQ.png'),  # White queen
           'K': pygame.image.load('graph/wK.png'),  # White king
           'p': pygame.image.load('graph/bP.png'),  # Black pawn
           'n': pygame.image.load('graph/bN.png'),  # Black knight
           'b': pygame.image.load('graph/bB.png'),  # Black bishop
           'r': pygame.image.load('graph/bR.png'),  # Black rook
           'q': pygame.image.load('graph/bQ.png'),  # Black queen
           'k': pygame.image.load('graph/bK.png'),  # Black king
           }


    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        self.draw_chessboard(qp)
        qp.end()
    
        qp = QtGui.QPainter(self)
        self.draw_pieces(qp)
        qp.end()
    
        qp = QtGui.QPainter(self)
        self.draw_moves(qp)
        qp.end()
    
        qp = QtGui.QPainter(self)
        self.draw_error_highlight(qp)
        qp.end()
        qp = QtGui.QPainter(self)
        self.draw_error_highlight2(qp)
        qp.end()
    #rysowanie
    def algebraic_to_coordinates(self, algebraic_notation):
        """
        Konwertuje notację szachową (np. 'e2e4') na indeksy kolumny i wiersza (np. (4, 6)).

        :param algebraic_notation: Notacja szachowa ruchu.
        :return: Krotka (kolumna, wiersz).
        """
        col_mapping = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        row1 = 8 - int(algebraic_notation[1])
        
        col1 = col_mapping[algebraic_notation[0]]
        row2 = 8 - int(algebraic_notation[3])
        
        col2= col_mapping[algebraic_notation[2]]
        #print(row1, col1,row2,col2)
        return row1, col1,row2,col2
    def highlight_error_algebraic(self, algebraic_notation):
        coordinates = self.algebraic_to_coordinates(algebraic_notation)
    
        #print(coordinates)
        if coordinates:
            row1, col1,row2,col2 = coordinates
            self.highlighted_squares.append((col1, row1))
            self.highlighted_squares.append((col2, row2))
            self.update()  # Ponowne rysowanie szachownicy
    def highlight_error_algebraic2(self, algebraic_notation):
        coordinates = self.algebraic_to_coordinates(algebraic_notation)
    
        #print(coordinates)
        if coordinates:
            row1, col1,row2,col2 = coordinates
            self.highlighted_squares2.append((col1, row1))
            self.highlighted_squares2.append((col2, row2))
            self.update()  # Ponowne rysowanie szachownicy
            
          
    def draw_error_highlight(self, qp):
        # Rysuj zaznaczenie błędu
        if self.highlighted_squares:
            for i in self.highlighted_squares:
                col, row = i
                #print(col, row)
                x, y = col * self.square_size, row * self.square_size
                #self.error_highlight_color.setAlpha(127)
                qp.fillRect(x, y, self.square_size, self.square_size,QtGui.QColor(255, 0, 0, 127))

    def draw_error_highlight2(self, qp):
        # Rysuj zaznaczenie błędu
        if self.highlighted_squares2:
            for i in self.highlighted_squares2:
                col, row = i
                #print(col, row)
                x, y = col * self.square_size, row * self.square_size
                #self.error_highlight_color.setAlpha(127)
                qp.fillRect(x, y, self.square_size, self.square_size,QtGui.QColor(0, 0, 255, 127))        
    def move_to_algebraic(self, move):
        """
        Konwertuje obiekt Move na notację szachową (np. 'e2e4').
        
        :param move: Obiekt Move.
        :return: Notacja szachowa ruchu.
        """
        from_square = chess.square_name(move.from_square)
        to_square = chess.square_name(move.to_square)
        return f"{from_square}{to_square}"
    
    #ustawianie szachownicy
    def set_board(self, fen):
        self.board = chess.Board(fen)
        self.update()
    def draw_chessboard(self, qp):
        LIGHT_SQUARE = (181, 136, 99)  # Light square color
        DARK_SQUARE = (240, 217, 181)   # Dark square color

        for row in range(8):
            for col in range(8):
                color = LIGHT_SQUARE if (row + col) % 2 == 0 else DARK_SQUARE
                x, y = col * self.square_size, (7 - row) * self.square_size  # Reverse the row calculation
                qp.fillRect(x, y, self.square_size, self.square_size, QtGui.QColor(*color))

    def draw_pieces(self, qp):
        for row in range(8):
            for col in range(8):
                piece = self.board.piece_at(8 * (7 - row) + col)  # Reverse the row calculation
                if piece is not None:
                    piece_img = self.piece_images[piece.symbol()]
                    x, y = col * self.square_size, row * self.square_size
                    piece_img = pygame.transform.scale(piece_img, (self.square_size, self.square_size))
                    image_data = pygame.image.tostring(piece_img, 'RGBA')
                    img_qt = QtGui.QImage(image_data, self.square_size, self.square_size, QtGui.QImage.Format_ARGB32)
                    pixmap = QtGui.QPixmap.fromImage(img_qt)
                    qp.drawPixmap(x, y, pixmap)
    def draw_moves(self, qp):
        # Draw arrows to indicate moves
        if self.selected_square is not None and self.target_square is not None:
            selected_col, selected_row = chess.square_file(self.selected_square), 7 - chess.square_rank(self.selected_square)
            target_col, target_row = chess.square_file(self.target_square), 7 - chess.square_rank(self.target_square)

            # Calculate the coordinates of the centers of the selected and target squares
            #selected_x, selected_y = selected_col * self.square_size + self.square_size // 2, selected_row * self.square_size + self.square_size // 2
            #target_x, target_y = target_col * self.square_size + self.square_size // 2, target_row * self.square_size + self.square_size // 2

            # Draw an arrow from the selected square to the target square
            #qp.setPen(QtGui.QPen(Qt.blue, 2, Qt.SolidLine))
            #qp.drawLine(selected_x, selected_y, target_x, target_y)
     
        
    def mousePressEvent(self, event):
        col, row = event.x() // self.square_size, 7 - event.y() // self.square_size
        square = chess.square(col, row)

        if self.selected_square is None:
            # Select a piece if the square contains one
            piece = self.board.piece_at(square)
            if piece is not None:
                self.selected_square = square
        else:
            # Try to make a move
            move = chess.Move(self.selected_square, square)
            if move in self.board.legal_moves:
                self.target_square = square
                self.board.push(move)
            else:
                self.selected_square = None

        self.update()  # Trigger a repaint to update the display

class MyWindow(QMainWindow):
    content_changed = pyqtSignal(str)  # Define a custom signal
    def __init__(self,  parent=None):
        super(MyWindow, self).__init__(parent)
        #SCREEN_WIDTH, SCREEN_HEIGHT = surface.get_width(), surface.get_height()
        self.setWindowTitle("Praca")
        self.setGeometry(100, 100, 420, 550)

        #self.data = surface.get_buffer().raw
        #self.image = QtGui.QImage(self.data, SCREEN_HEIGHT, SCREEN_WIDTH, QtGui.QImage.Format_RGB32)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.text_field = QTextEdit()
        self.text_field.setFixedSize(250, 50)
        layout.addWidget(self.text_field)

        self.button_change = QPushButton('enter',clicked=self.return_text)
        #self.button_change.clicked.connect(self.return_text)
        self.button_change.setFixedSize(200, 50)
        layout.addWidget(self.button_change)

        self.chessboard_widget = ChessboardWidget()
        layout.addWidget(self.chessboard_widget)

        self.current_central_widget = QWidget()
        self.current_central_widget.setLayout(layout)

        self.setCentralWidget(self.current_central_widget)

    def return_text(self):
        content = self.text_field.toPlainText()
        global N
        
        self.content_changed.emit(content)
        self.chessboard_widget.highlighted_squares=[]
        self.chessboard_widget.highlighted_squares2=[]
        self.update()
        
        #games=client.games.export_by_player(content,evals=False,perf_type="rapid",clocks=False,analysed=True)
        #to zajmuje dużo czasu 
        #games1 = list(games)
        from szachy import checkmiss
        #print(content)
        game_id=checkmiss(content)
        #print(game_id)
        N=game_id
        #fen_result=game_id[0][0]
        if game_id:
            #print("jestem")
            fen_result=game_id[0][0]
            
        if fen_result:
            # Ustaw planszę w widżecie szachowym na podstawie FEN
            self.chessboard_widget.set_board(fen_result)
            self.chessboard_widget.highlight_error_algebraic(self.chessboard_widget.move_to_algebraic(game_id[0][1]))
            self.chessboard_widget.highlight_error_algebraic2(self.chessboard_widget.move_to_algebraic(game_id[0][2]))
        else:
            #print(fen_result)
            self.chessboard_widget.set_board(chess.STARTING_FEN)
        #return client.games.export(game_id,as_pgn=True)
        return game_id
        
        

    # def paintEvent(self, event):
    #     qp = QtGui.QPainter()
    #     qp.begin(self)
    #     qp.drawImage(100, 40, self.image)
    #     qp.end()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()

    # Create a list to store connections

    try:
        sys.exit(app.exec_())
    except SystemExit:
        G=window.return_text()
        
