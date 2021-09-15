import sys

if sys.version_info >= (3, 8):  # pragma: no cover
    from typing import Literal, Optional, List, Dict, Union
else:  # pragma: no cover
    from typing import Optional, List, Dict, Union
    from typing_extensions import Literal

from ._api_structures import Position
from ._api_types import Error
from ._invoke import determine_element, wait_for_element

NoneType = type(None)


class Interaction:
    def __init__(self, obj):
        self._obj = obj

    def __getattr__(self, item):
        if self.__dict__.get(item):
            return self.item()
        else:
            return getattr(self._obj, item)

    def _find_element_cross_frame(self, selector: str, only=True):
        """跨frame搜索元素。
        :param only:
        :param selector: 元素定位器。
        """
        return determine_element(self._obj, selector=selector, only=only)

    def check(
            self,
            selector: str,
            *,
            force: bool = None,
            no_wait_after: bool = None,
            position: Position = None,
            timeout: float = None
    ) -> NoneType:
        """选择复选框或单选按钮。

        :param selector: 用于搜索元素的选择器。 如果有多个元素满足选择器，将使用第一个。
        :param force: 是否绕过可操作性检查。 默认为 false。
        :param no_wait_after: 启动导航的操作正在等待这些导航发生并等待页面开始加载。
            可以通过设置此标志选择退出等待。
            只需要在特殊情况下使用此选项，例如导航到无法访问的页面。
            默认为 false。
        :param position: 相对于元素填充框的左上角使用的点。 如果未指定，则使用元素的一些可见点。
        :param timeout: 以毫秒为单位的最长时间，默认为 30 秒，传递 0 以禁用超时。可以使用
            browser_context.set_default_timeout(timeout)
            或 page.set_default_timeout(timeout) 方法更改默认值。
        """
        element = self._find_element_cross_frame(selector)
        element.check(
            force=force,
            no_wait_after=no_wait_after,
            position=position,
            timeout=timeout
        )

    def click(
            self,
            selector: str,
            *,
            button: Literal["left", "middle", "right"] = None,
            click_count: int = None,
            delay: float = None,
            force: bool = None,
            modifiers: Optional[
                List[Literal["Alt", "Control", "Meta", "Shift"]]
            ] = None,
            no_wait_after: bool = None,
            position: Position = None,
            timeout: float = None,
    ) -> NoneType:
        """此方法单击匹配选择器的元素。

        :param selector: 用于搜索元素的选择器。 如果有多个元素满足选择器，将使用第一个。
        :param button: 鼠标的左、中（滚轮）、右按键。默认为左。
        :param click_count: 默认为 1。
        :param delay: 在 mousedown 和 mouseup 之间等待的时间（以毫秒为单位）。 默认为 0。
        :param force: 是否绕过可操作性检查。 默认为 false。
        :param modifiers: 要按下的修饰键。 确保在操作期间仅按下这些修饰符，然后将当前修饰符恢复回来。 如果未指定，则使用当前按下的修饰符。
        :param no_wait_after: 启动导航的操作正在等待这些导航发生并等待页面开始加载。 你可以通过设置此标志选择退出等待。
            只需要在特殊情况下使用此选项，例如导航到无法访问的页面。 默认为 false。
        :param position: 相对于元素填充框的左上角使用的点。 如果未指定，则使用元素的一些可见点。
            x <float>
            y <float>
        :param timeout: 以毫秒为单位的最长时间，默认为 30 秒，传递 0 以禁用超时。
            可以使用 browser_context.set_default_timeout(timeout) 或 page.set_default_timeout(timeout) 方法更改默认值。
        """
        element = self._find_element_cross_frame(selector)
        element.click(
            button=button,
            click_count=click_count,
            delay=delay,
            force=force,
            modifiers=modifiers,
            no_wait_after=no_wait_after,
            position=position,
            timeout=timeout
        )

    def cell_text(self, *, column_header: str = None, row_header: str = None):
        """根据列标题 `column_header` 和行标题 `row_header` 获得文本值。
        仅提供行标题 `row_header` 时，将获得其右侧最近的一个文本值。

        :param column_header: 列标题。
        :param row_header: 行标题。
        """
        if column_header is None:
            element_handler = self._obj.query_selector(f"*:right-of(:text('{row_header}'))")
            if element_handler is None:
                raise Error(f"未找到匹配行标题 {row_header} 的元素。")
            return element_handler.inner_text()
        column_header_handler = self._obj.query_selector(f"text='{column_header}' >> visible=true")
        row_header_handler = self._obj.query_selector(f"text='{row_header}' >> visible=true")
        x = column_header_handler.bounding_box()["x"] + column_header_handler.bounding_box()["width"] / 2
        y = row_header_handler.bounding_box()["y"] + row_header_handler.bounding_box()["height"] / 2
        return self._obj.evaluate_handle(f"document.elementFromPoint({x},{y}).innerText")

    def dblclick(
            self,
            selector: str,
            *,
            modifiers: Optional[
                List[Literal["Alt", "Control", "Meta", "Shift"]]
            ] = None,
            position: Position = None,
            delay: float = None,
            button: Literal["left", "middle", "right"] = None,
            timeout: float = None,
            force: bool = None,
            no_wait_after: bool = None,
    ) -> NoneType:
        """双击匹配选择器的元素。

        :param selector: 用于搜索元素的选择器。 如果有多个元素满足选择器，将使用第一个。
        :param button: 鼠标的左、中（滚轮）、右按键。默认为左。
        :param delay: 在 mousedown 和 mouseup 之间等待的时间（以毫秒为单位）。 默认为 0。
        :param force: 是否绕过可操作性检查。 默认为 false。
        :param modifiers: 要按下的修饰键。 确保在操作期间仅按下这些修饰符，然后将当前修饰符恢复回来。 如果未指定，则使用当前按下的修饰符。
        :param no_wait_after: 启动导航的操作正在等待这些导航发生并等待页面开始加载。 你可以通过设置此标志选择退出等待。
            只需要在特殊情况下使用此选项，例如导航到无法访问的页面。 默认为 false。
        :param position: 相对于元素填充框的左上角使用的点。 如果未指定，则使用元素的一些可见点。
            x <float>
            y <float>
        :param timeout: 以毫秒为单位的最长时间，默认为 30 秒，传递 0 以禁用超时。
            可以使用 browser_context.set_default_timeout(timeout) 或 page.set_default_timeout(timeout) 方法更改默认值。
        """
        element = self._find_element_cross_frame(selector)
        element.dblclick(
            selector=selector,
            modifiers=modifiers,
            position=position,
            delay=delay,
            button=button,
            timeout=timeout,
            force=force,
            no_wait_after=no_wait_after,
        )

    def dispatch_event(
            self,
            selector: str,
            *,
            event_type: str = None,
            event_init: Dict = None,
    ) -> NoneType:
        """触发事件。

        下面的代码片段在元素上调度点击事件。
        无论元素的可见性状态如何，点击事件都会被调度。
        这等同于调用
        [element.click()](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/click)。

        ```py
        page.dispatch_event(\"button#submit\", \"click\")
        ```

        在后台，它根据给定的 `type` 创建一个事件实例，并使用 `eventInit` 属性对其进行初始化
        并在元素上调度它。事件默认为“已组合”、“可取消”和“冒泡”。

        如果你希望将活动对象传递到事件中，还可以指定 `JSHandle` 作为属性值：
        ```py
        # 请注意，只能在 Chromium 和 firefox 中创建 data_transfer
        data_transfer = page.evaluate_handle(\"new DataTransfer()\")
        page.dispatch_event(\"#source\", \"dragstart\", { \"dataTransfer\": data_transfer })
        ```

        :param selector: 用于搜索元素的选择器。 如果有多个元素满足选择器，将使用第一个。
        :param event_type: DOM 事件类型：“click”、“dragstart”等。
        :param event_init: 可选的特定于事件的初始化属性。
        """
        element = self._find_element_cross_frame(selector)
        element.dispatch_event(
            type=event_type,
            event_init=event_init,
        )

    def drag_and_drop(
            self,
            source: str,
            target: str,
            source_position: Position = None,
            target_position: Position = None,
            timeout: float = None,
    ):
        """执行从 `selector_from` 选择的元素到 `selector_to` 选择的元素的拖放操作。
        该方法不支持跨Frame搜索元素

        :param source: 起点元素
        :param target: 终点元素
        :param source_position: 在该点相对于元素的填充框的左上角单击源元素。 如果未指定，则使用元素的某些可见点。
        :param target_position: 此时相对于元素填充框的左上角落在目标元素上。 如果未指定，则使用元素的某些可见点。
        :param timeout: 以毫秒为单位的最长时间，默认为 30 秒，传递 0 以禁用超时。可以使用
            browser_context.set_default_timeout(timeout)
            或 page.set_default_timeout(timeout) 方法更改默认值。
        """
        if ">>>" in source or ">>>" in target:
            unsupported_selector_engine = Error("该方法不支持跨 Frame 搜索语法。")
            raise unsupported_selector_engine
        self._obj.drag_and_drop(
            source=source,
            target=target,
            source_position=source_position,
            target_position=target_position,
            timeout=timeout,
        )

    def fill(
            self,
            selector: str,
            value: str,
            *,
            no_wait_after: bool = None,
            timeout: float = None,
            clear: bool = True,
    ) -> NoneType:
        """清空 `selector` 找到的文本字段，然后使用 `value` 填充它。
        此方法等待元素匹配选择器，等待可操作性检查，聚焦元素，填充它并在填充后触发输入事件。
        如果匹配选择器的元素不是 input 、textarea 或 contenteditable 元素，则此方法会引发错误。

        :param selector: 用于搜索元素的选择器。 如果有多个元素满足选择器，将使用第一个。
        :param value: 为 input 、textarea 或 contenteditable 元素填充的值。
        :param no_wait_after: 启动导航的操作正在等待这些导航发生并等待页面开始加载。
            可以通过设置此标志选择退出等待。
            只需要在特殊情况下使用此选项，例如导航到无法访问的页面。
            默认为 false。
        :param timeout: 以毫秒为单位的最长时间，默认为 30 秒，传递 0 以禁用超时。可以使用
            browser_context.set_default_timeout(timeout)
            或 page.set_default_timeout(timeout) 方法更改默认值。
        :param clear: 如果在填充之前不应清除该字段，则设置为 false。 默认为 true。
        """
        element = self._find_element_cross_frame(selector)
        if clear:
            # 清空
            element.fill(
                value='',
                force=True,
                no_wait_after=no_wait_after,
                timeout=timeout,
            )
        # 填充
        element.fill(
            value=value,
            force=True,
            no_wait_after=no_wait_after,
            timeout=0,
        )

    def focus(self, selector: str):
        """此方法使用选择器 `selector` 获取元素并聚焦它。
        如果没有与选择器匹配的元素，该方法将等待匹配元素出现在 DOM 中。

        :param selector: 用于搜索元素的选择器。 如果有多个元素满足选择器，将使用第一个。
        """
        element = self._find_element_cross_frame(selector)
        element.focus()

    def get_attribute(self, selector: str, name: str) -> Union[NoneType, str]:
        """返回元素属性值。

        :param selector: 用于搜索元素的选择器。 如果有多个元素满足选择器，将使用第一个。
        :param name: 要获取其值的属性名称。
        """
        element = self._find_element_cross_frame(selector)
        return element.get_attribute(name)

    def go_back(
            self,
            timeout: float = None,
            wait_until: Literal["domcontentloaded", "load", "networkidle"] = None
    ):
        """导航到历史记录的上一页。
        返回主要资源响应。
        在多次重定向的情况下，导航将使用上次重定向的响应进行解析。
        如果不能返回，则返回 null。

        :param timeout:最大操作时间以毫秒为单位，默认为 30 秒，传递 0 以禁用超时。
            可以使用 browser_context.set_default_navigation_timeout(timeout)、
            browser_context.set_default_timeout(timeout)、
            page.set_default_navigation_timeout(timeout)
            或 page.set_default_timeout(timeout) 方法更改默认值。
        :param wait_until: <"load"|"domcontentloaded"|"networkidle"> 当认为操作成功时，默认加载。 事件可以是：#
            'domcontentloaded' - 当 DOMContentLoaded 事件被触发时，认为操作完成。
            'load' - 当加载事件被触发时，认为操作已经完成。
            'networkidle' - 当至少 500 毫秒没有网络连接时，认为操作完成。
        """
        if type(self._obj).__name__ == "Page":
            return self._obj.go_back(
                timeout=timeout,
                wait_until=wait_until,
            )
        elif type(self._obj).__name__ == "Frame":
            return self._obj.page.go_back(
                timeout=timeout,
                wait_until=wait_until,
            )
        else:
            raise TypeError(f"{self._obj}的类型应当是 Page 类型或 Frame 类型。")

    def go_forward(
            self,
            timeout: float = None,
            wait_until: Literal["domcontentloaded", "load", "networkidle"] = None
    ):
        """导航到历史记录的下一页。
        返回主要资源响应。
        在多次重定向的情况下，导航将使用上次重定向的响应进行解析。
        如果不能返回，则返回 null。

        :param timeout:最大操作时间以毫秒为单位，默认为 30 秒，传递 0 以禁用超时。
            可以使用 browser_context.set_default_navigation_timeout(timeout)、
            browser_context.set_default_timeout(timeout)、
            page.set_default_navigation_timeout(timeout)
            或 page.set_default_timeout(timeout) 方法更改默认值。
        :param wait_until: <"load"|"domcontentloaded"|"networkidle"> 当认为操作成功时，默认加载。 事件可以是：#
            'domcontentloaded' - 当 DOMContentLoaded 事件被触发时，认为操作完成。
            'load' - 当加载事件被触发时，认为操作已经完成。
            'networkidle' - 当至少 500 毫秒没有网络连接时，认为操作完成。
        """
        if type(self._obj).__name__ == "Page":
            return self._obj.go_forward(
                timeout=timeout,
                wait_until=wait_until,
            )
        elif type(self._obj).__name__ == "Frame":
            return self._obj.page.go_forward(
                timeout=timeout,
                wait_until=wait_until,
            )
        else:
            raise TypeError(f"{self._obj}的类型应当是 Page 类型或 Frame 类型。")

    def goto(
            self,
            url: str,
            *,
            timeout: float = None,
            wait_until: Literal["domcontentloaded", "load", "networkidle"] = None,
            referer: str = None
    ):
        """导航到 `url`
        返回主要资源响应。 在多次重定向的情况下，导航将使用上次重定向的响应进行解析。
        如果出现以下情况，该方法将抛出错误：
            存在 SSL 错误（例如，在自签名证书的情况下）。
            目标网址无效。
            导航期间超时。
            远程服务器没有响应或无法访问。
            主资源加载失败。
        当远程服务器返回任何有效的 HTTP 状态代码时，该方法不会抛出错误，包括 404“未找到”和 500“内部服务器错误”。
        可以通过调用 response.status 来检索此类响应的状态代码。
        注意:
        该方法要么抛出错误，要么返回主资源响应。 唯一的例外是导航到 about:blank 或导航到具有不同散列的相同 URL，这将成功并返回 null。

        :param url:页面导航到的 URL。 网址应包括方案，例如 https://。
            当通过上下文选项提供 base_url 并且传递的 URL 是路径时，它会通过新的 URL() 构造函数合并。
        :param timeout: 最大操作时间以毫秒为单位，默认为 30 秒，传递 0 以禁用超时。
            可以使用 browser_context.set_default_navigation_timeout(timeout)、
            browser_context.set_default_timeout(timeout)、
            page.set_default_navigation_timeout(timeout)
            或 page.set_default_timeout(timeout) 方法更改默认值。
        :param wait_until: <"load"|"domcontentloaded"|"networkidle"> 当认为操作成功时，默认加载。 事件可以是：#
            'domcontentloaded' - 当 DOMContentLoaded 事件被触发时，认为操作完成。
            'load' - 当加载事件被触发时，认为操作已经完成。
            'networkidle' - 当至少 500 毫秒没有网络连接时，认为操作完成。
        :param referer: 引用标头值。 如果提供，它将优先于 page.set_extra_http_headers(headers) 设置的引用标头值.
        """
        return self._obj.goto(
            url=url,
            timeout=timeout,
            wait_until=wait_until,
            referer=referer,
        )

    def hover(
            self,
            selector: str,
            timeout: float = None,
            modifiers: Optional[
                List[Literal["Alt", "Control", "Meta", "Shift"]]
            ] = None,
            position: Position = None,
    ):
        """鼠标悬停
        此方法通过执行以下步骤将鼠标悬停在元素上：
        等待对元素的可操作性检查。
        如果需要，将元素滚动到视图中。
        使用 page.mouse 将鼠标悬停在元素的中心或指定位置上。
        等待启动的导航成功或失败

        :param position: 相对于元素填充框的左上角使用的点。 如果未指定，则使用元素的一些可见点。
        :param modifiers: 要按下的修饰键。 确保在操作期间仅按下这些修饰符，然后将当前修饰符恢复回来。 如果未指定，则使用当前按下的修饰符
        :param selector: 用于搜索元素的选择器。 如果有多个元素满足选择器，将使用第一个。
        :param timeout: 最大操作时间以毫秒为单位，默认为 30 秒，传递 0 以禁用超时。
            可以使用 browser_context.set_default_navigation_timeout(timeout)、
            browser_context.set_default_timeout(timeout)、
            page.set_default_navigation_timeout(timeout)
            或 page.set_default_timeout(timeout) 方法更改默认值。
        """
        element = self._find_element_cross_frame(selector=selector)
        element.hover(
            modifiers=modifiers,
            timeout=timeout,
            position=position,
        )

    def inner_html(self, selector: str) -> str:
        """元素的 innerHTML 值。

        :param selector: 用于搜索元素的选择器。 如果有多个元素满足选择器，将使用第一个。
        """
        element = self._find_element_cross_frame(selector)
        return element.inner_html()

    def inner_text(self, selector: str) -> str:
        """元素的 innerText 值。

        :param selector: 用于搜索元素的选择器。 如果有多个元素满足选择器，将使用第一个。
        """
        element = self._find_element_cross_frame(selector)
        return element.inner_text()

    def input_value(self, selector: str, timeout: float = None) -> str:
        """元素的 value 属性的值。

        :param selector: 用于搜索元素的选择器。 如果有多个元素满足选择器，将使用第一个。
        :param timeout: 最大操作时间以毫秒为单位，默认为 30 秒，传递 0 以禁用超时。
            可以使用 browser_context.set_default_navigation_timeout(timeout)、
            browser_context.set_default_timeout(timeout)、
            page.set_default_navigation_timeout(timeout)
            或 page.set_default_timeout(timeout) 方法更改默认值
        """
        element = self._find_element_cross_frame(selector)
        return element.input_value(timeout=timeout)

    def is_checked(self, selector: str) -> bool:
        """返回是否选中元素。如果元素不是复选框或单选输入，则引发异常。"""
        return self._find_element_cross_frame(selector).is_checked()

    def is_disabled(self, selector: str) -> bool:
        """返回元素是否被禁用，与启用相反。"""
        return self._find_element_cross_frame(selector).is_disabled()

    def is_editable(self, selector: str) -> bool:
        """返回元素是否可编辑。"""
        return self._find_element_cross_frame(selector).is_editable()

    def is_enabled(self, selector: str) -> bool:
        """返回元素是否被启用。"""
        return self._find_element_cross_frame(selector).is_enabled()

    def is_hidden(self, selector: str) -> bool:
        """返回元素是否隐藏，与可见相反。 不匹配任何元素的选择器被认为是隐藏的。"""
        return self._find_element_cross_frame(selector).is_hidden()

    def is_visible(self, selector: str) -> bool:
        """返回元素是否可见。 不匹配任何元素的选择器被认为是不可见的。"""
        return self._find_element_cross_frame(selector).is_visible()

    def press(
            self,
            selector: str,
            key: str,
            delay: float = None,
            timeout: float = None,
            no_wait_after: bool = None,
    ) -> None:
        """模拟手动输入。

        聚焦元素，然后使用keyboard.down(key) 和keyboard.up(key)。
        key 可以指定预期的 keyboardEvent.key 值或要为其生成文本的单个字符。 可以在此处找到键值的超集。 键的例子是：
        F1 - F12, Digit0- Digit9, KeyA- KeyZ, 反引号, 减号, 等号, 反斜杠, Backspace, Tab, Delete, Escape, ArrowDown, End,
        Enter, Home, Insert, PageDown, PageUp, ArrowRight, ArrowUp, 等等。

        还支持以下修改快捷键：Shift、Control、Alt、Meta、ShiftLeft。

        按住 Shift 键将键入与大写键对应的文本。

        如果键是单个字符，则它区分大小写，因此值a和A将生成不同的文本。

        也支持快捷键，例如键：“Control+o”或键：“Control+Shift+T”。 当使用修饰符指定时，在按下后续键的同时按下并按住修饰符。

        :param selector: 用于搜索元素的选择器。如果有多个元素满足选择器，将使用第一个。
        :param key: 要按下的键的名称或要生成的字符，例如 ArrowLeft 或 a。
        :param delay: 在 keydown 和 keyup 之间等待的时间（以毫秒为单位）。 默认为 0。
        :param timeout: 以毫秒为单位的最长时间，默认为 30 秒，传递 0 以禁用超时。
            可以使用 browser_context.set_default_timeout(timeout) 或 page.set_default_timeout(timeout) 方法更改默认值
        :param no_wait_after: 启动导航的操作正在等待这些导航发生并等待页面开始加载。 可以通过设置此标志选择退出等待。
            只需要在特殊情况下使用此选项，例如导航到无法访问的页面。 默认为假。
        """
        element = self._find_element_cross_frame(selector)
        element.press(
            key=key,
            delay=delay,
            timeout=timeout,
            no_wait_after=no_wait_after,
        )

    def select_option(
            self,
            selector,
            value: Union[str, List[str]] = None,
            index: Union[int, List[int]] = None,
            label: Union[str, List[str]] = None,
            option_element: Union["ElementHandle", List["ElementHandle"]] = None,
            timeout: float = None,
    ) -> List[str]:
        """此方法等待元素匹配选择器，等待可操作性检查，等待所有指定的选项都出现在 <select> 元素中并选择这些选项。

        如果目标元素不是 <select> 元素，则此方法会引发错误。 但是，如果该元素位于具有关联控件的 <label> 元素内，则将使用该控件。

        返回已成功选择的选项值数组。

        一旦选择了所有提供的选项，就会触发更改和输入事件。
        :param selector:
        :param value: 按值选择的选项。 可选的。
            如果 <select> 具有 multiple 属性，则选择所有给定的选项，否则仅选择与传递的选项之一匹配的第一个选项。
        :param index: 按索引选择的选项。 可选的。
        :param label: 按标签选择的选项。 可选的。
            如果 <select> 具有 multiple 属性，则选择所有给定的选项，否则仅选择与传递的选项之一匹配的第一个选项。
        :param option_element: 按 ElementHandle 实例选择选项。 可选的。
        :param timeout: 以毫秒为单位的最长时间，默认为 30 秒，传递 0 以禁用超时。
            可以使用 browser_context.set_default_timeout(timeout) 或 page.set_default_timeout(timeout) 方法更改默认值。
        """
        element = self._find_element_cross_frame(selector=selector)
        return element.select_option(
            timeout=timeout,
            element=option_element,
            index=index,
            value=value,
            label=label
        )

    def query_selector(self, selector: str):
        """该方法在页面中查找与指定选择器匹配的元素。
        如果没有元素与选择器匹配，则返回值解析为 null。
        要等待页面上的元素，请使用 page.wait_for_selector(selector, **kwargs)。
        """
        return self._find_element_cross_frame(selector)

    def query_selector_all(self, selector: str):
        """该方法查找页面内与指定选择器匹配的所有元素。 如果没有元素与选择器匹配，则返回值解析为 []。"""
        return self._find_element_cross_frame(selector, False)

    def uncheck(self, selector: str):
        """此方法取消选中元素匹配选择器。"""
        element = self._find_element_cross_frame(selector)
        element.uncheck()

    def wait_for_selector(self, selector: str, timeout: float = None,
                          state: Literal["attached", "detached", "hidden", "visible"] = None):
        """返回选择器指定的元素满足状态选项时。 如果等待隐藏或分离，则返回 null。
        等待选择器满足状态选项（从 dom 出现/消失，或变为可见/隐藏）。
        如果在调用方法选择器的那一刻已经满足条件，该方法将立即返回。
        如果选择器不满足超时毫秒的条件，该函数将抛出。
        """
        return wait_for_element(self._obj, selector=selector, timeout=timeout, state=state)
