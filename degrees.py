import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 3:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) >= 2 else "large"
    type = sys.argv[2] if len(sys.argv) >= 3 else "1"


    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")
    isStarting = True

    while isStarting:
        source = None
        target = None

        while source is None:
            source = person_id_for_name(input("Name: "))
            if source is None:
                print("Person not found.")
        

        while target is None:
            target = person_id_for_name(input("Name: "))
            if target is None:
                print("Person not found.")

        
        path = shortest_path(source, target, type)
        print("Done computing!")

        if path is None:
            print("Not connected.")
        else:
            degrees = len(path)
            print(f"{degrees} degrees of separation.")
            print("\nPath : {}".format(path))
            path = [(None, source)] + path
            for i in range(degrees):
                person1 = people[path[i][1]]["name"]
                person2 = people[path[i + 1][1]]["name"]
                movie = movies[path[i + 1][0]]["title"]
                print(f"{i + 1}: {person1} and {person2} starred in {movie}")

        wantToContinue = input("Do you want to continue using the application? (Y/N)")
        if(wantToContinue is not None and wantToContinue.lower() == "y"):
            isStarting = True
            newType = input("Select the method to use? \n(1 = 'Depth-First Search (DFS)', 2 = 'Breadth-First Search (BFS)')")
            if newType is not None and newType.lower() == "2":
                type = "2"
            else:
                type = "1"
        else:
            isStarting = False


def shortest_path(source, target, type= "1"):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
    """Finds a solution to maze, if one exists."""

    # Keep track of number of states explored
    num_explored = 0

    # Initialize frontier to just the starting position
    start = Node(state=source, parent=None, action=None)
    if type == 2 or type == "2":
        frontier = QueueFrontier()
        print("Using Breadth-First Search (BFS)")
    else:
        frontier = StackFrontier()
        print("Using Depth-First Search (DFS)")

    frontier.add(start)

    # Initialize an empty explored set
    explored = set()
    exploredAction = set()

    # Keep looping until solution found
    print("Source : {}\nTarget : {}".format(source, target))
    # print("Target : {}".format(target))
    found = False
    # while num_explored < 30:
    print("Computing ...")
    # time.sleep(1)
    while not found:

        # If nothing left in frontier, then no path
        if frontier.empty():
            # raise Exception("no solution")
            return None

        # Choose a node from the frontier
        node = None
        while node is None or node.depth() > 6:
            try:
                node = frontier.remove()
            except Exception:
                found = True
                continue
            

        num_explored += 1
        # print("Node state : {}\nDepth : {}".format(node.state, node.depth()))
        # If node is the goal, then we have a solution
    
        if node.state == target:
            print("Found target")
            saved_node = node
            # actions = []
            # cells = []
            solutions = []
            while node.parent is not None:
                # actions.append(node.action)
                # cells.append(node.state)
                solutions.append((node.action, node.state))
                node = node.parent
            # actions.reverse()
            # cells.reverse()
            # print("\nActions : {}".format(actions))
            # print("Cells : {}".format(cells))
            solutions.reverse()
            # print("Solutions : {}".format(solutions))
            if(len(solutions) < 7):
                found = True
                return solutions
            else:
                node = saved_node

        # Mark node as explored
        explored.add(node.state)
        exploredAction.add(node.action)

        # Add neighbors to frontier
        for action, state in neighbors_for_person(node.state):
            # print("\n-------Neighours-------- \nAction : {}, State : {}".format(action, state))
            if not frontier.contains_state(state) and action not in exploredAction and state not in explored:
                # print("---------\nTraversing \nAction : {}".format(action))
                # print("State : {}\n".format(state))
                child = Node(state=state, parent=node, action=action)
                # print("Adding to frontier\n")
                # child.print()
                frontier.add(child)
        
        # frontier.print()
        # print("frontier size = {}\n".format(frontier.size()))
        # if frontier.size() == 0:
        #     found = True

    return None
    # TODO
    # raise NotImplementedError


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
