import numpy as np
from tkinter import Button
from my_classes import King, Queen, Rook, Knight, Bishop, Pawn

# Naming convention: First letter is the color, 2nd is piece, 3rd is a number
# to distinguish duplicates.
br1 = Rook('b')
br2 = Rook('b')
bn1 = Knight('b')
bn2 = Knight('b')
bb1 = Bishop('b')
bb2 = Bishop('b')
bq1 = Queen('b')
bk = King('b')
bp1 = Pawn('b')
bp2 = Pawn('b')
bp3 = Pawn('b')
bp4 = Pawn('b')
bp5 = Pawn('b')
bp6 = Pawn('b')
bp7 = Pawn('b')
bp8 = Pawn('b')

wr1 = Rook('w')
wr2 = Rook('w')
wn1 = Knight('w')
wn2 = Knight('w')
wb1 = Bishop('w')
wb2 = Bishop('w')
wq1 = Queen('w')
wk = King('w')
wp1 = Pawn('w')
wp2 = Pawn('w')
wp3 = Pawn('w')
wp4 = Pawn('w')
wp5 = Pawn('w')
wp6 = Pawn('w')
wp7 = Pawn('w')
wp8 = Pawn('w')

# Board for initializing the game
start_board = np.array([[br1, bn1, bb1, bq1, bk,bb2,bn2,br2],
                        [bp1, bp2,bp3,bp4,bp5,bp6,bp7,bp8],
                        [0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0],
                        [wp1,wp2,wp3,wp4,wp5,wp6,wp7,wp8],
                        [wr1,wn1,wb1,wq1,wk,wb2,wn2,wr2]])

# Board used for resetting the game. Can be made into separate boards for tests.
reset_board = np.array([[br1, bn1, bb1, bq1, bk,bb2,bn2,br2],
                        [bp1, bp2,bp3,bp4,bp5,bp6,bp7,bp8],
                        [0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0],
                        [wp1,wp2,wp3,wp4,wp5,wp6,wp7,wp8],
                        [wr1,wn1,wb1,wq1,wk,wb2,wn2,wr2]])

# The following boards were used for testing.
queen_board = np.array([[0,0,0,bq1,0,0,bp1,bk],
                        [0,0,0,0,0,0,bp2,bp3],
                        [0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,wq1,0,0],
                        [0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,wp2,wp3],
                        [0,0,0,0,0,0,wp1,wk]])

stale_board = np.array([[0,bq1, br2,0,0,0,0,bk],
                        [0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,br1],
                        [0,wk,0,0,0,0,0,0]])

pawn_promo_board = np.array([[0,0,0,0,0,0,0,0],
                             [wp2,wp1,wp2,wp4,0,0,0,bk],
                             [0,0,0,0,0,0,0,0],
                             [0,0,0,0,0,0,0,0],
                             [0,0,0,0,0,0,0,0],
                             [0,0,0,0,0,0,0,0],
                             [wk,0,0,0,bp4,bp3,bp2,bp1],
                             [0,0,0,0,0,0,0,0]])

castle_check_board = np.array([[br1,0,0,0,bk,0,0,br2],
                             [0,0,0,0,0,0,0,0],
                             [0,0,0,0,0,0,0,0],
                             [0,0,0,0,0,0,0,0],
                             [0,0,0,0,0,0,0,0],
                             [0,0,0,0,0,0,0,0],
                             [0,0,0,0,0,0,0,0],
                             [wr1,0,0,0,wk,0,0,wr2]])

en_passant_board = np.array([[0,0,0,0,bk,0,0,0],
                             [bp1,0,bp3,0,bp5,0,bp7,0],
                             [0,0,0,0,0,0,0,0],
                             [0,wp2,0,wp4,0,wp6,0,wp8],
                             [0,bp2,0,bp4,0,bp6,0,bp8],
                             [0,0,0,0,0,0,0,0],
                             [wp1,0,wp3,0,wp5,0,wp7,0],
                             [0,0,0,0,wk,0,0,0]])

