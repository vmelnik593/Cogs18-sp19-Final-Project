from tkinter import Button, Label, Tk
import numpy as np
import random
from my_classes import King, Queen, Rook, Knight, Bishop, Pawn
from my_variables import (start_board, reset_board, test_list, games_list,
    button_array, pawn_to_queen, pawn_to_rook, pawn_to_bishop, pawn_to_knight)

# This was used for testing. current_board = np.zeros((8,8))
# current_board = np.array(current_board,dtype = object)

current_board = start_board
testing_index = 0 # This is used to keep track of the current test board

# This determines whose turn it is
white_moves = True


def reset_board(set_board = [[reset_board, 'w', '']], board = current_board, screen = '', test_iter = False):
    """Resets the current board.

    Args:
        set_board(list): list with boards from which to choose from to reset to,
                         color which is to move, info about the board, and info on whether tests are being iterated through.
        board(numpy array): The board layout on which the piece resides.
        
    """

    # If test_iter is True, this will iterate through the test boards
    global testing_index
    if test_iter == True:
        rand_board = set_board[testing_index]
        if testing_index < len(set_board) - 1:
            testing_index += 1
        else:
            testing_index = 0
        board = rand_board[0]
    else:
        # Set the reset board
        rand_board = random.choice(set_board)
        board = rand_board[0]

    mover = rand_board[1]
    game_info = rand_board[2]
    current_board = board

    # Resets the number of moves each piece has made to 0
    for rw in range(8):
        for cl in range(8):
            current_board[rw,cl] = board[rw,cl]
            if current_board[rw,cl] != 0:
                current_board[rw,cl].moves = 0
    
    # Hides pawn promotion buttons in case board is reset during pawn promotion
    pawn_to_queen.grid_forget()
    pawn_to_rook.grid_forget()
    pawn_to_bishop.grid_forget()
    pawn_to_knight.grid_forget()
    
    global white_moves
    
    if mover == 'w':
        white_moves = True
    else:
        white_moves = False
    
    # Hides previously written text
    message_label = Label(text = ('                                               '
                                  + '                                             '
                                  + '                                             '),
                          font = ('Arial', 12))
    message_label.grid(row = 9, columnspan = 8)
    
    draw(board) # Draws the new board
    
    # If there is a message to print, this makes sure it gets printed
    if game_info != '':
        message_label = Label(text = ('                                            '
                                      + '                                          '
                                      + '                                          '),
                              font = ('Arial', 12))
        message_label.grid(row = 9, columnspan = 8)
        message_label = Label(text = game_info, font = ('Arial', 12))
        message_label.grid(row = 9, columnspan = 8)


def promote(rw, cl, promotion,board = current_board):
    """Promotes a pawn and draws the new board.
    
    Args:
        rw(int): The row where the pawn is located.
        cl(int): The column where the pawn is located.
        board(numpy array): The current board layout.
    """
    
    # Hides the buttons when one is pressed
    pawn_to_queen.grid_forget()
    pawn_to_rook.grid_forget()
    pawn_to_bishop.grid_forget()
    pawn_to_knight.grid_forget()
    
    # Replaces the pawn with the chosen piece, keeping the color the same
    if promotion == 'q':
        board[rw, cl] = Queen(board[rw, cl].color)
    elif promotion == 'r':
        board[rw, cl] = Rook(board[rw, cl].color)
    elif promotion == 'bi':
        board[rw, cl] = Bishop(board[rw, cl].color)
    elif promotion == 'n':
        board[rw, cl] = Knight(board[rw, cl].color)
    
    message_label = Label(text = ('                                           '
                                  + '                                         '
                                  + '                                '))
    message_label.grid(row = 9, columnspan = 8)
                          
    draw(board)


