import numpy as np


class Piece():
    """Generic piece containing all standard chess moves, and a check for check.
    Args:
        color(str): Color of the piece ('b' for Black or 'w' for White).
        piece(str): Type of piece 'k', 'q', 'r', 'bi', or 'n' for
               King, Queen, Rook, Bishop, or Knight respectively.
    
    Attributes:
        piece(str): Type of piece ('k', 'q', 'r', 'bi', or 'n')
        color(str): Color of piece ('b' or 'w')
        sym(str): Unicode symbol of the piece.
        moves(int): The number of times the piece has moved.
        justmoved(bool): Is true if the piece has just moved, False otherwise.
    """
    # Creating an empty board which will be updated later.
    current_board = np.zeros((8,8))

    def __init__(self, color, piece):
        self.piece = piece
        self.color = color
        
        # Sets the unicode string which will display the piece on the board
        if color == 'w':
            if piece == 'k':
                symbol = '\u2654'
            elif piece == 'q':
                symbol = '\u2655'
            elif piece == 'r':
                symbol = '\u2656'
            elif piece == 'bi':
                symbol = '\u2657'
            elif piece == 'n':
                symbol = '\u2658'
            elif piece == 'p':
                symbol = '\u2659'
        elif color == 'b':
            if piece == 'k':
                symbol = '\u265A'
            elif piece == 'q':
                symbol = '\u265B'
            elif piece == 'r':
                symbol = '\u265C'
            elif piece == 'bi':
                symbol = '\u265D'
            elif piece == 'n':
                symbol = '\u265E'
            elif piece == 'p':
                symbol = '\u265F' 
                
        self.sym = symbol
        self.moves = 0
        self.justmoved = False
        

    def in_board(self, rw,cl):
        """Checks if a the row and column are within the board limits.
        
        Args:
            rw(int): The row to be tested.
            cl(int): The column to be tested

        Returns:
            True if within limits, False otherwise.
        """
        if ((rw >= 0) and (rw <= 7) and (cl >= 0) and (cl <= 7)):
            return True
        else:
            return False


    def find_king(self, color, board):
        """Finds the row and column of the king, given color.
        
        Args:
            color(str): Which color king to find.
            board(numpy array): The current board layout.

        Returns:
            King_rw(int): The row location of the king.
            King_cl(int): The column location of the king.
        """
        for irw in range(8):
            for icl in range(8):
                if ((board[irw, icl] != 0) and
                    (board[irw, icl].piece == 'k') and
                    (board[irw, icl].color == color)):
                    king_rw = irw
                    king_cl = icl
        return king_rw, king_cl


    def check(self, from_rw, from_cl, to_rw, to_cl, board = current_board):
        """Given a move, checks if the king will be in check.
        
        Args:
            from_rw('int'): The row where the piece is moving from.
            from_cl('int'): The column where the piece is moving from.
            to_rw('int'): The row where the piece is moving to.
            to_cl('int'): The column where the piece is moving to.
            board(numpy array): The board layout on which the piece resides.
            
        Returns:
            int: 1 if not in check, and 0 if in check.
        """
        # new_board is a temporary board to test check on, without changing the
        # gloabl board.
        new_board = np.zeros((8,8))
        new_board = np.array(new_board, dtype = object)

        for irw in range(8):
            for icl in range(8):
                new_board[irw,icl] = board[irw,icl]

        # Moving the piece to the new position
        new_board[to_rw, to_cl] = new_board[from_rw, from_cl]
        
        # If the piece has actually moved, clearing the old spot.
        if (to_rw != from_rw) or (to_cl != from_cl):
            new_board[from_rw, from_cl] = 0
        
        # Checking the location of the king for the current active color.
        king_rw, king_cl = self.find_king(new_board[to_rw, to_cl].color, new_board)
        
        # Checking if the king can be attacked by any rooks.
        avail_rook_takes = self.avail_rook_takes(king_rw, king_cl, new_board)
        if self.contains_piece('r',avail_rook_takes,new_board):
            return 0
        
        # Checking if the king can be attacked by any bishops.
        avail_bishop_takes = self.avail_bishop_takes(king_rw, king_cl, new_board)
        if self.contains_piece('bi',avail_bishop_takes,new_board):
            return 0
            
        # Checking if the king can be attacked by any queens.
        avail_queen_takes = self.avail_queen_takes(king_rw, king_cl,new_board)
        if self.contains_piece('q',avail_queen_takes,new_board):
            return 0
        
        # Checking if the king can be attacked by any knights.
        avail_knight_takes = self.avail_knight_takes(king_rw, king_cl, new_board)
        if self.contains_piece('n',avail_knight_takes,new_board):
            return 0
        
        # Checking if the king can be attacked by any pawns.
        avail_pawn_takes = self.avail_pawn_takes(king_rw, king_cl, new_board)
        if self.contains_piece('p',avail_pawn_takes,new_board):
            return 0
        
        # Checking if the king can be attacked by the opponent's king.
        avail_king_takes = self.avail_king_takes(king_rw, king_cl, new_board)
        if self.contains_piece('k',avail_king_takes,new_board):
            return 0
        return 1


    def contains_piece(self, piece,avail_takes,board):
        """Checks an array of potential attacks for specific pieces
        
        Args:
            piece(str): The row where the piece is at.
            avail_takes(numpy array): The column where the piece is at.
            board(numpy array): An array with 1 in rows and columns with
                                      available moves
            
        Returns:
            True if avail_takes contains the target piece, false otherwise.         
        
        """
        for irw in range(8):
            for icl in range(8):
                if ((avail_takes[irw, icl] == 1) and (board[irw, icl].piece == piece)):
                    return True
        return False

            
    def legal_check(self, rw, cl, moves_board, board = current_board):
        """Checks potential moves for whether it would get the king into check.
        
        Args:
            rw(int): The row where the piece is at.
            cl(int): The column where the piece is at.
            moves_board(numpy array): An array with 1 in rows and columns with
                                      available moves
            board(numpy array): The board layout on which the piece resides.
            
        Returns:
            moves_board(numpy array): An array representing moves that won't
                                      put the king into check.           
        
        """
        for irw in range(8):
            for icl in range(8):
                if moves_board[irw, icl] != 0:
                    moves_board[irw, icl] *= self.check(rw, cl, irw, icl, board)
        return moves_board


    def legal_moves(self, rw, cl, board = current_board):
        """Spaces where the piece can move to legally.
        
        Args:
            rw(int): The row where the piece is at.
            cl(int): The column where the piece is at.
            board(numpy array): The board layout on which the piece resides.
            
        Returns:
            allowed_moves(numpy array): An array representing the legal moves.           
        
        """
        # The generic piece has no allowed moves. This function will be updated
        # for each individual piece class.
        # The purpose of this function, and legal_takes, is to have a function
        # that can be called in any class to return legal moves and takes
        allowed_moves = np.zeros((8,8))
        return allowed_moves
    
    def legal_takes(self, rw, cl, board = current_board):
        """Spaces where the piece can move to legally, for captures.
        
        Args:
            rw(int): The row where the piece is at.
            cl(int): The column where the piece is at.
            board(numpy array): The board layout on which the piece resides.
            
        Returns:
            allowed_takes(numpy array): An array representing legal captures.           
        """
        # The generic piece has no allowed moves. This function will be updated
        # for each individual piece class.
        allowed_takes = np.zeros((8,8))
        return allowed_takes
    
    def can_move(self, rw, cl, board = current_board):
        """Checks if the piece has any legal moves or captures available.
        
        Args:
            rw(int): The row where the piece is at.
            cl(int): The column where the piece is at.
            board(numpy array): The board layout on which the piece resides.
            
        Returns:
            True if there is a legal move or capture available.           
        
        """
        allowed_moves = self.legal_moves(rw, cl, board)
        allowed_takes = self.legal_takes(rw, cl, board)
        return allowed_moves.any() or allowed_takes.any()

    def avail_rook_moves(self, rw, cl, board = current_board):
        """Returns potentially legal moves for a rook, given position.
        
        Args:
            rw(int): The row where the piece is at.
            cl(int): The column where the piece is at.
            board(numpy array): The board layout on which the piece resides.
            
        Returns:
            allowed_moves(numpy array): An array representing potentially
            legal moves.
        
        """
        allowed_moves = np.zeros((8,8))
        
        # Starting at the position of the rook and this iterates up, down, left,
        # and right storing every empty spot until it's blocked by another piece
        for num in range(rw, 0, -1):
            if board[num-1, cl] != 0:
                break
            else:
                allowed_moves[num-1, cl] = 1
                
        for num in range(rw, 7):
            if board[num+1, cl] != 0:
                break
            else:
                allowed_moves[num+1, cl] = 1
                
        for num in range(cl, 0, -1):
            if board[rw, num-1] != 0:
                break
            else:
                allowed_moves[rw, num-1] = 1
                
        for num in range(cl, 7):
            if board[rw, num+1] != 0:
                break
            else:
                allowed_moves[rw, num+1] = 1
        return allowed_moves

    def avail_rook_takes(self, rw, cl, board = current_board):
        """Returns potentially legal captures for a rook, given position.
        
        Args:
            rw(int): The row where the piece is at.
            cl(int): The column where the piece is at.
            board(numpy array): The board layout on which the piece resides.
            
        Returns:
            allowed_moves(numpy array): An array representing potentially
            legal moves.
        
        """
        allowed_takes = np.zeros((8,8))
        
        # Similar to above, this iterates up, down, left, and right, but it
        # stores the first opponent piece it runs into, along each direction.
        for num in range(rw, 0, -1):
            if (board[num-1, cl] != 0) and (board[num-1, cl].color == self.color):
                break
            elif board[num-1, cl] == 0:
                continue
            else:
                allowed_takes[num-1, cl] = 1
                break
                
        for num in range(rw, 7):
            if (board[num+1, cl] != 0) and (board[num+1, cl].color == self.color):
                break
            elif board[num+1, cl] == 0:
                continue
            else:
                allowed_takes[num+1, cl] = 1
                break
                
        for num in range(cl, 0, -1):
            if (board[rw, num-1] != 0) and (board[rw, num-1].color == self.color):
                break
            elif board[rw, num-1] == 0:
                continue
            else:
                allowed_takes[rw, num-1] = 1
                break
                
        for num in range(cl, 7):
            if (board[rw, num+1] != 0) and (board[rw, num+1].color == self.color):
                break
            elif board[rw, num+1] == 0:
                continue
            else:
                allowed_takes[rw, num+1] = 1
                break
        return allowed_takes
    
    # Same as avail_rook_moves, but it also checks if the king will be in
    # check with self.check. If the king won't be in check, it saves the
    # position.
    ##
    # Both functions are necessary as otherwise avail_rook_moves
    # would be called within itself when self.check is called.
    ##
    def legal_rook_moves(self, rw, cl, board = current_board):
        """Returns legal moves for a rook, given position.
        
        Args:
            rw(int): The row where the piece is at.
            cl(int): The column where the piece is at.
            board(numpy array): The board layout on which the piece resides.
            
        Returns:
            allowed_moves(numpy array): An array representing legal moves.
        
        """
        #allowed_moves = np.zeros((8,8))
        
        allowed_moves = self.avail_rook_moves(rw, cl, board)
        allowed_moves = self.legal_check(rw, cl, allowed_moves, board)

        return allowed_moves


    def legal_rook_takes(self, rw, cl, board = current_board):
        """Returns legal captures for a rook, given position.
        
        Args:
            rw(int): The row where the piece is at.
            cl(int): The column where the piece is at.
            board(numpy array): The board layout on which the piece resides.
            
        Returns:
            allowed_moves(numpy array): An array representing legal captures.
        
        """
        allowed_moves = self.avail_rook_takes(rw, cl, board)
        allowed_moves = self.legal_check(rw, cl, allowed_moves, board)

        return allowed_moves
    
    
    # All of the following piece definitions follow the same general format:
    # 4 functions: available_moves, available_takes, legal_moves, legal_takes
    def avail_knight_moves(self, rw, cl, board = current_board):
        """Returns potentially legal moves for a knight, given position.
        
        Args:
            rw(int): The row where the piece is at.
            cl(int): The column where the piece is at.
            board(numpy array): The board layout on which the piece resides.
            
        Returns:
            allowed_moves(numpy array): An array representing potentially
            legal moves.
        
        """
        allowed_moves = np.zeros((8,8))
        potential_moves = [[rw+2, cl+1],[rw+2, cl-1],[rw-2, cl+1],[rw-2, cl-1],
                           [rw+1, cl+2],[rw-1, cl+2],[rw+1, cl-2],[rw-1, cl-2]]
        
        # Checks each potential move to see if it's not blocked and stores them
        for move in potential_moves:
            if ((self.in_board(move[0],move[1])) and
                (board[move[0], move[1]] == 0)):
                allowed_moves[move[0], move[1]] = 1
        return allowed_moves
    
    def avail_knight_takes(self, rw, cl, board = current_board):
        """Returns potentially legal captures for a knight, given position.
        
        Args:
            rw(int): The row where the piece is at.
            cl(int): The column where the piece is at.
            board(numpy array): The board layout on which the piece resides.
            
        Returns:
            allowed_moves(numpy array): An array representing potentially
            legal moves.
        
        """
        allowed_takes = np.zeros((8,8))
        potential_takes = [[rw+2, cl+1],[rw+2, cl-1],[rw-2, cl+1],[rw-2, cl-1],
                           [rw+1, cl+2],[rw-1, cl+2],[rw+1, cl-2],[rw-1, cl-2]]
        
        # Checks each potential move to look for an opponent's piece
        for move in potential_takes:
            if ((self.in_board(move[0],move[1])) and
                (board[move[0], move[1]] != 0) and
                (board[move[0], move[1]].color != self.color)):
                allowed_takes[move[0], move[1]] = 1
        return allowed_takes
    
    def legal_knight_moves(self, rw, cl, board = current_board):
        """Returns legal moves for a knight, given position.
        
        Args:
            rw(int): The row where the piece is at.
            cl(int): The column where the piece is at.
            board(numpy array): The board layout on which the piece resides.
            
        Returns:
            allowed_moves(numpy array): An array representing legal moves.
        
        """
        allowed_moves = self.avail_knight_moves(rw, cl, board)
        allowed_moves = self.legal_check(rw, cl, allowed_moves, board)

        return allowed_moves

    
    def legal_knight_takes(self, rw, cl, board = current_board):
        """Returns legal captures for a knight, given position.
        
        Args:
            rw(int): The row where the piece is at.
            cl(int): The column where the piece is at.
            board(numpy array): The board layout on which the piece resides.
            
        Returns:
            allowed_moves(numpy array): An array representing legal captures.
        
        """
        allowed_moves = self.avail_knight_takes(rw, cl, board)
        allowed_moves = self.legal_check(rw, cl, allowed_moves, board)

        return allowed_moves

    
    def avail_bishop_moves(self, rw, cl, board = current_board):
        """Returns potentially legal moves for a bishop, given position.
        
        Args:
            rw(int): The row where the piece is at.
            cl(int): The column where the piece is at.
            board(numpy array): The board layout on which the piece resides.
            
        Returns:
            allowed_moves(numpy array): An array representing potentially
            legal moves.
        
        """
        allowed_moves = np.zeros((8,8))
        for a,b in zip(range(rw, 0, -1),range(cl, 0, -1)):
            if board[a-1, b-1] != 0:
                break
            else:
                allowed_moves[a-1, b-1] = 1
                
        for a,b in zip(range(rw, 7),range(cl, 0, -1)):
            if board[a+1, b-1] != 0:
                break
            else:
                allowed_moves[a+1, b-1] = 1
                
        for a,b in zip(range(rw, 0, -1),range(cl, 7)):
            if board[a-1, b+1] != 0:
                break
            else:
                allowed_moves[a-1, b+1] = 1
                
        for a,b in zip(range(rw, 7),range(cl, 7)):
            if board[a+1, b+1] != 0:
                break
            else:
                allowed_moves[a+1, b+1] = 1
                
        return allowed_moves
    
    def avail_bishop_takes(self, rw, cl, board = current_board):
        """Returns potentially legal captures for a bishop, given position.
        
        Args:
            rw(int): The row where the piece is at.
            cl(int): The column where the piece is at.
            board(numpy array): The board layout on which the piece resides.
            
        Returns:
            allowed_moves(numpy array): An array representing potentially
            legal moves.
        
        """
        allowed_takes = np.zeros((8,8))
        
        # Iterates diagonally in 4 directions, storing position, until it runs
        # across a blockes space.
        for a,b in zip(range(rw, 0, -1),range(cl, 0, -1)):
            if (board[a-1, b-1] != 0) and (board[a-1, b-1].color == self.color):
                break
            elif board[a-1, b-1] == 0:
                continue
            else:
                allowed_takes[a-1, b-1] = 1
                break
                
        for a,b in zip(range(rw, 7),range(cl, 0, -1)):
            if (board[a+1, b-1] != 0) and (board[a+1, b-1].color == self.color):
                break
            elif board[a+1, b-1] == 0:
                continue
            else:
                allowed_takes[a+1, b-1] = 1
                break
                
        for a,b in zip(range(rw, 0, -1),range(cl, 7)):
            if (board[a-1, b+1] != 0) and (board[a-1, b+1].color == self.color):
                break
            elif board[a-1, b+1] == 0:
                continue
            else:
                allowed_takes[a-1, b+1] = 1
                break
                
        for a,b in zip(range(rw, 7),range(cl, 7)):
            if (board[a+1, b+1] != 0) and (board[a+1, b+1].color == self.color):
                break
            elif board[a+1, b+1] == 0:
                continue
            else:
                allowed_takes[a+1, b+1] = 1
                break
        return allowed_takes
    
    # Iterates diagonally as before, but stores the first opponent position in
    # each of the diagonal directions
    def legal_bishop_moves(self, rw, cl, board = current_board):
        """Returns legal moves for a bishop, given position.
        
        Args:
            rw(int): The row where the piece is at.
            cl(int): The column where the piece is at.
            board(numpy array): The board layout on which the piece resides.
            
        Returns:
            allowed_moves(numpy array): An array representing legal moves.
        
        """
        allowed_moves = self.avail_bishop_moves(rw, cl, board)
        allowed_moves = self.legal_check(rw, cl, allowed_moves, board)

        return allowed_moves

    
    def legal_bishop_takes(self, rw, cl, board = current_board):
        """Returns legal captures for a bishop, given position.
        
        Args:
            rw(int): The row where the piece is at.
            cl(int): The column where the piece is at.
            board(numpy array): The board layout on which the piece resides.
            
        Returns:
            allowed_moves(numpy array): An array representing legal captures.
        
        """
        allowed_takes = np.zeros((8,8))
        
        allowed_moves = self.avail_bishop_takes(rw, cl, board)
        allowed_moves = self.legal_check(rw, cl, allowed_moves, board)

        return allowed_moves

    
    def avail_queen_moves(self, rw, cl, board = current_board):
        """Returns potentially legal moves for a queen, given position.
        
        Args:
            rw(int): The row where the piece is at.
            cl(int): The column where the piece is at.
            board(numpy array): The board layout on which the piece resides.
            
        Returns:
            allowed_moves(numpy array): An array representing potentially
            legal moves.
        
        """
        # The queen just combines the moves of the bishop and rook
        allowed_moves = (self.avail_bishop_moves(rw, cl, board)
                         + self.avail_rook_moves(rw, cl, board))
        return allowed_moves
    
    def avail_queen_takes(self, rw, cl, board = current_board):
        """Returns potentially legal captures for a queen, given position.
        
        Args:
            rw(int): The row where the piece is at.
            cl(int): The column where the piece is at.
            board(numpy array): The board layout on which the piece resides.
            
        Returns:
            allowed_moves(numpy array): An array representing potentially
            legal moves.
        
        """
        allowed_takes = self.avail_bishop_takes(rw, cl, board)+\
        self.avail_rook_takes(rw, cl, board)
        return allowed_takes
 
    def legal_queen_moves(self, rw, cl, board = current_board):
        """Returns legal moves for a queen, given position.
        
        Args:
            rw(int): The row where the piece is at.
            cl(int): The column where the piece is at.
            board(numpy array): The board layout on which the piece resides.
            
        Returns:
            allowed_moves(numpy array): An array representing legal moves.
        
        """
        allowed_moves = self.avail_queen_moves(rw, cl, board)
        allowed_moves = self.legal_check(rw, cl, allowed_moves, board)

        return allowed_moves

    
    def legal_queen_takes(self, rw, cl, board = current_board):
        """Returns legal captures for a queen, given position.
        
        Args:
            rw(int): The row where the piece is at.
            cl(int): The column where the piece is at.
            board(numpy array): The board layout on which the piece resides.
            
        Returns:
            allowed_moves(numpy array): An array representing legal captures.
        
        """
        allowed_moves = self.avail_queen_takes(rw, cl, board)
        allowed_moves = self.legal_check(rw, cl, allowed_moves, board)

        return allowed_moves

    
    def avail_pawn_moves(self, rw, cl, board = current_board):
        """Returns potentially legal moves for a pawn, given position.
        
        Args:
            rw(int): The row where the piece is at.
            cl(int): The column where the piece is at.
            board(numpy array): The board layout on which the piece resides.
            
        Returns:
            allowed_moves(numpy array): An array representing potentially
            legal moves.
        
        """
        allowed_moves = np.zeros((8,8))       
        if self.color == 'w':
            # Checks if first spot in front is open
            if (rw-1 >= 0) and (board[rw-1, cl] == 0):
                allowed_moves[rw-1, cl] = 1
                # If first spot in front is open, and pawn hasn't moved, and pawn is in row 2 or 7, also checks 2nd spot
                if (rw-2 >= 0) and (board[rw-2, cl] == 0) and (self.moves == 0) and (rw == 1 or rw == 6):
                    allowed_moves[rw-2, cl] = 1
        else:
            if (rw+1 <= 7) and (board[rw+1, cl] == 0):
                allowed_moves[rw+1, cl] = 1
                if (rw+2 <= 7) and (board[rw+2, cl] == 0) and (self.moves == 0) and (rw == 1 or rw == 6):
                    allowed_moves[rw+2, cl] = 1
        return allowed_moves
    
    def avail_pawn_takes(self, rw, cl, board = current_board):
        """Returns potentially legal captures for a pawn, given position.
        
        Args:
            rw(int): The row where the piece is at.
            cl(int): The column where the piece is at.
            board(numpy array): The board layout on which the piece resides.
            
        Returns:
            allowed_moves(numpy array): An array representing potentially
            legal moves.
        
        """
        allowed_takes = np.zeros((8,8)) 
        
        # Checks the first diagonal positions in front for an opponent piece        
        if self.color == 'w':
            if ((rw-1 >= 0) and (cl-1 >= 0) and
                (board[rw-1, cl-1] != 0) and
                (board[rw-1, cl-1].color != self.color)):
                allowed_takes[rw-1, cl-1] = 1
            if ((rw-1 >= 0) and
                (cl+1 <= 7) and
                (board[rw-1, cl+1] != 0) and
                (board[rw-1, cl+1].color != self.color)):
                allowed_takes[rw-1, cl+1] = 1
        else:
            if ((rw+1 <= 7) and
                (cl-1 >= 0) and
                (board[rw+1, cl-1] != 0) and
                (board[rw+1, cl-1].color != self.color)):
                allowed_takes[rw+1, cl-1] = 1
            if ((rw+1 <= 7) and
                (cl+1 <= 7) and
                (board[rw+1, cl+1] != 0) and
                (board[rw+1, cl+1].color != self.color)):
                allowed_takes[rw+1, cl+1] = 1
        return allowed_takes
    
    def legal_pawn_moves(self, rw, cl, board = current_board):
        """Returns legal moves for a pawn, given position.
        
        Args:
            rw(int): The row where the piece is at.
            cl(int): The column where the piece is at.
            board(numpy array): The board layout on which the piece resides.
            
        Returns:
            allowed_moves(numpy array): An array representing legal moves.
        
        """
        allowed_moves = self.avail_pawn_moves(rw, cl, board)
        allowed_moves = self.legal_check(rw, cl, allowed_moves, board)

        return allowed_moves

    
    def legal_pawn_takes(self, rw, cl, board = current_board):
        """Returns legal captures for a pawn, given position.
        
        Args:
            rw(int): The row where the piece is at.
            cl(int): The column where the piece is at.
            board(numpy array): The board layout on which the piece resides.
            
        Returns:
            allowed_moves(numpy array): An array representing legal captures.
        
        """
        allowed_moves = self.avail_pawn_takes(rw, cl, board)
        allowed_moves = self.legal_check(rw, cl, allowed_moves, board)

        return allowed_moves


    def avail_king_moves(self, rw, cl, board = current_board):
        """Returns potentially legal moves for a king, given position.
        
        Args:
            rw(int): The row where the piece is at.
            cl(int): The column where the piece is at.
            board(numpy array): The board layout on which the piece resides.
            
        Returns:
            allowed_moves(numpy array): An array representing potentially
            legal moves.
        
        """
        allowed_moves = np.zeros((8,8))
        potential_moves = [[rw-1, cl-1],[rw-1, cl],[rw-1, cl+1],
                           [rw, cl-1],[rw, cl+1],
                           [rw+1, cl-1],[rw+1, cl],[rw+1, cl+1]]
        
        # This part works similar to how it does for the knight. It checks a set
        # list of positions around to see if they're on the board and available.
        for move in potential_moves:
            if ((self.in_board(move[0],move[1])) and
                (board[move[0], move[1]] == 0)):
                allowed_moves[move[0], move[1]] = 1
        return allowed_moves
    
    def avail_king_takes(self, rw, cl, board = current_board):
        """Returns potentially legal captures for a king, given position.
        
        Args:
            rw(int): The row where the piece is at.
            cl(int): The column where the piece is at.
            board(numpy array): The board layout on which the piece resides.
            
        Returns:
            allowed_moves(numpy array): An array representing potentially
            legal moves.
        
        """
        allowed_takes = np.zeros((8,8))
        potential_takes = [[rw-1, cl-1],[rw-1, cl],[rw-1, cl+1],
                           [rw, cl-1],[rw, cl+1],
                           [rw+1, cl-1],[rw+1, cl],[rw+1, cl+1]]
        
        for move in potential_takes:
            if ((self.in_board(move[0],move[1])) and
                (board[move[0], move[1]] != 0) and
                (board[move[0], move[1]].color != self.color)):
                allowed_takes[move[0], move[1]] = 1
        return allowed_takes
    
    def legal_king_moves(self, rw, cl, board = current_board):
        """Returns legal moves for a king, given position.
        
        Args:
            rw(int): The row where the piece is at.
            cl(int): The column where the piece is at.
            board(numpy array): The board layout on which the piece resides.
            
        Returns:
            allowed_moves(numpy array): An array representing legal moves.
        
        """
        allowed_moves = self.avail_king_moves(rw, cl, board)
        allowed_moves = self.legal_check(rw, cl, allowed_moves, board)

        return allowed_moves

    
    def legal_king_takes(self, rw, cl, board = current_board):
        """Returns legal captures for a king, given position.
        
        Args:
            rw(int): The row where the piece is at.
            cl(int): The column where the piece is at.
            board(numpy array): The board layout on which the piece resides.
            
        Returns:
            allowed_moves(numpy array): An array representing legal captures.
        
        """
        allowed_moves = self.avail_king_takes(rw, cl, board)
        allowed_moves = self.legal_check(rw, cl, allowed_moves, board)

        return allowed_moves
    
    
