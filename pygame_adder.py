import pygame
import platform
from os import system
from time import perf_counter_ns

_config: dict = {}  # 程序的配置

_system = platform.system().lower() # 提前获取系统版本
quit = pygame.quit                  # 设置 quit() 函数，用于退出窗口

def nothing(*args, **kwargs):
    """
    空函数，用于占位。
    """
    pass

_traced = []    # 正在跟踪的组件

def initalize(size, bgcolor=(0, 0, 0), caption="Pygame Adder Window", icon="favicon.png") -> pygame.Surface:
    """
    初始化 Pygame
    :param size: 窗口大小
    :param bgcolor: 背景颜色
    :return: screen
    """
    pygame.init()
    screen = pygame.display.set_mode(size)
    set_background(new_surface(size, bgcolor))
    pygame.display.set_caption(caption)
    pygame.display.set_icon(to_surface(icon))
    return screen

def flush():
    """
    刷新屏幕上显示的所有内容
    """
    screen = pygame.display.get_surface()                       # 获取当前 screen
    screen.blit(_config["background"], (0, 0))                  # 在 screen 上绘制添加背景
    flag = False                                                # 是否已处理鼠标 hover 事件
    for component in _traced:                                   # 遍历已跟踪的 Component
        if hasattr(component, "flush"):                         # 如果 Component 有 flush() 函数
            component.flush()                                   # 刷新 Component
        screen.blit(component.image, component.rect)            # 绘制 Component
        if flag:                                                # 如果已经查找到鼠标悬浮的 Component
            continue                                            # 跳过本次循环剩余部分
        if component.rect.collidepoint(pygame.mouse.get_pos()): # 如果鼠标悬浮在 component 上方
            if hasattr(component, "_cursor"):                   # 如果 Component 有 _cursor 属性
                pygame.mouse.set_cursor(component._cursor)      # 设置鼠标样式
            flag = True                                         # 接下来的循环都跳过
            if pygame.mouse.get_pressed()[2]:                   # 如果鼠标按下了右键
                if hasattr(component, "right_menu"):            # 如果 Component 有右键菜单的属性
                    right_menu = component.right_menu           # 将右键菜单保存到变量里
                    if right_menu:                              # 如果右键菜单包含内容
                        surf = pygame.Surface((100, len(right_menu) * 20))
                                                                # 创建新的 Surface
                        font = pygame.font.SysFont("Microsoft Yahei UI", 15)
                        i = 0
                        for name, func in right_menu:           # 遍历右键菜单列表
                            surf.blit(font.render(name, False, (255, 255, 255)), (0, i * 20))
                            i += 1
                        screen.blit(surf, pygame.mouse.get_pos())
    if not flag:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    pygame.display.flip()

def to_surface(x):
    """
    将 `'path', Surface` 中的任何一个转换为 pygame.Surface 类型，如果表示路径，也可以是一张网络图片。
    :param x: 如上所述。
    :return: pygame.Surface
    """
    if isinstance(x, str):              # 是一张图片的路径 / 网络地址
        if x.startswith("http"):        # 是网络图片（http / https 开头）
            image_name = x.split('/')[-1]
            if _system == "windows":    system(f"curl {x} -o {image_name}") # windows 系统，使用 curl
            if _system == "darwin":     system(f"curl -O {x}")              # mac 系统，使用 curl
            if _system == "linux":      system(f"wget -O {image_name} {x}") # linux 系统，使用 wget
            x = to_surface(image_name)
            if _system == "windows":            system(f"del {image_name}") # windows 系统，使用 del
            if _system in ["darwin", "linux"]:  system(f"rm {image_name}")  # mac/linux，使用 rm
        else:
            x = pygame.image.load(x)    # 是本地图片
    return x

def new_surface(size, bgcolor) -> pygame.Surface:
    """
    使用背景色快速创建一个 Surface。
    :param size: Surface 大小。
    :param bgcolor: 背景颜色。
    :return: pygame.Surface
    """
    surface = pygame.Surface(size)
    surface.fill(bgcolor)
    return surface

def set_background(background):
    """
    设置清除屏幕时，显示的背景。
    :param background: 背景，只能是图像或图片路径/网络图片。
    """
    background = to_surface(background)
    _config["background"] = background

def trace(component):
    """
    跟踪一个组件（即将组件记录为需要显示的组件）
    :param component: 组件
    """
    _traced.append(component)

