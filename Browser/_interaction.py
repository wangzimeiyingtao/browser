import typing

from ._api_structures import Position
from ._api_types import Error
from ._invoke import determine_element

NoneType = type(None)


class Interaction:
    def __init__(self, obj):
        self._obj = obj

    def __getattr__(self, item):
        if self.__dict__.get(item):
            return self.item()
        else:
            return getattr(self._obj, item)

    def _find_element_cross_frame(self, selector, timeout: float = None):
        """跨frame搜索元素。
        :param selector: 元素定位器。
        """
        return determine_element(self._obj, selector, timeout)

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
            unsupported_selector_engine = Error("该方法不支持跨Frame搜索")
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

    def focus(self, selector: str):
        """此方法使用选择器 `selector` 获取元素并聚焦它。
        如果没有与选择器匹配的元素，该方法将等待匹配元素出现在 DOM 中。

        :param selector: 用于搜索元素的选择器。 如果有多个元素满足选择器，将使用第一个。
        """
        element = self._find_element_cross_frame(selector)
        element.focus()

    def get_attribute(self, selector: str, name: str, timeout: float = None) -> typing.Union[NoneType, str]:
        """返回元素属性值。

        :param selector: 用于搜索元素的选择器。 如果有多个元素满足选择器，将使用第一个。
        :param name: 要获取其值的属性名称。
        :param timeout: 以毫秒为单位的最长时间，默认为 30 秒，传递 0 以禁用超时。
            可以使用 browser_context.set_default_timeout(timeout) 或 page.set_default_timeout(timeout) 方法更改默认值
        """
        element = self._find_element_cross_frame(selector, timeout=timeout)
        return element.get_attribute(name)

    def go_back(
            self,
            timeout: float = None,
            wait_until: typing.Literal["domcontentloaded", "load", "networkidle"] = None
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
            wait_until: typing.Literal["domcontentloaded", "load", "networkidle"] = None
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
            wait_until: typing.Literal["domcontentloaded", "load", "networkidle"] = None,
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
            modifiers: typing.Optional[
                typing.List[typing.Literal["Alt", "Control", "Meta", "Shift"]]
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
