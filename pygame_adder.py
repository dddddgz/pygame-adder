import pygame

class Error(BaseException):
    def __init__(self, message):
        """
        创建一个 Pygame Adder Error，用于在程序中随时检查不正确的参数，避免更多不可预料的 Bug。
        :param message: 报错信息
        """
        self._message = message
    
    def __str__(self):
        return self.message

def nothing(*args, **kwargs):
    """
    空函数，用于占位。
    """
    pass

# 正在跟踪的组件
_traced = []

def trace(component):
    """
    跟踪一个组件（即将组件记录为需要显示的组件）
    :param component: 组件，Component 类型
    """
    if component in _traced:
        raise Error(f"重复跟踪 {component}：它已经在 {_traced.index(component)} 位置被跟踪了")
    _traced.append(component)

def untrace(component):
    """
    取消跟踪一个组件（即将组件从需要显示的组件列表中移除）
    :param component: 组件，Component 类型
    """
    if component not in _traced:
        raise Error(f"{component} 没有被跟踪，因此无法被移除。")
    _traced.remove(component)

class Component(pygame.sprite.Sprite):
    def __init__(self, events, name):
        """
        Component，组件，程序中的每个交互元素（例如文本框等）都是组件。
        :param events: dict 类型，内容为：
            {
                "onclick":     nothing; # 鼠标单击
                "doubleclick": nothing; # 鼠标双击
            }
            其中，若有一些项目没有填写绑定的函数，则默认执行空函数。
        :param name: str，组件的名称
        """
        self._events = events
        # 如果字典中找不到这些内容，就设为空函数
        for item in ["onclick", "ondoubleclick"]:
            if item not in events:
                events[item] = nothing
        self._name = name
    
    def __getitem__(self, item):
        if item in self._events:
            return self._events[item]
        raise Error(f"{item} 不存在于事件列表中")

    def __repr__(self):
        return self._name
