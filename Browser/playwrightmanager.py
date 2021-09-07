import os
import pathlib
import typing

from playwright.sync_api._context_manager import PlaywrightContextManager

from ._api_structures import ProxySettings, HttpCredentials, StorageState, ViewportSize
from ._api_types import Error
from ._interaction import Interaction
from .data_types import SupportedBrowsers


class PlaywrightManager:
    def __init__(
            self,
            timeout: float = 30000,
            navigation_timeout: float = 1200000,
            enable_playwright_debug: bool = False,
            external_browser_executable: typing.Optional[typing.Dict[SupportedBrowsers, str]] = None,
    ):
        """对Playwright方法的封装。

        :param timeout: 将更改所有接受超时选项的方法的默认最长时间。
        :param navigation_timeout: 将更改触发导航的方法和相关快捷方式的默认最长导航时间。
        :param enable_playwright_debug: 启用playwright的调试模式，输出详细日志。
        :param external_browser_executable: 浏览器可执行路径。
        """
        self.external_browser_executable: typing.Dict[SupportedBrowsers, str] = (
                external_browser_executable or {}
        )  # 浏览器可执行程序的路径

        self.enable_playwright_debug = enable_playwright_debug  # 启用playwright调试模式

        self.default_timeout = timeout  # 此设置将更改所有接受超时选项的方法的默认最长时间。
        self.default_navigation_timeout = navigation_timeout
        # 此设置将更改以下方法和相关快捷方式的默认最长导航时间：
        # go_back(), go_forward(), goto(), reload(), set_content(), expect_navigation()

        self._playwright_process = None  # playwright进程
        self._browser = None  # 当前使用的浏览器实例
        self._context = None  # 激活的context实例
        self._page = None  # 激活的page实例
        self._frame = None  # 激活的frame实例
        self._interaction = None  # 实际与浏览器交互的对象

    @property
    def interaction(self):
        return Interaction(self._interaction)

    def start_playwright(self):
        """启动Playwright进程。"""
        if self.enable_playwright_debug:
            os.environ["DEBUG"] = "pw:api"
        os.environ["PLAYWRIGHT_BROWSERS_PATH"] = "0"
        self._playwright_process = PlaywrightContextManager().start()

    def connect_over_cdp(
            self,
            endpoint_url: str,
            *,
            headers: typing.Dict[str, str] = None,
            slow_mo: float = None,
            timeout: float = None
    ):
        """此方法使用 Chrome DevTools 协议将 Playwright 附加到现有浏览器实例。
        注意，只有基于 Chromium 的浏览器才支持通过 Chrome DevTools 协议进行连接。

        :param endpoint_url: 要连接到的 CDP websocket 端点或 http url。
            例如 http://localhost:9222/ 或 ws://127.0.0.1:9222/devtools/browser/387adf4c-243f-4051-a181-46798f4a46f4。
        :param headers: 与连接请求一起发送的附加 HTTP 标头。 可选的。
        :param slow_mo: 将 Playwright 操作减慢指定的毫秒数。很有用，以便看到正在发生的事情。 默认为 0。
        :param timeout: 等待建立连接的最长时间（以毫秒为单位）。默认为 30000（30 秒）。 传递 0 以禁用超时。
        """
        browser_type = self._playwright_process.chromium
        self._browser = browser_type.connect_over_cdp(
            endpoint_url=endpoint_url,
            headers=headers,
            slow_mo=slow_mo,
            timeout=timeout
        )
        self._context = self._browser.contexts[0]
        self._page = self._context.pages[0]

    def new_browser(
            self,
            *,
            browser: SupportedBrowsers = SupportedBrowsers.chromium,
            args: typing.List[str] = None,
            downloads_path: typing.Union[str, pathlib.Path] = None,
            env: typing.Optional[typing.Dict[str, typing.Union[str, float, bool]]] = None,
            executable_path: typing.Union[str, pathlib.Path] = None,
            headless: bool = None,
            proxy: ProxySettings = None,
            slow_mo: float = None,
            timeout: float = None,
    ):
        """创建具有指定选项的浏览器实例。

        :param browser: 打开指定的浏览器。 默认为 chromium。
        :param args: 传递给浏览器实例的附加参数。
        :param downloads_path: 如果指定，接受的下载将下载到此目录中。否则，将创建临时文件夹，并在浏览器关闭时删除。
        无论如何，当创建它们的浏览器上下文关闭时，下载将被删除。
        :param env: 指定浏览器可见的环境变量。默认为 process.env。
        :param executable_path: 要运行的浏览器可执行文件的路径。如果executable_path 是一个相对路径，那么它是相对于当前工作目录解析的。
        :param headless: 是否在无头模式下运行浏览器。默认为true。
        :param proxy: 网络代理设置。
            `server` 用于所有请求的代理。支持 HTTP 和 SOCKS 代理，例如 http://myproxy.com:3128 或 socks5://myproxy.com:3128。
            缩写 myproxy.com:3128 被视为 HTTP 代理。
            `bypass` 可选的逗号分隔域以绕过代理，例如“.com、chromium.org、.domain.com”。
            `username` 如果 HTTP 代理需要身份验证，则使用的可选用户名。
            `password` 如果 HTTP 代理需要身份验证，则使用的可选密码。
        :param slow_mo: 将 Playwright 操作减慢指定的毫秒数。很有用，可以看到正在发生的事情。
        :param timeout: 等待浏览器实例启动的最长时间（以毫秒为单位）。 默认为 30000（30 秒）。 传递 0 以禁用超时。
        """
        if self._browser is not None:
            print("已有打开的浏览器，请勿重复打开。")
            return
        browser_path = self.external_browser_executable.get(browser)
        if browser_path:
            executable_path = browser_path
        browser_type = getattr(self._playwright_process, browser.name)
        self._browser = browser_type.launch(
            args=args,
            downloads_path=downloads_path,
            env=env,
            executable_path=executable_path,
            headless=headless,
            proxy=proxy,
            slow_mo=slow_mo,
            timeout=timeout
        )

    def close_browser(self):
        """如果此浏览器是使用 `new_browser` 获得的，则关闭浏览器及其所有页面（如果有的话）。
        如果连接到此浏览器，则清除所有创建的属于此浏览器的上下文并断开与浏览器服务器的连接。
        Browser 对象本身被认为已被释放，不能再使用。
        """
        self._browser.close()
        # 重置所有活动对象
        self._browser = None
        self._context = None
        self._page = None
        self._interaction = None

    def new_context(
            self,
            accept_downloads: bool = None,
            base_url: str = None,
            bypass_csp: bool = None,
            extra_http_headers: typing.Optional[typing.Dict[str, str]] = None,
            http_credentials: HttpCredentials = None,
            ignore_https_errors: bool = None,
            java_script_enabled: bool = None,
            no_viewport: bool = None,
            proxy: ProxySettings = None,
            storage_state: typing.Union[StorageState, str, pathlib.Path] = None,
            strict_selectors: bool = None,
            user_agent: str = None,
            viewport: ViewportSize = None,
    ):
        """创建一个新的浏览器上下文。 它不会与其他浏览器上下文共享 cookie/缓存。

        :param accept_downloads: 是否自动下载所有附件。 默认为 false ，其中所有下载都被取消。
        :param base_url: 当使用 goto(url, **kwargs), route(url, handler), wait_for_url(url, **kwargs),
            expect_request(url_or_predicate, **kwargs), 或 expect_response(url_or_predicate) , **kwargs) 时，
            它通过使用 URL() 构造函数来构建相应的 URL 。例子：
            baseURL: http://localhost:3000 并导航到 /bar.html => http://localhost:3000/bar.html
            baseURL: http://localhost:3000/foo/ 并导航到 ./bar.html => http://localhost:3000/foo/bar.html
        :param bypass_csp: 切换绕过页面的内容安全策略。
        :param extra_http_headers: 包含每个请求都要发送的附加HTTP头的对象。所有标题值必须是字符串。
        :param http_credentials: HTTP 身份验证的凭据。
        :param ignore_https_errors: 是否在导航过程中忽略 HTTPS 错误。 默认为 false。
        :param java_script_enabled: 是否在上下文中启用 JavaScript。 默认为 true。
        :param no_viewport: 不强制固定视口，允许在有头模式下调整窗口大小。
        :param proxy: 与此上下文一起使用的网络代理设置。
        :param storage_state: 使用给定的存储状态填充上下文。
            此选项可用于使用通过 storage_state(**kwargs) 获取的登录信息初始化上下文。
            具有保存存储的文件的路径，或具有以下字段的对象:
            cookies <List[Dict]> 为上下文设置的可选 cookie
                name <str>
                value <str>
                url <str> url、domain和path三选一。
                domain <str> url、domain和path三选一。
                path <str> url、domain和path三选一。
                expires <float> 可选的 Unix 时间（以秒为单位）。
                httpOnly <bool> 可选的 httpOnly 标志
                secure <bool> 可选的secure标志
                sameSite <"Strict"|"Lax"|"None"> 可选的 sameSite 标志
            origins <List[Dict]> 为上下文设置的可选 localStorage
                origin <str>
                localStorage <List[Dict]>
                name <str>
                value <str>
        :param strict_selectors: 它指定，为此上下文启用严格选择器模式。
            在严格选择器模式模式下，当多个元素与选择器匹配时，将抛出对选择器的所有操作，这些操作意味着单个目标DOM元素。
        :param user_agent: 在此上下文中使用的特定用户代理。
        :param viewport: 为每个页面设置一致的视窗。默认为 1280x720 视窗。
            width <int> 以像素为单位的页面宽度。
            height <int> 以像素为单位的页面高度。
        """
        self._context = self._browser.new_context(
            accept_downloads=accept_downloads,
            base_url=base_url,
            bypass_csp=bypass_csp,
            extra_http_headers=extra_http_headers,
            http_credentials=http_credentials,
            ignore_https_errors=ignore_https_errors,
            java_script_enabled=java_script_enabled,
            no_viewport=no_viewport,
            proxy=proxy,
            storage_state=storage_state,
            strict_selectors=strict_selectors,
            user_agent=user_agent,
            viewport=viewport
        )
        self._context.set_default_navigation_timeout(self.default_navigation_timeout)
        self._context.set_default_timeout(self.default_timeout)

    def close_context(self):
        """关闭浏览器上下文。
        属于浏览器上下文的所有页面都将关闭。
        无法关闭默认浏览器上下文。
        """
        if self._context is not None:
            self._context.close()
            if self._browser.contexts:
                self._context = self._browser.contexts[-1]
                self._page = None
                self._interaction = None

    def new_page(
            self,
            accept_downloads: bool = None,
            base_url: str = None,
            bypass_csp: bool = None,
            extra_http_headers: typing.Optional[typing.Dict[str, str]] = None,
            http_credentials: HttpCredentials = None,
            ignore_https_errors: bool = None,
            java_script_enabled: bool = None,
            no_viewport: bool = None,
            proxy: ProxySettings = None,
            storage_state: typing.Union[StorageState, str, pathlib.Path] = None,
            strict_selectors: bool = None,
            user_agent: str = None,
            viewport: ViewportSize = None
    ):
        """在新的浏览器上下文中创建一个新页面。 关闭此页面也将关闭上下文。这是一个方便的API，应该只用于单页场景和短片段。
        生产代码应显式创建浏览器上下文，然后创建页面，以控制其确切的生命周期。

        :param accept_downloads: 是否自动下载所有附件。 默认为 false ，其中所有下载都被取消。
        :param base_url: 当使用 goto(url, **kwargs), route(url, handler), wait_for_url(url, **kwargs),
            expect_request(url_or_predicate, **kwargs), 或 expect_response(url_or_predicate) , **kwargs) 时，
            它通过使用 URL() 构造函数来构建相应的 URL 。例子：
            baseURL: http://localhost:3000 并导航到 /bar.html => http://localhost:3000/bar.html
            baseURL: http://localhost:3000/foo/ 并导航到 ./bar.html => http://localhost:3000/foo/bar.html
        :param bypass_csp: 切换绕过页面的内容安全策略。
        :param extra_http_headers: 包含每个请求都要发送的附加HTTP头的对象。所有标题值必须是字符串。
        :param http_credentials: HTTP 身份验证的凭据。
        :param ignore_https_errors: 是否在导航过程中忽略 HTTPS 错误。 默认为 false。
        :param java_script_enabled: 是否在上下文中启用 JavaScript。 默认为 true。
        :param no_viewport: 不强制固定视口，允许在有头模式下调整窗口大小。
        :param proxy: 与此上下文一起使用的网络代理设置。
        :param storage_state: 使用给定的存储状态填充上下文。
            此选项可用于使用通过 storage_state(**kwargs) 获取的登录信息初始化上下文。
            具有保存存储的文件的路径，或具有以下字段的对象:
            cookies <List[Dict]> 为上下文设置的可选 cookie
                name <str>
                value <str>
                url <str> url、domain和path三选一。
                domain <str> url、domain和path三选一。
                path <str> url、domain和path三选一。
                expires <float> 可选的 Unix 时间（以秒为单位）。
                httpOnly <bool> 可选的 httpOnly 标志
                secure <bool> 可选的secure标志
                sameSite <"Strict"|"Lax"|"None"> 可选的 sameSite 标志
            origins <List[Dict]> 为上下文设置的可选 localStorage
                origin <str>
                localStorage <List[Dict]>
                name <str>
                value <str>
        :param strict_selectors: 它指定，为此上下文启用严格选择器模式。
            在严格选择器模式模式下，当多个元素与选择器匹配时，将抛出对选择器的所有操作，这些操作意味着单个目标DOM元素。
        :param user_agent: 在此上下文中使用的特定用户代理。
        :param viewport: 为每个页面设置一致的视窗。默认为 1280x720 视窗。
            width <int> 以像素为单位的页面宽度。
            height <int> 以像素为单位的页面高度。
        """
        if self._context is not None:
            self._page = self._context.new_page()
        else:
            self._page = self._browser.new_page(
                accept_downloads=accept_downloads,
                base_url=base_url,
                bypass_csp=bypass_csp,
                extra_http_headers=extra_http_headers,
                http_credentials=http_credentials,
                ignore_https_errors=ignore_https_errors,
                java_script_enabled=java_script_enabled,
                no_viewport=no_viewport,
                proxy=proxy,
                storage_state=storage_state,
                strict_selectors=strict_selectors,
                user_agent=user_agent,
                viewport=viewport
            )
            self._page.context.set_default_timeout(self.default_timeout)
            self._page.context.set_default_navigation_timeout(self.default_navigation_timeout)
        self._interaction = self._page

    def close_page(self):
        """关闭当前的页面。如果还有其他打开的页面，将切换到最近打开的页面。"""
        if self._page is not None:
            self._page.close()
            if self._context.pages:  # 如果还有打开的页面
                self._page = self._context.pages[-1]
                self._interaction = self._page
            else:
                self._interaction = None

    def switch_context(self, index: int):
        """按 `index` 将活动浏览器上下文切换到另一个打开的上下文。

        :param index: 要更改为的上下文的索引。从0开始。
        """
        self._context = self._browser.contexts[index]

    def switch_page(self, index: int):
        """按 `index` 将活动浏览器页面切换到另一个打开的页面。

        :param index: 要更改为的页面的索引。从0开始。
        """
        self._page.expect_popup()
        self._page = self._context.pages[index]
        self._interaction = self._page

    def switch_new_page(self):
        """活动浏览器页面切换到最新打开的页面。"""
        self._page = self._page.expect_popup().value
        self._interaction = self._page

    def switch_opener_page(self):
        """切换到当前弹出窗口的开启窗口。
        如果当前页面非弹出窗口，则抛出异常。
        如果开启窗口已经关闭，则抛出异常。
        """
        self._page = self._page.opener()
        if self._page is None:
            no_opener = Error('开启页面已关闭或当前页面没有开启页面。')
            raise no_opener
        else:
            self._interaction = self._page

    def switch_frame_by_index(self, index: int):
        """根据索引选择frame。"""
        self._frame = self._page.frames[index]
        if self._frame.parent_frame is None:
            self._interaction = self._frame.page
        else:
            self._interaction = self._frame

    def switch_frame(self, url: str = None, name: str = None):
        """返回匹配指定条件的帧。 必须指定名称或网址。

        :param url: glob 模式、正则表达式模式或谓词接收框架的 url 作为 URL 对象。 可选的。
        :param name: 在 iframe 的 name 属性中指定的框架名称。 可选的。
        """
        self._frame = self._page.frame(url=url, name=name)
        if self._frame is None:
            no_such_frame = Error(f"没有url={url}，name={name}的Frame。")
            raise no_such_frame
        if self._frame.parent_frame is None:
            self._interaction = self._frame.page
        else:
            self._interaction = self._frame
