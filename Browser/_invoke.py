import re


def determine_element(active, selector: str, only: bool = True):
    if is_frame_piercing_selector(selector):
        frame_selector, element_selector = split_frame_and_element_selector(selector)
        frame = find_frame(active, frame_selector)
        while is_frame_piercing_selector(element_selector):
            frame_selector, element_selector = split_frame_and_element_selector(element_selector)
            frame = find_frame(frame, frame_selector)
        elements = frame.query_selector_all(element_selector)
    else:
        elements = active.query_selector_all(selector)
    if only:
        if len(elements) == 0:
            return None
        return elements[0]
    else:
        return elements


def wait_for_element(active, selector: str, timeout: float = None):
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
    url = None
    name = None  # 初始化
    engine, selector = split_engine_and_selector(frame_selector)
    if engine == "url":
        url = selector
    if engine == "name":
        name = selector
    if type(parent).__name__ == "Page":
        content_frame = parent.frame(url=url, name=name)
    elif type(parent).__name__ == "Frame":
        content_frame = parent.page.frame(url=url, name=name)
    else:
        raise TypeError("参数 parent 应当是 Page 类型或 Frame 类型。")
    if content_frame is None:
        raise AssertionError(f"没有找到与选择器 {selector} 匹配的Frame。")
    return content_frame


def is_frame_piercing_selector(selector: str):
    return re.search(">>>", selector)


def split_frame_and_element_selector(selector: str):
    return selector.split(" >>> ", maxsplit=1)


def split_engine_and_selector(selector: str):
    engine, selector = selector.split("=", maxsplit=1)
    if selector.startswith("'") or selector.startswith('"'):
        selector = eval(selector)
    return engine, selector
