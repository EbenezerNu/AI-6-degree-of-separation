class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

    def print(self):
        if self is None:
            print("Node is empty")
        else:
            print("({}, {})".format(self.action, self.state))
    
    def depth(self):
        if self is None:
            return 0
        elif self.parent is None:
            return 1
        else:
            return 1 + self.parent.depth()


class StackFrontier():
    def __init__(self):
        self.frontier = []

    def size(self):
        return len(self.frontier)

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)
    
    def contains_action(self, action):
        return any(node.action == action for node in self.frontier)
    
    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node

    def print(self):
        print("Current frontier\n----------------\nFormat : (action, state, parent)\n")
        for i in range(len(self.frontier)):
            print("item {}".format(i+1))
            self.frontier[i].print()
    

class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node