class King(Piece):
    """Class that contains the state and legal actions of a king piece.
    
    Args:
        color(str): Color of the piece ('b' for Black or 'w' for White).

    Attributes:
        piece(str): Type of piece ('k', 'q', 'r', 'bi', or 'n')
        color(str): Color of piece ('b' or 'w')
        sym(str): Unicode symbol of the piece.
        moves(int): The number of times the piece has moved.
        justmoved(bool): Is true if the piece has just moved, False otherwise.
    """
    current_board = np.zeros((8,8))
    
    def __init__(self, color):
        super().__init__(color, piece = 'k')
        
    def legal_moves(self, rw, cl, board = current_board):
        """Spaces where the piece can move to legally.
        
        Args:
            rw(int): The row where the piece is at.
            cl(int): The column where the piece is at.
            board(numpy array): The board layout on which the piece resides.
            
        Returns:
            allowed_moves(numpy array): An array representing the legal moves.           
        """
        
        legal_king_moves = self.legal_king_moves(rw, cl, board)

        # This sections checks if the king can castle: checking that the king
        # and each rook haven't moved, and that the spaces between are clear
        if ((self.moves == 0) and # King hasn't moved
            (self.check(rw, cl, rw, cl, board) == 1) and # Not in check
            (board[rw, cl-1] == 0) and # Spot to left is clear
            (self.check(rw, cl, rw, cl-1, board) == 1) and # Spot left is safe
            (board[rw, cl-2] == 0) and # 2nd spot left is clear
            (self.check(rw, cl, rw, cl-2, board) == 1) and # 2nd spot left is safe
            (board[rw, cl-3] == 0)  and # 3rd spot to left is clear
            (board[rw, cl-4] != 0) and # Rook spot isn't empty
            (board[rw, cl-4].piece == 'r') and # Rook is in place
            (board[rw, cl-4].moves == 0)): # Rook hasn't moved
            if self.color == 'w':
                legal_king_moves[7,2] = 1
            else:
                legal_king_moves[0,2] = 1    

        if ((cl == 4) and
            ((rw == 7) or(rw == 0)) and
            (self.moves == 0) and
            (self.check(rw, cl, rw, cl, board) == 1) and
            (board[rw, cl+1] == 0) and
            (self.check(rw, cl, rw, cl+1, board) == 1) and
            (board[rw, cl+2] == 0) and
            (self.check(rw, cl, rw, cl+2, board) == 1) and
            (board[rw, cl+3] != 0) and
            (board[rw, cl+3].piece == 'r') and
            (board[rw, cl+3].moves == 0)):
            if self.color == 'w':
                legal_king_moves[7,6] = 1
            else:
                legal_king_moves[0,6] = 1
        return legal_king_moves
        
            
    
    def legal_takes(self, rw, cl, board = current_board):
        """Spaces where the piece can move to legally, for captures.
        
        Args:
            rw(int): The row where the piece is at.
            cl(int): The column where the piece is at.
            board(numpy array): The board layout on which the piece resides.
            
        Returns:
            allowed_takes(numpy array): An array representing legal captures.           
        """
        return self.legal_king_takes(rw, cl, board)

    
