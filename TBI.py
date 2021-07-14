from os import write
import argparse

import numpy as np

from ADTs.adt import ListNode, MatrixNode



class Graph:
    def __init__(self):
        self.graph_repr = None

    def __repr__(self) -> str:
        return str(self.graph_repr)

    def read_graph(self, path: str, represent_as="matrix"):
        with open(path) as fp:
            self.V, self.E = self.__get_V_E(fp)
            lines = fp.readlines()
            self.isDigraph = (
                True if fp.name.split("/")[-1].split("_")[0] == "digrafo" else False
            )
            self.graph_repr = (
                self.AdjMatrix(self.V, self.isDigraph, lines)
                if represent_as == "matrix"
                else self.AdjList(self.V, self.isDigraph, lines)
            )

    def __get_V_E(self, fp):
        while line := fp.readline():
            if line.strip()[0] != "c":
                return map(lambda x: int(x), line.split(" "))

    def write_file(self, path="data/output/"):
        file_name = "di" if self.isDigraph else ""
        file_name = file_name + "grafo"
        file_name = file_name + "v" if self.graph_repr.isValued else file_name
        file_name = file_name + "_n_m.dot" 
        
        with open(path+file_name, "w") as fp:
            fp.write(str(self))

    class AdjMatrix:
        def __init__(self, V: int, isDigraph, lines: str):
            self.header = "digraph G" if isDigraph else "graph G"
            self.isDigraph = isDigraph
            self.isValued = False
            self.graph_repr = self.__get_adj_matrix(lines, V, isDigraph)

        def __get_adj_matrix(self, lines: str, V: int, isDigraph):
            adj_matrix = [[MatrixNode(0, None) for _ in range(V)] for _ in range(V)]
            for line in lines:
                if line.strip()[0] == "c":
                    continue
                row, column, weight = map(lambda x: int(x), line.strip().split(" "))
                (adj_matrix[row - 1][column - 1]).has_edge = 1
                (adj_matrix[row - 1][column - 1]).weight = weight
                if weight != 0:
                    self.isValued = True
                if not isDigraph:
                    pass
                    # self.__add_simetric_edge(adj_matrix, row, column, weight)
            return adj_matrix

        def __add_simetric_edge(self, adj_matrix, row, column, weight):
            adj_matrix[column - 1][row - 1] = MatrixNode(1, weight)

        def __repr__(self) -> str:
            body = self.__get_formatted_graph()
            formated_string = self.header + "\n" + "{\n" + body + "}\n"
            return formated_string

        def __get_formatted_graph(self):
            separator = " -> " if self.isDigraph else " -- "
            get_weigth_str = (lambda weight: f" [label = {weight}]") if self.isValued else lambda _: ""
            get_col_range = lambda idx, matrix_dimension: range(0, matrix_dimension) if self.isDigraph else range(idx, matrix_dimension)
            
            body = ""
            matrix_dimension = len(self.graph_repr)
            for row_idx in range(matrix_dimension):
                for col_idx in get_col_range(row_idx, matrix_dimension):
                    if self.graph_repr[row_idx][col_idx].has_edge:
                        _from = str(row_idx + 1)
                        _to = str(col_idx + 1)
                        weight = self.graph_repr[row_idx][col_idx].weight
                        body = body + _from + separator + _to + get_weigth_str(weight) +";\n"
            return body

    class AdjList:
        def __init__(self, V: int, isDigraph, lines: str):
            self.header = "digraph G" if isDigraph else "graph G"
            self.isDigraph = isDigraph
            self.isValued = False
            self.graph_repr = self.__get_adj_list(lines, V, isDigraph)

        def __get_adj_list(self, lines: str, V: int, isDigraph):
            adj_list = [[] for _ in range(V)]
            for line in lines:
                if line.strip()[0] == "c":
                    continue
                row, column, weight = map(lambda x: int(x), line.strip().split(" "))
                adj_list[row - 1].append(ListNode(column - 1, weight))
                if weight != 0:
                    self.isValued = True
                if not isDigraph:
                    pass
                    # self.__add_simetric_edge(adj_list, row, column, weight)

            return adj_list

        def __add_simetric_edge(self, adj_list, row, column, weight):
            adj_list[column - 1].append(ListNode(row - 1, weight))

        def __get_formatted_graph(self):
            body = ""
            separator = " -> " if self.isDigraph else " -- "
            get_weigth_str = (lambda weight: f" [label = {weight}]") if self.isValued else lambda _: ""
                
            for from_vertix, to_list in enumerate(self.graph_repr):
                for to_vertix in to_list:
                    body = (
                        body
                        + str(from_vertix + 1)
                        + separator
                        + str(to_vertix.links_to + 1)
                        + get_weigth_str(to_vertix.weight)
                        + ";\n"
                    )
            return body

        def __repr__(self) -> str:
            body = self.__get_formatted_graph()
            formated_string = self.header + "\n" + "{\n" + body + "}\n"
            return formated_string


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', action='store', required=True)
    parser.add_argument('-r', choices=['matrix', 'list'], action='store')
    arg_dict = vars(parser.parse_args())
    file_path, represent_as = arg_dict['f'], arg_dict['r']
    
    my_graph = Graph()
    my_graph.read_graph(file_path)
    my_graph.write_file()

