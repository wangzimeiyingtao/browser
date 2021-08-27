import typing

from ._api_structures import Position
from ._invoke import determine_element


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
    ) -> None:
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
    ) -> None:
        """此方法单击匹配选择器的元素。
        :param selector: 用于搜索元素的选择器。 如果有多个元素满足选择器，将使用第一个。
        :param button: 鼠标的左、中（滚轮）、右按键。默认为左。
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

    def fill(
            self,
            selector: str,
            value: str,
            *,
            force: bool = None,
            no_wait_after: bool = None,
            timeout: float = None,
            clear: bool = True,
    ) -> None:
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