class Pawn(Piece):
    """Class that contains the state and legal actions of a pawn piece.
    
    Args:
        color(str): Color of the piece ('b' for Black or 'w' for White).

    Attributes:
        piece(str): Type of piece ('k', 'q', 'r', 'bi', or 'n')
        color(str): Color of piece ('b' or 'w')
        sym(str): Unicode symbol of the piece.
        moves(int): The number of times the piece has moved.
        justmoved(bool): Is true if the piece has just moved, False otherwise.
    """
    current_board = np.zeros((8,8))
    
    def __init__(self, color):
        super().__init__(color, piece = 'p')
        
    def legal_moves(self, rw, cl, board = current_board):
        """Spaces where the piece can move to legally.
        
        Args:
            rw(int): The row where the piece is at.
            cl(int): The column where the piece is at.
            board(numpy array): The board layout on which the piece resides.
            
        Returns:
            allowed_moves(numpy array): An array representing the legal moves.           
        """
        return self.legal_pawn_moves(rw, cl, board)
    
    def legal_takes(self, rw, cl, board = current_board):
        """Spaces where the piece can move to legally, for captures.
        
        Args:
            rw(int): The row where the piece is at.
            cl(int): The column where the piece is at.
            board(numpy array): The board layout on which the piece resides.
            
        Returns:
            allowed_takes(numpy array): An array representing legal captures.           
        """
        legal_pawn_takes = self.legal_pawn_takes(rw, cl, board)
        
        # This is an implementation of En passant, which allows the pawn to
        # take an opponent's pawn while it's behind, in specific instances.
        if ((cl-1 >= 0) and
            ((rw == 3) or (rw == 4)) and # The attacking pawn is here
            (board[rw, cl-1] != 0) and # A piece is behind it
            (board[rw, cl-1].justmoved) and # That piece just moved
            (board[rw, cl-1].color != self.color) and # Opponent piece
            (board[rw, cl-1].piece == 'p') and # Opponent piece = pawn
            (board[rw, cl-1].moves == 1)): # Opponent pawn moved once
            if self.color == 'w':
                legal_pawn_takes[rw-1, cl-1] = 1 # Sets an extra legal take
            else:
                legal_pawn_takes[rw+1, cl-1] = 1
                
        if ((cl+1 <= 7) and
            ((rw == 3) or (rw == 4)) and
            (board[rw, cl+1] != 0) and
            (board[rw, cl+1].justmoved) and
            (board[rw, cl+1].color != self.color) and
            (board[rw, cl+1].piece == 'p') and
            (board[rw, cl+1].moves == 1)):
            if self.color == 'w':
                legal_pawn_takes[rw-1, cl+1] = 1
            else:
                legal_pawn_takes[rw+1, cl+1] = 1
        return legal_pawn_takes
    
    