test_list = [[queen_board, 'w', "White's turn | Test board for queen movement"],
               [stale_board, 'w', "White's turn | Test board for checkmate and stalemate"],
               [pawn_promo_board,'w', "White's turn | Test board for pawn promotion"],
               [castle_check_board, 'w', "White's turn | Test board for castling"],
               [en_passant_board, 'w', "White's turn | Test board for En passant"]]

gutman = np.array([[br1,bn1,0,bq1,0,br2,0,bk],
                  [0,0,bp3,bp4,0,0,0,0],
                  [0,0,0,0,0,bp6,wq1,0],
                  [0,bb1,0,wp4,wb1,0,0,0],
                  [0,0,0,0,0,0,0,0],
                  [0,0,0,0,wp5,0,0,0],
                  [wp1,wp2,0,wk,0,wp6,0,wp8],
                  [wr1,0,0,0,0,0,0,0]])

# Critical game positions from professional games
kasparov = np.array([[br1,0,bq1,0,0,br2,bk,0],
                    [wp1,wb1,0,0,bb2,bp6,bp7,bp8],
                    [0,bp2,bp3,0,bp5,bn1,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,wp3,wp4,0,0,0,0],
                    [0,0,0,0,0,wn1,wp7,0],
                    [wp1,wp2,wq1,0,0,wp6,wb2,wp8],
                    [wr1,0,wb1,wr2,0,0,wk,0]])

sagar13 = np.array([[0,br1,0,bq1,0,br2,bk,0],
                   [0,0,0,0,bp4,bp5,bb2,bp8],
                   [bp1,0,bp3,bp4,0,bn2,bp7,0],
                   [bn1,0,0,0,0,0,0,0],
                   [0,0,wp3,0,0,wb1,bb1,0],
                   [0,wp2,wn1,0,0,wn2,wp7,0],
                   [wp1,0,0,0,wp5,wp6,wb2,wp8],
                   [0,0,wb1,wq1,0,wr2,wk,0]])

anand = np.array([[0,0,bb1,bq1,bn1,bb1,bk,0],
                 [0,0,0,0,0,bp3,0,bp1],
                 [0,0,0,0,0,wp3,bp2,wq1],
                 [0,0,0,bp5,wp4,0,wp2,0],
                 [0,0,bp6,wp5,0,0,0,0],
                 [0,bp7,wp6,0,0,0,wn1,0],
                 [0,0,0,0,0,0,wb1,wp1],
                 [0,0,0,0,0,wr1,wk,0]])

sagar12 = np.array([[br1,bn1,bb1,0,br2,bb2,bk,0],
                   [0,bp2,bq1,0,0,bp6,bp7,bp8],
                   [0,0,bp3,bp4,0,bn2,0,0],
                   [bp1,0,0,0,bp5,0,0,0],
                   [wp1,0,wp4,wp5,wp6,0,0,0],
                   [0,0,wn1,0,wb1,wn2,wp7,wp8],
                   [0,wp2,wq1,0,0,wp6,wb2,0],
                   [0,0,0,wr1,0,wr2,wk,0]])

# List of critical positions, who moves, and information
games_list = [[gutman, 'b', "Black's turn | Gutma vs Vitolinsh 1979"],
             [kasparov, 'w', "White's turn | Kasparov vs Dubiel 1993"],
             [sagar13, 'w', "White's turn | Sagar vs Vinay 2013"],
             [anand, 'b', "Black's turn | Anand vs Carlsen 2013"],
             [sagar12, 'w', "White's turn | Sagar vs Deepthamsh 2012"]]

# For a traditional experience, hide_disabled_moves should be set to True or 1,
# however, setting it to 0 allows the user to see if everything is working 
# correctly since each piece that can't be moved will be greyed out.
hide_disabled_moves = 1
if hide_disabled_moves:
    dbclr='black' # dbclr is short for disabled_color
else:
    dbclr='dimgrey'

