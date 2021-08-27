from Browser.playwrightmanager import PlaywrightManager
from Browser.data_types import SupportedBrowsers

pm = PlaywrightManager(
    external_browser_executable={
        SupportedBrowsers.chromium: r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
    }
)
pm.start_playwright()
pm.new_browser(headless=False)
pm.new_page()
pm.interaction.goto('file:///C:/Users/Nanakawa/Desktop/test.html')
pm.interaction.fill('name=myframe >>> url="https://www.kancloud.cn/" >>> [name="account"]', value='test')
pm.close_browser()