class Knight(Piece):
    """Class that contains the state and legal actions of a knight piece.
    
    Args:
        color(str): Color of the piece ('b' for Black or 'w' for White).

    Attributes:
        piece(str): Type of piece ('k', 'q', 'r', 'bi', or 'n')
        color(str): Color of piece ('b' or 'w')
        sym(str): Unicode symbol of the piece.
        moves(int): The number of times the piece has moved.
        justmoved(bool): Is true if the piece has just moved, False otherwise.
    """
    current_board = np.zeros((8,8))
    
    def __init__(self, color):
        super().__init__(color, piece = 'n')
        
    def legal_moves(self, rw, cl, board = current_board):
        """Spaces where the piece can move to legally.
        
        Args:
            rw(int): The row where the piece is at.
            cl(int): The column where the piece is at.
            board(numpy array): The board layout on which the piece resides.
            
        Returns:
            allowed_moves(numpy array): An array representing the legal moves.           
        """
        return self.legal_knight_moves(rw, cl, board)
    
    def legal_takes(self, rw, cl, board = current_board):
        """Spaces where the piece can move to legally, for captures.
        
        Args:
            rw(int): The row where the piece is at.
            cl(int): The column where the piece is at.
            board(numpy array): The board layout on which the piece resides.
            
        Returns:
            allowed_takes(numpy array): An array representing legal captures.           
        """
        return self.legal_knight_takes(rw, cl, board)
    
    