def move_to(from_rw, from_cl, to_rw, to_cl, board = current_board, drw = True):
    """Moves a piece on the board.
    
    Args:
        from_rw(int): The original row of the piece.
        from_cl(int): The original column of the piece.
        to_rw(int): The new row of the piece.
        to_cl(int): The new row of the piece.
        board(numpy array): The current board layout.
        drw(bool): Draws the board if True, returns the board array otherwise.
        
    Returns:
        board(numpy array): The updated board layout after the move is made.
    """
    board[to_rw, to_cl] = board[from_rw, from_cl] # Copies piece to new position
    board[from_rw, from_cl] = 0 # Sets old position to 0
    disable_board = False # Sets all buttons to be able to be pressed
    
    # If a pawn made it across, disables board, and enables promote buttons
    if ((to_rw == 0) or (to_rw == 7)) and (board[to_rw, to_cl].piece == 'p'):
        pawn_to_queen.configure(command = lambda to_rw = to_rw, to_cl = to_cl:
                              promote(to_rw, to_cl,'q', board))
        pawn_to_queen.grid(row = 10, column = 0)
        pawn_to_rook.configure(command = lambda to_rw = to_rw, to_cl = to_cl:
                             promote(to_rw, to_cl,'r', board))
        pawn_to_rook.grid(row = 10, column = 1)
        pawn_to_bishop.configure(command = lambda to_rw = to_rw, to_cl = to_cl:
                               promote(to_rw, to_cl,'bi', board))
        pawn_to_bishop.grid(row = 10, column = 2)
        pawn_to_knight.configure(command = lambda to_rw = to_rw, to_cl = to_cl:
                               promote(to_rw, to_cl,'n', board))
        pawn_to_knight.grid(row = 10, column = 3)
        disable_board = True
    
    # If the king is castleing left, sets the rook to the right place
    if ((board[to_rw, to_cl] != 0) and
        (board[to_rw, to_cl].piece == 'k') and
        (board[to_rw, to_cl].moves == 0) and
        (to_cl == 2)):
        board[to_rw, 3] = board[to_rw,0]
        board[to_rw,0] = 0
    
    # King castling right
    if ((board[to_rw, to_cl] != 0) and
        (board[to_rw, to_cl].piece == 'k') and
        (board[to_rw, to_cl].moves == 0) and
        (to_cl == 6)):
        board[to_rw,5] = board[to_rw, 7]
        board[to_rw, 7] = 0
        
    # Deletes the appropriate pawn if a pawn is attacking En passant.
    if ((board[to_rw, to_cl] != 0) and
        (board[to_rw, to_cl].piece != 0) and
        (board[to_rw, to_cl].piece == 'p') and
        ((to_rw == 2) or (to_rw == 5))):
        if ((board[to_rw, to_cl].color == 'b') and
            (board[to_rw-1, to_cl] != 0) and
            (board[to_rw-1, to_cl].piece == 'p') and
            (board[to_rw-1, to_cl].justmoved)):
            board[to_rw-1, to_cl]=0
        elif ((board[to_rw, to_cl].color == 'w') and
              (board[to_rw+1, to_cl] != 0) and
              (board[to_rw+1, to_cl].piece == 'p') and
              (board[to_rw+1, to_cl].justmoved)):
            board[to_rw+1, to_cl]=0
    
    # Adds 1 to the move counter for the piece
    if (board[to_rw, to_cl] != 0):
        board[to_rw, to_cl].moves += 1
    
    # Sets all pieces .justmoved method to False
    for irw in range(8):
        for icl in range(8):
            if board[irw, icl] != 0:
                board[irw, icl].justmoved = False
        
    # Sets the moved piece .justmoved method to True
    if (board[to_rw, to_cl] != 0):
        board[to_rw, to_cl].justmoved = True
    
    # If the input drw is set to True (True by default), display the board
    if drw:
    # Hides previously written text
        message_label = Label(text = ('                                               '
                                      + '                                             '
                                      + '                                             '),
                              font = ('Arial', 12))
        message_label.grid(row = 9, columnspan = 8)
        global white_moves
        white_moves = not white_moves
        draw(board,disabled_buttons = disable_board)
        
        # Pawn promo message if conditions are met
        if ((to_rw == 0) or (to_rw == 7)) and (board[to_rw, to_cl].piece == 'p'):
            message_label = Label(text = 'Promote your pawn.',
                                 font = ('Arial',12))
            message_label.grid(row = 9, columnspan = 8)
    else:
        return board

    
def show_moves(rw, cl, board = current_board):
    """Shows the available legal moves when a piece is selected.
    
    Args:
        rw(int): The row of the selected piece.
        cl(int): The column of the selected piece.
        board(numpy array): The board layout on which the piece resides.
    """
    legal_moves = (board[rw, cl].legal_moves(rw, cl, board)
                  + board[rw, cl].legal_takes(rw, cl, board))
    from_rw = rw
    from_cl = cl
    
    for rw in range(8):
        for cl in range(8):
            bg_color = 'white' # Sets every quare to white
            button_state = 'normal'
            if (rw + cl) % 2 == 1:
                bg_color = 'lightgray' # Sets every other square gray
            if legal_moves[rw, cl] == 0: # Disable spots that can't be moved to
                button_state = 'disabled'
            if board[rw, cl] == 0: # Empty symbol for spaces w/o pieces
                symbol = ''
            else:
                symbol = board[rw, cl].sym # sets unicode symbol
            
            if legal_moves[rw, cl] != 0: # Set legal move buttons to green
                bg_color = 'green'
                
            
            # Configures each button appropriately to pass through it's row and
            # column into the command function if it is pressed. Also, sets the
            # button text to the unicode symbol.
            button_array[rw, cl].config(command = lambda from_rw = from_rw,
                                       from_cl = from_cl,
                                       rw = rw,
                                       cl = cl: move_to(from_rw, from_cl, rw, cl),
                                       state = button_state, text = symbol,
                                       bg = bg_color, width = 3,
                                       height = 1, font = ('Arial', 30))
            button_array[rw, cl].grid(row = rw, column = cl) # Places button
            

