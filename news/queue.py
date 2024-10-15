from collections import deque
from .models import NewsThemes

class Queue():
    def __init__(self):
        self._container=deque()
    @property
    def empty(self):
        return not self._container

    def push(self,item):
        self._container.append(item)
    def pop(self):
        return self._container.popleft()
    def __repr__(self):
        return repr(self._container)
def get_theme_children(theme):
    frontier = Queue()
    frontier.push(theme)
    explored = {theme.id}

    while not frontier.empty:
        current_theme = frontier.pop()
        childrens = NewsThemes.objects.filter(parent=current_theme)
        for child in childrens:
            if child.id in explored:
                continue
            explored.add(child.id)
            frontier.push(child)
    return explored