class Rook(Piece):
    """Class that contains the state and legal actions of a rook piece.
    
    Args:
        color(str): Color of the piece ('b' for Black or 'w' for White).

    Attributes:
        piece(str): Type of piece ('k', 'q', 'r', 'bi', or 'n')
        color(str): Color of piece ('b' or 'w')
        sym(str): Unicode symbol of the piece.
        moves(int): The number of times the piece has moved.
        justmoved(bool): Is true if the piece has just moved, False otherwise.
    """
    current_board = np.zeros((8,8))
    
    def __init__(self, color):
        super().__init__(color, piece = 'r')
        
    def legal_moves(self, rw, cl, board = current_board):
        """Spaces where the piece can move to legally.
        
        Args:
            rw(int): The row where the piece is at.
            cl(int): The column where the piece is at.
            board(numpy array): The board layout on which the piece resides.
            
        Returns:
            allowed_moves(numpy array): An array representing the legal moves.           
        """
        return self.legal_rook_moves(rw, cl, board)
    
    def legal_takes(self, rw, cl, board = current_board):
        """Spaces where the piece can move to legally, for captures.
        
        Args:
            rw(int): The row where the piece is at.
            cl(int): The column where the piece is at.
            board(numpy array): The board layout on which the piece resides.
            
        Returns:
            allowed_takes(numpy array): An array representing legal captures.           
        """
        return self.legal_rook_takes(rw, cl, board)
    
    
