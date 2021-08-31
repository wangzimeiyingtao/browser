import re

from ._api_types import Error


def determine_element(active, selector: str, timeout: float = None):
    if is_frame_piercing_selector(selector):
        frame_selector, element_selector = split_frame_and_element_selector(selector)
        frame = find_frame(active, frame_selector)
        while is_frame_piercing_selector(element_selector):
            frame_selector, element_selector = split_frame_and_element_selector(element_selector)
            frame = find_frame(frame, frame_selector)
        return frame.wait_for_selector(element_selector, timeout=timeout)
    else:
        return active.wait_for_selector(selector, timeout=timeout)


def find_frame(parent, frame_selector: str):
    content_frame = None
    engine, selector = split_engine_and_selector(frame_selector)
    if type(parent).__name__ == "Page":
        child_frames = parent.main_frame.child_frames
    elif type(parent).__name__ == "Frame":
        child_frames = parent.child_frames
    else:
        raise TypeError("参数 parent 应当是 Page 类型或 Frame 类型。")
    for frame in child_frames:
        if selector == getattr(frame, engine):
            content_frame = frame
    if content_frame is None:
        no_such_frame = Error(f'根据选择器 {frame_selector} 没有找到Frame。')
        raise no_such_frame
    return content_frame


def is_frame_piercing_selector(selector: str):
    return re.search('>>>', selector)


def split_frame_and_element_selector(selector: str):
    return selector.split(' >>> ', maxsplit=1)


def split_engine_and_selector(selector: str):
    engine, selector = selector.split('=')
    if selector.startswith("'") or selector.startswith('"'):
        selector = eval(selector)
    return engine, selector