def untrace(component):
    """
    取消跟踪一个组件（即将组件从需要显示的组件列表中移除）
    :param component: 组件
    """
    _traced.remove(component)

class Component(pygame.sprite.Sprite):
    def __init__(self, events, image, right_menu, cursor=pygame.SYSTEM_CURSOR_ARROW):
        """
        Component 的意思为组件。它是所有 Pygame Adder 组件的基类。
        :param events: 表示所有事件。
            {
                event: function
            }
        :param image: 组件的图像
        :param right_menu: 右键菜单，[(item, func), ...]
        :param cursor: 当鼠标悬浮在 Component 上面时，显示的指针样式
        """
        if not isinstance(events, dict):
            raise f"events 参数存在错误：应该是 dict 类型，实际是 {str(type(events))[8:-2]}"
        self._events = events
        # 如果字典中找不到这些内容，就设为空函数
        for item in ["onclick", "ondoubleclick"]:
            if item not in events:
                events[item] = nothing
        self.origin_image = image
        self.image = image
        self.right_menu = right_menu
        self._cursor = cursor
        self._angle = 0
    
    def __getitem__(self, item):
        if item in self._events:
            return self._events[item]

    def flush(self):
        """
        由子类扩展，每个类型的组件的刷新逻辑都不一样
        """
        self._angle %= 360                  # 让自己的旋转角度对 360 取余
        pos = self.rect.center              # 保存当前图形的中心
        new_surf = pygame.transform.rotate(self.origin_image, self._angle)
                                            # 获取旋转后的新表面
        self.image = new_surf               # 设置表面
        self.rect = self.image.get_rect()   # 重新获取 rect
        self.rect.center = pos              # 设置 center

    def move_to(self, pos):
        """
        按照锚点移动位置
        :param pos: 新的坐标（中心点）
        """
        self.rect.center = pos
    
    def rotate(self, angle):
        """
        向逆时针旋转 angle 度
        :param angle: 旋转的度数
        """
        self._angle += angle

class Label(Component):
    def __init__(self, events, text, font, pos, fgcolor, bgcolor=None):
        """
        Label（标签）是 Pygame Adder 中的一个文字显示工具。
        :param events: 见 Component
        :param text: 标签上显示的文字
        :param font: 文字显示的字体
        :param pos: 组件的坐标
        :param fgcolor: 文字前景色（文字颜色）
        :param bgcolor: 文字背景色（不填默认为 None）
        """
        self._font = font
        self.image = font.render(text, False, fgcolor, bgcolor)
        super().__init__(events, self.image, [])
        self.rect = self.image.get_rect()
        self.rect.center = pos

class Button(Component):
    def __init__(self, events, text, font, pos, size, fgcolor, bgcolor, func=nothing):
        """
        Button（按钮）是 Pygame Adder 中的按钮，它可以接受鼠标点击事件，并为此做出反应。
        :param events: 见 Component
        :param text: 显示的文字
        :param font: 文字的字体
        :param pos: 按钮的坐标
        :param size: 按钮的大小 (width, height)
        :param fgcolor: 文字前景色（文字颜色）
        :param bgcolor: 文字背景色
        :param func: 当点击按钮时触发的函数（默认为 nothing）
        """
        self.image = new_surface(size, bgcolor)
        super().__init__(events, self.image, [], pygame.SYSTEM_CURSOR_HAND)
        text_surf = font.render(text, False, fgcolor)       # 按钮上的文字
        text_rect = text_surf.get_rect()                    # 给文字使用 Rect，便于固定在中心
        text_rect.center = (size[0] // 2, size[1] // 2)     # 设置中心点
        self._func = func                                   # 设置当点击时调用的函数
        self._last_clicked = perf_counter_ns()              # 上一次被点击的时间
        self.image.blit(text_surf, text_rect)               # 显示文字
        self.rect = self.image.get_rect()                   # 计算位置
        self.rect.topleft = pos                             # 设置位置
    
    def flush(self):
        """
        刷新对象
        """
        if self.rect.collidepoint(pygame.mouse.get_pos()):  # 鼠标移到了按钮上面
            if pygame.mouse.get_pressed()[0]:               # 鼠标左键按下
                last = self._last_clicked                   # 保留上次时间
                self._last_clicked = perf_counter_ns()      # 标记当前时间
                if self._last_clicked - last > 1_0000_0000: # 距离上一次按钮被点击超过了一亿纳秒（0.1 秒）
                    self._func()                            # 执行函数
