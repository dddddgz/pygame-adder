import pygame
import typing
import platform
from os import system
from time import perf_counter_ns

# 程序的配置
_config: dict = {}

NoneType = type(None)
color = typing.Union[list[int, int, int], tuple[int, int, int]] # 用于表示一个颜色
image = typing.Union[pygame.Surface, str]                       # 用于表示一个表面

_system = platform.system().lower()     # 提前获取系统版本
quit = pygame.quit

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
        return self._message

def nothing(*args, **kwargs):
    """
    空函数，用于占位。
    """
    pass

# 正在跟踪的组件
_traced = []

def initalize(
        size: typing.Union[tuple[int, int], list[int, int]],
        bgcolor: color = (0, 0, 0),
        caption: str = "Pygame Adder Window",
        icon: pygame.Surface = "favicon.png",
    ) -> pygame.Surface:
    """
    初始化 Pygame
    :param size: 窗口大小
    :param bgcolor: 背景颜色
    :return: screen
    """
    pygame.init()
    screen = pygame.display.set_mode(size)
    try:
        is_valid(bgcolor, "color")  # 是颜色，不是背景图片
        set_background(new_surface(size, bgcolor))
    except:
        # 不是颜色，那么检查是不是背景图
        raise
    pygame.display.set_caption(caption)
    pygame.display.set_icon(to_surface(icon))
    return screen

def is_valid(value, format):
    """
    检查某个值是否符合正确格式，如果不符合直接 raise 报错
    :param value: 值
    :param format: 格式
    """
    if format == "color":
        # 是元组或列表
        if isinstance(value, tuple) or isinstance(value, list):
            # 长度正常
            if len(value) == 3:
                # 都是整数
                if isinstance(value[0], int) and isinstance(value[1], int) and isinstance(value[2], int):
                    # 正常
                    return True
                # 不是整数
                else:
                    raise Error(f"{value} 中的某个/某些值不是整数")
            # 长度异常
            else:
                raise Error(f"{value} 的长度应该是 3，而不是 {len(value)}")
        # 格式错误
        else:
            raise Error(f"{value} 的类型应该是 tuple 或 list，而不是 {type(value)}")

def flush():
    """
    刷新屏幕上显示的所有内容
    """
    # 先获取系统背景
    screen = pygame.display.get_surface()
    screen.blit(_config["background"], (0, 0))
    for component in _traced:
        component.flush()
        screen.blit(component.image, component.rect)
    pygame.display.flip()

def to_surface(
        x: image
    ):
    """
    将 `'path', Surface` 中的任何一个转换为 pygame.Surface 类型，如果表示路径，也可以是一张网络图片。
    :param x: 如上所述。
    :return: pygame.Surface
    """
    if isinstance(x, str):
        # 是一张图片的名称
        if x.startswith("http"):
            # 是网络图片
            image_name = x.split('/')[-1]
            if _system == "windows":
                # windows 系统，使用 curl
                system(f"curl {x} -o {image_name}")
            elif _system == "darwin":
                # mac 系统，使用 curl
                system(f"curl -O {x}")
            elif _system == "linux":
                # linux 系统，使用 wget
                system(f"wget -O {image_name} {x}")
            else:
                raise Error(f"未识别的系统：{_system}。请前往 https://github.com/dddddgz/pygame-adder/issues 进行反馈。")
            x = to_surface(image_name)
            if _system == "windows":
                system(f"del {image_name}")
            elif _system == "darwin":
                system(f"rm {image_name}")
            elif _system == "linux":
                system(f"rm {image_name}")
        else:
            # 是本地图片
            x = pygame.image.load(x)
    elif isinstance(x, pygame.Surface):
        # 是一个 Surface
        x = x
    else:
        raise Error(f"{x} 的类型不正确：它只能为图片。")
    return x

def new_surface(
        size: tuple[int, int],
        bgcolor: color
    ) -> pygame.Surface:
    """
    使用背景色快速创建一个 Surface。
    :param size: Surface 大小。
    :param bgcolor: 背景颜色。
    :return: pygame.Surface
    """
    surface = pygame.Surface(size)
    surface.fill(bgcolor)
    return surface

def set_background(
        background: pygame.Surface
    ):
    """
    设置清除屏幕时，显示的背景。
    :param background: 背景，只能是图像或图片路径/网络图片。
    """
    background = to_surface(background)
    _config["background"] = background

def trace(
        component: "Component"
    ):
    """
    跟踪一个组件（即将组件记录为需要显示的组件）
    :param component: 组件
    """
    if component in _traced:
        raise Error(f"重复跟踪 {component}：它已经在 {_traced.index(component)} 位置被跟踪了。")
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
    
    def __getitem__(self, item):
        if item in self._events:
            return self._events[item]
        raise Error(f"{item} 不存在于事件列表中")

    def __repr__(self):
        return self._name

    def flush(self):
        """
        由子类写，Component.flush() 用来摸鱼
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
        """
        https://github.com/dddddgz/pygame-adder/wiki/Label
        """
        super().__init__(events, text)
        self._font = font
        is_valid(fgcolor, "color")
        if bgcolor is not None:
            is_valid(bgcolor, "color")
        self.image = self._font.render(text, False, fgcolor, bgcolor)
        self._anchor = anchor
        self.rect = self.image.get_rect(**{anchor: pos})
    
    def flush(self):
        """
        刷新对象
        """
        anchor_pos = self.rect.__getattribute__(self._anchor)
        self.rect = self.image.get_rect()
        self.rect.__setattr__(self._anchor, anchor_pos)

class Button(Component):
    def __init__(self,
        events: dict,
        name: str,
        text: str,
        font: pygame.font.Font,
        pos: tuple[int, int],
        size: tuple[int, int],
        fgcolor: color,
        bgcolor: color,
        func,
        anchor: str = "topleft",
    ):
        super().__init__(events, name)
        is_valid(fgcolor, "color")
        if bgcolor is not None:
            is_valid(bgcolor, "color")
        self.image = new_surface(size, bgcolor)
        text_surf = font.render(text, False, fgcolor)   # 按钮上的文字
        text_rect = text_surf.get_rect()                # 给文字使用 Rect，便于固定在中心
        text_rect.center = (size[0] // 2, size[1] // 2) # 设置中心点
        self._func = func
        self._last_clicked = perf_counter_ns()
        self.image.blit(text_surf, text_rect)
        self._anchor = anchor
        self.rect = self.image.get_rect(**{anchor: pos})
    
    def flush(self):
        """
        刷新对象
        """
        anchor_pos = self.rect.__getattribute__(self._anchor)
        self.rect = self.image.get_rect()
        self.rect.__setattr__(self._anchor, anchor_pos)
        if self.rect.collidepoint(pygame.mouse.get_pos()):  # 鼠标移到了按钮上面
            if pygame.mouse.get_pressed()[0]:               # 鼠标左键按下
                last = self._last_clicked                   # 保留上次时间
                self._last_clicked = perf_counter_ns()      # 标记当前时间
                if self._last_clicked - last > 1_0000_0000: # 距离上一次按钮被点击超过了一亿纳秒（0.1 秒）
                    self._func()                            # 执行函数
        #    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        # else:
        #     pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