class Bishop(Piece):
    """Class that contains the state and legal actions of a bishop piece.
    
    Args:
        color(str): Color of the piece ('b' for Black or 'w' for White).

    Attributes:
        piece(str): Type of piece ('k', 'q', 'r', 'bi', or 'n')
        color(str): Color of piece ('b' or 'w')
        sym(str): Unicode symbol of the piece.
        moves(int): The number of times the piece has moved.
        justmoved(bool): Is true if the piece has just moved, False otherwise.
    """
    current_board = np.zeros((8,8))
    
    def __init__(self, color):
        super().__init__(color, piece = 'bi')
        
    def legal_moves(self, rw, cl, board = current_board):
        """Spaces where the piece can move to legally.
        
        Args:
            rw(int): The row where the piece is at.
            cl(int): The column where the piece is at.
            board(numpy array): The board layout on which the piece resides.
            
        Returns:
            allowed_moves(numpy array): An array representing the legal moves.           
        """
        return self.legal_bishop_moves(rw, cl, board)
    
    def legal_takes(self, rw, cl, board = current_board):
        """Spaces where the piece can move to legally, for captures.
        
        Args:
            rw(int): The row where the piece is at.
            cl(int): The column where the piece is at.
            board(numpy array): The board layout on which the piece resides.
            
        Returns:
            allowed_takes(numpy array): An array representing legal captures.           
        """
        return self.legal_bishop_takes(rw, cl, board)
    
    
