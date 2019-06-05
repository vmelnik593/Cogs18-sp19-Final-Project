from my_classes import Piece

test_piece = Piece('b','q')


def test_in_board():
	"""Test function that tests the in_board() method contained in the Piece class.
	Args:
		None

	Returns:
		Passes silently if all asserts pass.
		Otherwise, raises assertion error.

	"""
	for row in range(8):
		for col in range(8):
			assert(test_piece.in_board(row,col))

	assert(not test_piece.in_board(-1,0))
	assert(not test_piece.in_board(0,8))
	assert(not test_piece.in_board(8,0))
	assert(not test_piece.in_board(8,8))


test_in_board()