def draw(board = current_board, disabled_buttons = False, screen = ''):
    """Displays the given board onto the screen.
    
    Args:
        board(numpy array): The board which is to be displayed.
        disabled_buttons(bool): Disables the board if True.
        screen(Tkinter window)
    """

    for irw in range(8):
        for icl in range(8):
            current_board[irw,icl] = board[irw,icl]
            
    # Variable that stores whether any pieces of the current color can move
    no_moves = True
    checked = False
    
    if white_moves:
        mover = 'White'
    else:
        mover = 'Black'

    message = mover + "'s Turn"
    
    # Initializing the king's background color, row, and column as values that
    # they can't be ultimately to help with implementation and finding errors.
    king_bg_color = 'black'
    king_rw = 10
    king_cl = 10
    
    for rw in range(8):
    
        for cl in range(8):
            bg_color = 'white' # Setting background (bg) to white
            button_state = 'disabled'
            if (rw + cl) % 2 == 1:
                bg_color = 'lightgray' # Setting bg gray for appropriate buttons
            if board[rw, cl] == 0:
                button_state = 'disabled' # Disabling buttons with no piece
            elif ((board[rw, cl].color == 'w') == white_moves):
                if board[rw, cl].can_move(rw, cl, board):
                    button_state = 'normal' # Enabling pieces that can move
                    no_moves = False # State of no_moves changes
                    # If the king has already been set as red (check & no moves)
                    # but a move is found now, this sets the king back to orange
                    # which represents the king being in check, but not mate
                    if king_bg_color == 'lightpink':
                        king_bg_color = 'orange'
                # Set the king background to orange if in check.
                if ((board[rw, cl].piece == 'k') and
                    (board[rw, cl].check(rw, cl, rw, cl, board) == 0)):
                    king_bg_color = 'orange'
                    king_rw = rw
                    king_cl = cl
                    # Set the king background to light pink if there are also no
                    # moves available to get out of check.
                    if no_moves:
                        king_bg_color = 'lightpink'
                        checked = True
            # Sets the button symbol to empty if no piece on that spot.
            if board[rw, cl] == 0:
                symbol = ''
            else:
                symbol = board[rw, cl].sym 
            if disabled_buttons:
                button_state = 'disabled'
                
            # Creates each button, passing through row and column.
            button_array[rw, cl].config(command = lambda rw = rw,
                                       cl = cl: show_moves(rw, cl, board),
                                       text = symbol, bg = bg_color,
                                       width = 3, height = 1,
                                       font = ('Arial', 30),
                                       state = button_state)
            # Adds the button to the GUI
            button_array[rw, cl].grid(row = rw, column = cl)
        
    # King_rw is initialized as 10 and will only be changed if the background
    # color also changes to either orange or light pink. This will update the
    # buttons to reflect the changes.
    if king_rw != 10:
        button_array[king_rw,king_cl].config(bg = king_bg_color)
        button_array[king_rw,king_cl].grid(row = king_rw, column = king_cl)
    
    reset_button = Button(text ='\u27F2', font = ('Arial', 30),
                          command = lambda: reset_board())

    shuffle_button = Button(text ='\u2605', font = ('Arial', 30),
                          command = lambda games = games_list: reset_board(games))

    testing_button = Button(text ='Tests', font = ('Arial', 10),
                            height = 4, width = 8,
                          command = lambda games = test_list: reset_board(games, test_iter = True))

    reset_button.grid(row = 10, column = 7) # Adds the reset button
    shuffle_button.grid(row = 10, column = 6) # Adds the shuffle button
    testing_button.grid(row = 10, column = 5) # Adds the testing button
            
    if no_moves:
        if white_moves:
            if checked:
                message = 'Checkmate! Black Wins'
            else:
                message = 'Draw by stalemate. White has no legal moves left.'
        else:
            if checked:
                message = 'Checkmate! White Wins'
            else:
                message = 'Draw by stalemate. Black has no legal moves left.'
        
    message_label = Label(text = message, font = ('Arial',12))
    message_label.grid(row = 9, columnspan = 8)