class Queen(Piece):
    """Class that contains the state and legal actions of a queen piece.
    
    Args:
        color(str): Color of the piece ('b' for Black or 'w' for White).

    Attributes:
        piece(str): Type of piece ('k', 'q', 'r', 'bi', or 'n')
        color(str): Color of piece ('b' or 'w')
        sym(str): Unicode symbol of the piece.
        moves(int): The number of times the piece has moved.
        justmoved(bool): Is true if the piece has just moved, False otherwise.
    """
    current_board = np.zeros((8,8))
    
    def __init__(self, color):
        super().__init__(color, piece = 'q')
        
    def legal_moves(self, rw, cl, board = current_board):
        """Spaces where the piece can move to legally.
        
        Args:
            rw(int): The row where the piece is at.
            cl(int): The column where the piece is at.
            board(numpy array): The board layout on which the piece resides.
            
        Returns:
            allowed_moves(numpy array): An array representing the legal moves.           
        """
        return self.legal_queen_moves(rw, cl, board)
    
    def legal_takes(self, rw, cl, board = current_board):
        """Spaces where the piece can move to legally, for captures.
        
        Args:
            rw(int): The row where the piece is at.
            cl(int): The column where the piece is at.
            board(numpy array): The board layout on which the piece resides.
            
        Returns:
            allowed_takes(numpy array): An array representing legal captures.           
        """
        return self.legal_queen_takes(rw, cl, board)

