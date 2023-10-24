import pygame
import typing
import platform
# 部分功能需要调用系统命令行
from os import system

# 程序的配置
config: dict = {}

# 定义 color 类型，用于表示一个颜色
color = typing.Union[list[int, int, int], tuple[int, int, int]]
# 定义 image 类型，用于表示一个表面
image = typing.Union[pygame.Surface, str]

# 提前获取系统版本
_system = platform.system().lower()

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
    if is_valid(bgcolor):
        screen.fill(bgcolor)
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
    pygame.display.flip()
    for component in Component._components:
        component.flush()
        pygame.display.get_surface().blit(component.image, component.rect)

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
                raise Error(f"未识别的系统：{_system}请前往 https://github.com/dddddgz/pygame-adder/issues 进行反馈。")
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
        is_valid(fgcolor)
        is_valid(bgcolor)
        self.image = self._font.render(text, False, fgcolor, bgcolor)
        self._anchor = anchor
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
