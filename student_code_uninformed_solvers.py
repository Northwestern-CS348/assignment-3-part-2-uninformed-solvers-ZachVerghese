
from solver import *
from collections import deque
class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        
        curr_state = self.currentState
        moves = self.gm.getMovables()
        if self.victoryCondition == curr_state.state:
            return True
        for eachmove in self.gm.getMovables():
            self.gm.makeMove(eachmove)
            next_state = GameState(self.gm.getGameState(),self.currentState.depth +1, eachmove)
            curr_state.children.append(next_state)
            next_state.parent = curr_state
            self.gm.reverseMove(eachmove)
        for eachchild in curr_state.children:
            if eachchild not in self.visited:
                self.currentState = eachchild
                self.visited[eachchild] = True
                self.gm.makeMove(eachchild.requiredMovable)
                break
        return False

class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.queue = deque()
        self.path = []
        self.count = 0

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        current_state = self.currentState
        if current_state.state == self.victoryCondition:
            return True
        if current_state not in self.queue:
            if current_state:
                self.queue.append(current_state)
        self.visited[self.currentState] = True
        moves = self.gm.getMovables()
        if moves:
            if not current_state.children:
                for eachmove in moves:
                    self.gm.makeMove(eachmove)
                    new_state = self.gm.getGameState()
                    new_child = GameState(new_state, current_state.depth +1, eachmove)
                    new_child.parent = current_state
                    current_state.children.append(new_child)
                    if new_child not in self.visited:
                        self.visited[new_child] = False
                        if new_child not in self.queue:
                            self.queue.append(new_child)
                    self.gm.reverseMove(eachmove)
        self.queue.popleft()
        first_element = self.queue[0]
        exist = True
        while exist != False:
            self.path.append(first_element.requiredMovable)
            first_element = first_element.parent
            if first_element:
                if not first_element.parent:
                    exist = False
                else:
                    while current_state.parent:
                        self.gm.reverseMove(current_state.requiredMovable)
                        current_state = current_state.parent
                    for x in reversed(self.path):
                        self.gm.makeMove(x)
                    self.currentState = self.queue[0]
                    self.count = self.count +1
                    return False