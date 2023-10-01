import pygame
import typing

# 程序的配置
config: dict = {}

# 定义 color 类型
color = typing.Union[list[int, int, int], tuple[int, int, int]]

class Error(BaseException):
    def __init__(
            self,
            message: str
        ):
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

def initalize(
        size: typing.Union[tuple[int, int], list[int, int]]
    ) -> pygame.Surface:
    """
    初始化 Pygame
    :param size: 窗口大小
    :param bgcolor: 背景颜色
    :return: screen
    """
    pygame.init()
    return pygame.display.set_mode(size)

def flush():
    """
    刷新屏幕上显示的所有内容
    """
    pygame.display.flip()
    for component in Component._components:
        component.flush()
        pygame.display.get_surface().blit(component.image, component.rect)

def to_surface(
        x: typing.Union[color, str, pygame.Surface]
    ):
    """
    将 `[r, g, b], (r, g, b), 'path', Surface` 中的任何一个转换为 pygame.Surface 类型。
    :param x: 如上所述。
    :return: pygame.Surface
    """
    if isinstance(x, tuple) or isinstance(x, list):
        # RGB 颜色值
        x = tuple(x)
        if len(x) != 3:
            raise Error(f"RGB 颜色值 {x} 的长度为 {len(x)} 而不是 3")
        for i in range(3):
            color_i = x[i]
            if not (0 <= color_i < 256 and isinstance(color_i, int)):
                # 不是正确的数
                raise Error(f"RGB 颜色值 {x} 中的 {'RGB'[i]} 元素不正确")
    elif isinstance(x, str):
        # 是一张图片的名称
        x = pygame.image.load(x)
    elif isinstance(x, pygame.Surface):
        # 是一个 Surface
        x = x
    else:
        raise Error(f"{x} 的类型不正确：它只能为本地图片或者 RGB。")

def set_background(background, autoresize):
    """
    设置清除屏幕时，显示的背景。
    :param background: 背景，可以是 RGB 或者图像。
    """
    background = to_surface(background)
    config["background"] = [background, autoresize]

def trace(
        component: "Component"
    ):
    """
    跟踪一个组件（即将组件记录为需要显示的组件）
    :param component: 组件
    """
    if component in _traced:
        raise Error(f"重复跟踪 {component}：它已经在 {_traced.index(component)} 位置被跟踪了")
    _traced.append(component)

def untrace(
        component: "Component"
    ):
    """
    取消跟踪一个组件（即将组件从需要显示的组件列表中移除）
    :param component: 组件
    """
    if component not in _traced:
        raise Error(f"{component} 没有被跟踪，因此无法被移除。")
    _traced.remove(component)

class Component(pygame.sprite.Sprite):
    # 所有组件
    _components: list["Component"] = []

    def __init__(
            self,
            events: dict,
            name: str
    ):
        """
        https://github.com/dddddgz/pygame-adder/wiki/Component
        """
        if not isinstance(events, dict):
            raise f"events 参数存在错误：应该是 dict 类型，实际是 {str(type(events))[8:-2]}"
        self._events = events
        # 如果字典中找不到这些内容，就设为空函数
        for item in ["onclick", "ondoubleclick"]:
            if item not in events:
                events[item] = nothing
        self._name = name
        Component._components.append(self)
    
    def __getitem__(self, item):
        if item in self._events:
            return self._events[item]
        raise Error(f"{item} 不存在于事件列表中")

    def __repr__(self):
        return self._name

    def flush(self):
        """
        为了将来的需求预留
        """
        pass

class Label(Component):
    def __init__(
            self,
            events: dict,
            text: str,
            font: pygame.font.Font,
            pos: tuple[int, int],
            fgcolor: color,
            bgcolor: typing.Union[color, type(None)] = None,
            anchor: str = "topleft"
    ):
        super().__init__(events, text)
        self._font = font
        self.image = self._font.render(text, False, fgcolor, bgcolor)
        self._anchor = anchor
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
