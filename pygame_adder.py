import pygame
import typing
import platform

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
    :return: screen
    """
    pygame.init()
    return pygame.display.set_mode(size)

def flush():
    pygame.display.flip()
    for component in Component._components:
        component.flush()
        pygame.display.get_surface().blit(component.image, component.rect)

def clear(
        bg_image_or_color: typing.Union[str, pygame.Surface, tuple[int, int, int], list[int, int, int]],
        auto_resize: bool = False
    ):
    """
    清除屏幕。
    :param bg_image_or_color: 可以是 RGB 颜色值，或者 Surface 和图片路径。
    """
    screen = pygame.display.get_surface()
    if isinstance(bg_image_or_color, tuple) or isinstance(bg_image_or_color, list):
        # RGB 颜色值
        bg_color = tuple(bg_image_or_color)
        for i in range(3):
            color_i = bg_color[i]
            if not (0 <= color_i < 256 and isinstance(color_i, int)):
                # 不是正确的数
                raise Error(f"RGB 颜色值 {bg_color} 中的 {'RGB'[i]} 元素不正确")
        screen.fill(bg_color)
    elif isinstance(bg_image_or_color, str):
        # 是一张图片的名称
        bg_image = pygame.image.load(bg_image_or_color)
        if auto_resize:
            bg_image = pygame.transform.scale(bg_image, screen.get_size())
        screen.blit(bg_image, (0, 0))
    elif isinstance(bg_image_or_color, pygame.Surface):
        # 是一个 Surface
        bg_image = bg_image_or_color
        if auto_resize:
            bg_image = pygame.transform.scale(bg_image, screen.get_size())
        screen.blit(bg_image, (0, 0))
    else:
        raise Error(f"{bg_image_or_color} 的类型不正确：它只能为本地图片或者 RGB。")

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

class Font(pygame.font.Font):
    def __init__(
            self,
            font_name: str,
            size: int,
            bold: bool = False,
            italic: bool = False,
            underline: bool = False,
            fgcolor: tuple[int, int, int] = (0, 0, 0),
            bgcolor: typing.Union[type(None), tuple[int, int, int]] = None
    ):
        try:
            super().__init__(font_name, size)
        except FileNotFoundError:
            # 使用的是系统字体名称，而不是 .ttf 字体文件
            # 这里需要分情况（Windows、macOS 来看，后续可能会支持 Linux）
            if "windows" in platform.platform().lower():
                # Windows
                super().__init__(f"C:/Windows/Fonts/{font_name}", size)
        self.set_bold(bold)
        self.set_italic(italic)
        self.set_underline(underline)
        self._fgcolor = fgcolor
        self._bgcolor = bgcolor

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
            font: "Font",
            # anchor：预留
            pos: tuple[int, int] = (0, 0)
    ):
        super().__init__(events, text)
        self._font = font
        self.image = self._font.render(text, False, self._font._fgcolor, self._font._bgcolor)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
