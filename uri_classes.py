from TBI import Graph

class UriLabyrinth(Graph):
    def __init__(self):
        self.number_of_runs = None
        self.starting_point = None    
    
    def read_graph(self, path: str, represent_as="matrix"):
        with open(path) as fp:
            self.runs = self.__split_runs(fp)
    
    def __split_runs(self, fp):
        number_of_tests = int(fp.readline())
        lines = fp.readlines()
        E = 0
        total_lines_read = E
        repr_list = []
        current_bottom_limit = 2
        for _ in range(number_of_tests):
            starting_vertix = lines[current_bottom_limit - 2]
            V_E_line = lines[current_bottom_limit - 1]
            V, E = map(int, V_E_line.strip().split(" "))
            total_lines_read = total_lines_read + E + 2
            repr = self.AdjMatrix(V, False, lines[current_bottom_limit: total_lines_read])
            repr_list.append((starting_vertix, repr))
            current_bottom_limit = total_lines_read + 2
        return repr_list


if __name__ == '__main__':
    my_labyrinth = UriLabyrinth()
    my_labyrinth.read_graph('data/grafo_lab_n_m.txt')