# 8x8=64 buttons that will be used as the game board. Each is named by row,col
b00 = Button(disabledforeground=dbclr)
b01 = Button(disabledforeground=dbclr)
b01 = Button(disabledforeground=dbclr)
b02 = Button(disabledforeground=dbclr)
b03 = Button(disabledforeground=dbclr)
b04 = Button(disabledforeground=dbclr)
b05 = Button(disabledforeground=dbclr)
b06 = Button(disabledforeground=dbclr)
b07 = Button(disabledforeground=dbclr)
b10 = Button(disabledforeground=dbclr)
b11 = Button(disabledforeground=dbclr)
b12 = Button(disabledforeground=dbclr)
b13 = Button(disabledforeground=dbclr)
b14 = Button(disabledforeground=dbclr)
b15 = Button(disabledforeground=dbclr)
b16 = Button(disabledforeground=dbclr)
b17 = Button(disabledforeground=dbclr)
b20 = Button(disabledforeground=dbclr)
b21 = Button(disabledforeground=dbclr)
b22 = Button(disabledforeground=dbclr)
b23 = Button(disabledforeground=dbclr)
b24 = Button(disabledforeground=dbclr)
b25 = Button(disabledforeground=dbclr)
b26 = Button(disabledforeground=dbclr)
b27 = Button(disabledforeground=dbclr)
b30 = Button(disabledforeground=dbclr)
b31 = Button(disabledforeground=dbclr)
b32 = Button(disabledforeground=dbclr)
b33 = Button(disabledforeground=dbclr)
b34 = Button(disabledforeground=dbclr)
b35 = Button(disabledforeground=dbclr)
b36 = Button(disabledforeground=dbclr)
b37 = Button(disabledforeground=dbclr)
b40 = Button(disabledforeground=dbclr)
b41 = Button(disabledforeground=dbclr)
b42 = Button(disabledforeground=dbclr)
b43 = Button(disabledforeground=dbclr)
b44 = Button(disabledforeground=dbclr)
b45 = Button(disabledforeground=dbclr)
b46 = Button(disabledforeground=dbclr)
b47 = Button(disabledforeground=dbclr)
b50 = Button(disabledforeground=dbclr)
b51 = Button(disabledforeground=dbclr)
b52 = Button(disabledforeground=dbclr)
b53 = Button(disabledforeground=dbclr)
b54 = Button(disabledforeground=dbclr)
b55 = Button(disabledforeground=dbclr)
b56 = Button(disabledforeground=dbclr)
b57 = Button(disabledforeground=dbclr)
b60 = Button(disabledforeground=dbclr)
b61 = Button(disabledforeground=dbclr)
b62 = Button(disabledforeground=dbclr)
b63 = Button(disabledforeground=dbclr)
b64 = Button(disabledforeground=dbclr)
b65 = Button(disabledforeground=dbclr)
b66 = Button(disabledforeground=dbclr)
b67 = Button(disabledforeground=dbclr)
b70 = Button(disabledforeground=dbclr)
b71 = Button(disabledforeground=dbclr)
b72 = Button(disabledforeground=dbclr)
b73 = Button(disabledforeground=dbclr)
b74 = Button(disabledforeground=dbclr)
b75 = Button(disabledforeground=dbclr)
b76 = Button(disabledforeground=dbclr)
b77 = Button(disabledforeground=dbclr)

button_array = np.array([[b00,b01,b02,b03,b04,b05,b06,b07],
                         [b10,b11,b12,b13,b14,b15,b16,b17],
                         [b20,b21,b22,b23,b24,b25,b26,b27],
                         [b30,b31,b32,b33,b34,b35,b36,b37],
                         [b40,b41,b42,b43,b44,b45,b46,b47],
                         [b50,b51,b52,b53,b54,b55,b56,b57],
                         [b60,b61,b62,b63,b64,b65,b66,b67],
                         [b70,b71,b72,b73,b74,b75,b76,b77]])

# Buttons that are used to promote pawns
pawn_to_queen = Button(text = '\u2655', font = ('Arial', 30))
pawn_to_rook = Button(text = '\u2656', font = ('Arial', 30))
pawn_to_bishop = Button(text = '\u2657', font = ('Arial', 30))
pawn_to_knight = Button(text = '\u2658', font = ('Arial', 30))