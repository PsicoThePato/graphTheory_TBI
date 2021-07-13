class MatrixNode():
    def __init__(self, has_edge: int, weight: float):
        self.has_edge = has_edge
        self.weight = weight
    
    def __repr__(self):
        rep = f"MatrixNode(has_edge: {self.has_edge}, weight: {self.weight})"
        return rep

class ListNode():
    def __init__(self, links_to: int, weight: float):
        self.links_to = links_to
        self.weight = weight

    def __repr__(self):
        rep = f"ListNode(links_to: {self.links_to}, weight: {self.weight})"
        return rep
