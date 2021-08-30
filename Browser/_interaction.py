import typing

from ._api_structures import Position
from ._invoke import determine_element

NoneType = type(None)


class Interaction:
    def __init__(self, page):
        self._page = page

    def __getattr__(self, item):
        if self.__dict__.get(item):
            return self.item()
        else:
            return getattr(self._page, item)

    def _find_element_cross_frame(self, selector):
        """跨frame搜索元素。
        :param selector: 元素定位器。
        """
        return determine_element(self._page, selector)

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
            button: typing.Literal["left", "middle", "right"] = None,
            click_count: int = None,
            delay: float = None,
            force: bool = None,
            modifiers: typing.Optional[
                typing.List[typing.Literal["Alt", "Control", "Meta", "Shift"]]
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

    def dblclick(
            self,
            selector: str,
            *,
            modifiers: typing.Optional[
                typing.List[typing.Literal["Alt", "Control", "Meta", "Shift"]]
            ] = None,
            position: Position = None,
            delay: float = None,
            button: typing.Literal["left", "middle", "right"] = None,
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
            event_init: typing.Dict = None,
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

    def fill(
            self,
            selector: str,
            value: str,
            *,
            force: bool = None,
            no_wait_after: bool = None,
            timeout: float = None,
            clear: bool = True,
    ) -> NoneType:
        """清空 `selector` 找到的文本字段，然后使用 `value` 填充它。
        此方法等待元素匹配选择器，等待可操作性检查，聚焦元素，填充它并在填充后触发输入事件。
        如果匹配选择器的元素不是 input 、textarea 或 contenteditable 元素，则此方法会引发错误。

        :param selector: 用于搜索元素的选择器。 如果有多个元素满足选择器，将使用第一个。
        :param value: 为 input 、textarea 或 contenteditable 元素填充的值。
        :param force: 是否绕过可操作性检查。 默认为 false。
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
                force=force,
                no_wait_after=no_wait_after,
                timeout=timeout,
            )
        # 填充
        element.fill(
            value=value,
            force=force,
            no_wait_after=no_wait_after,
            timeout=timeout,
        )
