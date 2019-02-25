from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### listofasks = [self.kb.kb_ask(parse_input("fact: (on ?disk peg1)")),self.kb.kb_ask(parse_input("fact: (on ?disk peg2)")), self.kb.kb_ask(parse_input("fact: (on ?disk peg3)"))]
        peg1state=[]
        peg2state=[]
        peg3state=[]

        peg1ask = self.kb.kb_ask(parse_input("fact: (on ?disk peg1"))
        if peg1ask:
            for result in peg1ask:
                ###print('result: ')
                ###print(result)
                numb = int(result.bindings_dict['?disk'][-1])
                peg1state.append(numb)
        peg2ask = self.kb.kb_ask(parse_input("fact: (on ?disk peg2"))
        if peg2ask:
            for result in peg2ask:
                numb = int(result.bindings_dict['?disk'][-1])
                peg2state.append(numb)
        peg3ask = self.kb.kb_ask(parse_input("fact: (on ?disk peg3"))
        if peg3ask:
            for result in peg3ask:
                numb = int(result.bindings_dict['?disk'][-1])
                peg3state.append(numb)

        peg1state.sort()
        peg2state.sort()
        peg3state.sort()
        final = (tuple(peg1state), tuple(peg2state), tuple(peg3state))
        return final
         ### student code goes here
    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        mqstatement = self.produceMovableQuery().statement
        if match(movable_statement,mqstatement):
            bindings = match(movable_statement,mqstatement)
            disk = bindings.bindings_dict["?disk"]
            init = bindings.bindings_dict["?init"]
            target = bindings.bindings_dict["?target"]
        next_top = self.kb.kb_ask(parse_input("fact: (onTopOf " + disk + " ?bottom_disk)"))
        targetnotempty = self.kb.kb_ask(parse_input("fact: empty "+ target + " ?target_peg)"))
        if next_top: ###checks if current peg has two or more elements
            bottom = next_top[0].bindings_dict["?bottom_disk"]
            self.kb.kb_retract(parse_input("fact: (on " + disk + " " + init + ")"))
            ###self.kb.kb_retract(parse_input("fact: (top " + disk + " " + init + ")"))
            self.kb.kb_assert(parse_input("fact: (top " + bottom + " " + init + ")"))
            ###self.kb.kb_retract(parse_input("fact: (onTopOf " + disk + " " + bottom + ")"))
        else: #if one element
            self.kb.kb_assert(parse_input("fact: (empty " + init + ")"))
            ###self.kb.kb_retract(parse_input("fact: (top " + disk + " " + init + ")"))
            self.kb.kb_retract(parse_input("fact: (on " + disk + " " + init + ")"))
        if targetnotempty: # if target is not empty 
            oldtop = self.kb.kb_ask(parse_input("fact: (top ?oldtop " + target + ")"))[0].bindings_dict["?oldtop"]
            self.kb.kb_retract(parse_input("fact: (top " + oldtop + " " + target +")"))
            self.kb.kb_assert(parse_input("fact: (on " + disk + " "+ target + ")"))
            self.kb.kb_assert(parse_input("fact: top: " + disk + " " + target + ")"))
        else:  #if target is empty
            self.kb.kb_retract(parse_input("fact: (empty "+ target + ")"))
            self.kb.kb_assert(parse_input("fact: (on " + disk + " "+ target + ")"))
            self.kb.kb_assert(parse_input("fact: top: " + disk + " " + target + ")"))
    ### Student code goes here
    pass

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        row1state = [0,0,0]
        row2state = [0,0,0]
        row3state = [0,0,0]

        row1ask = self.kb.kb_ask(parse_input("fact: (coordinate ?tile ?row pos1"))
        for result in row1ask:
            tile = result.bindings_dict['?tile']
            row_coordinate = int(self.kb.kb_ask(parse_input("fact: (coordinate " + tile + " ?row pos1"))[0].bindings_dict["?row"][-1])
            if tile != 'empty':
                row1state[row_coordinate-1] = int(tile[-1])
            else:
                row1state[row_coordinate-1] = -1
        row2ask = self.kb.kb_ask(parse_input("fact: (coordinate ?tile ?row pos2"))
        for result in row2ask:
            tile = result.bindings_dict['?tile']
            row_coordinate = int(self.kb.kb_ask(parse_input("fact: (coordinate " + tile + " ?row pos2"))[0].bindings_dict["?row"][-1])
            ### row_coordinatev2 = self.kb.kb_ask(parse_input("fact: (coordinate " + tile + " ?row pos2"))
            ### tile_x = int(row_coordinatev2[0].bindings_dict["?row"][-1])
            ### print(tile_x)
            if tile != 'empty':
                row2state[row_coordinate-1] = int(tile[-1])
            else: 
                row2state[row_coordinate-1] = -1
        row3ask = self.kb.kb_ask(parse_input("fact: (coordinate ?tile ?row pos3"))
        for result in row3ask:
            tile = result.bindings_dict['?tile']
            row_coordinate = int(self.kb.kb_ask(parse_input("fact: (coordinate " + tile + " ?row pos3"))[0].bindings_dict["?row"][-1])
            if tile != 'empty':
                row3state[row_coordinate-1] = int(tile[-1])
            else: 
                row3state[row_coordinate-1] = -1
        final = (tuple(row1state),tuple(row2state),tuple(row3state))
        return final
        ### Student code goes here
        pass

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        print(movable_statement.terms)
        if movable_statement.predicate =="movable":
            tile = movable_statement.terms[0]
            cor1 = movable_statement.terms[1]
            cor2 = movable_statement.terms[2]
            cor3 = movable_statement.terms[3]
            cor4 = movable_statement.terms[4]
            self.kb.kb_retract(parse_input("fact: (coordinate " + str(tile) + " " + str(cor1) + " " + str(cor2) + ")" ))
            self.kb.kb_retract(parse_input("fact: (coordinate empty " + str(cor3) + " " + str(cor4) + ")" ))
            self.kb.kb_assert(parse_input("fact: (coordinate " + str(tile) + " " + str(cor3) + " " + str(cor4) + ")" ))
            self.kb.kb_assert(parse_input("fact: (coordinate empty" + " " + str(cor1) + " " + str(cor2) + ")" ))
        ### if match(mqstatement,mqstatement):
    ### Student code goes here

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
