
#--------------------starter code--------------------------------------------------------------------------
import sys
import NMM

BANNER = """
    __      _(_)_ __  _ __   ___ _ __| | |
    \ \ /\ / / | '_ \| '_ \ / _ \ '__| | |
     \ V  V /| | | | | | | |  __/ |  |_|_|
      \_/\_/ |_|_| |_|_| |_|\___|_|  (_|_)
"""


def input( prompt=None ):
   if prompt != None:
       print( prompt, end="" )
   aaa_str = sys.stdin.readline()
   aaa_str = aaa_str.rstrip( "\n" )
   print( aaa_str )
   return aaa_str


def count_mills(board, player):
    """
        Counts the number of mills formed by the given player on the board.
    Returns:
     count_mill: The number of mills formed by the player.
    """
    count_mill = 0
    for mill in board.MILLS:
        if all(board.points[point] == player for point in mill):
            count_mill += 1
    return count_mill


def place_piece_and_remove_opponents(board, player, destination):
    """
        Places a piece for the given player on the specified destination point.
    If a mill is formed by the placement, it removes one opponent's piece.

    """
    try:
        if board.points[destination.lower()] != ' ':
            raise RuntimeError("Invalid command: Destination point already taken")
        temp1 = count_mills(board, player)
        board.assign_piece(player, destination.lower())
        temp2 = count_mills(board, player)
        if temp2-temp1 > 0:
            print('A mill was formed!')
            print(board)
            remove_piece(board, get_other_player(player))
    except KeyError:
        raise RuntimeError("Invalid command: Not a valid point")

def move_piece(board, player, origin, destination):
    """
        Moves a piece for the given player from the specified origin point to the destination point.
    If a mill is formed by the movement, it removes one opponent's piece.

    """
    try:
        if board.points[origin] != player:
            raise RuntimeError("Invalid command: Origin point does not belong to player")
        elif board.points[destination] != ' ':
            raise RuntimeError("Invalid command: Destination point already taken")
        elif not check_adjacent(board,origin, destination):
            raise RuntimeError("Invalid command: Destination is not adjacent")
        board.clear_place(origin)
        temp1 = count_mills(board, player)
        board.assign_piece(player, destination)
        temp2 = count_mills(board, player)

        if temp2 - temp1 > 0:
            print('A mill was formed!')
            print(board)
            remove_piece(board, get_other_player(player))
    except KeyError:
        raise RuntimeError("Invalid command: Not a valid point")



def points_not_in_mills(board, player):
    """
        Returns the set of points belonging to the player that are not part of any mill.
    """
    placed_points = placed(board, player)
    mill_points = set()
    for mill in board.MILLS:
        if all(board.points[point] == player for point in mill):
            for point in mill:
                mill_points.add(point)
    non_mill_points = placed_points - mill_points
    return non_mill_points


def placed(board, player):
    """
        Returns a set of points on the board that belong to the given player.

    """
    placed = set()
    for point in board.points:
        if board.points[point] == player:
            placed.add(point)
    return placed

def check_adjacent(board,origin,destination):
    """Checks if two points on the board are adjacent
    """
    L = board.ADJACENCY[origin]
    if destination in L:
        return True
    return False

def remove_piece(board, player):
    """
        Removes a piece from the board for the given player.

    """
    try:
        valid_points = points_not_in_mills(board, player)
        while True:
            point_to_remove = input(f"Remove a piece at :> ").lower()

            if point_to_remove in valid_points:
                board.clear_place(point_to_remove)
                break
            elif point_to_remove in placed(board, player) and len(valid_points) == 0:
                board.clear_place(point_to_remove)
                break
            elif point_to_remove in placed(board, player)-valid_points:
                print("Invalid command: Point is in a mill")
                print("Try again.")
            elif len(point_to_remove) != 2:
                print("Invalid command: Not a valid point")
                print("Try again.")
            else:
                print("Invalid command: Point does not belong to player")
                print("Try again.")
    except KeyError:
        raise RuntimeError("Invalid command: Not a valid point")


def is_winner(board, player):
    """
        Checks if the given player is the winner, i.e., the opponent has less than three pieces on the board.
    """
    if len(placed(board, get_other_player(player))) < 3:
        return True
    else:
        return False


def get_other_player(player):
    """
    Get the other player.
    """
    if player == "X":
        return "O"
    else:
        return "X"

def main():
    # Loop so that we can start over on reset
    while True:
        # Setup stuff.
        print(RULES)
        print(MENU)
        board = NMM.Board()
        print(board)
        player = "X"
        placed_count = 0  # total of pieces placed by "X" or "O", includes pieces placed and then removed by opponent

        # PHASE 1
        print(player + "'s turn!")
        command = input("Place a piece at :> ").strip().lower()
        print()
        # Until someone quits or we place all 18 pieces...
        while command != 'q' and placed_count < 18:
            try:
                if len(command) == 2: #Place a piece and remove opponent's piece if a mill is formed
                    place_piece_and_remove_opponents(board, player, command.lower())
                    placed_count += 1
                    player = get_other_player(player)
                    print(board)
                    print(player + "'s turn!")
                elif command == 'r':
                    break  # Reset the game
                elif command == 'h':
                    print(MENU)
                elif command == 'q':
                    return
            except RuntimeError as error_message:
                print("{:s}\nTry again.".format(str(error_message)))
            # Prompt again
            if placed_count < 18:
                command = input("Place a piece at :> ").strip().lower()
            else:
                print("**** Begin Phase 2: Move pieces by specifying two points")
                command = input("Move a piece (source,destination) :> ").strip().lower()
            print()

        # Go back to top if reset
        if command == 'r':
            continue
        # PHASE 2 of game
        while command != 'q' and placed_count>=18:
            # commands should have two points
            command = command.split()
            try:
                if len(command) == 2:
                    move_piece(board, player, command[0].lower(), command[1].lower())
                    if is_winner(board, player):
                        print(BANNER)
                        return
                    player = get_other_player(player)

                elif command == 'q':
                    return  # Quit the game
                elif command == 'h':
                    print(MENU)
                elif command == 'r':
                    break
                else:
                    raise RuntimeError("Invalid number of points")
            except RuntimeError as error_message:
                print("{:s}\nTry again.".format(str(error_message)))

            print(board)
            print(player + "'s turn!")
            command = input("Move a piece (source,destination) :> ").strip().lower()
            print()

        # If we ever quit we need to return
        if command == 'q':
            return



if __name__ == "__main__":
    main()
