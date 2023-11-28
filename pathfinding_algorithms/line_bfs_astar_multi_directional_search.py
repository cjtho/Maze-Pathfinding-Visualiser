from .line_multi_directional_search import LineMultiDirectionalSearch


class LineBFSAStarMultiDirectionalSearch(LineMultiDirectionalSearch):
    def __init__(self, maze):
        super().__init__(maze)


def get_class():
    return LineBFSAStarMultiDirectionalSearch
