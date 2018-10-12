# selenium-remoteSync
用于同步观测远程连接的服务器selenium grid


运行环境 python 3.6 需要本地安装相应浏览器 及浏览器版本对应的驱动 以及 selenium



最近由于业务需要，需要在远程服务器端运行浏览器，但由于远程服务器均无gui界面，浏览器均使用无头模式,
使在开发及生产环境部署时可能存在异常场景，所以写了一个实现，用以同步可视化观察远程端的页面情况。



实现较为简单，使用selenium时获取远程服务器端浏览器的页面源码，保存于本地后，在本地开启http服务，并在本地打开一个webdriver访问保存下的页面源码文件。


syncRemote 类与 webdriver.Remote类具有相同的方法，在创建时需要多添加一个参数browser_name，例如：

browser = syncRemote(
command_executor='http://*:4444/wd/hub',
desired_capabilities=DesiredCapabilities.CHROME, 
options=webdriver.ChromeOptions(),
browser_name="Chrome"
)


暂时仅限“Chrome”,"FireFox","Ie","Edge","PhantomJS".


由于selenium无原生建立多窗口的方法，所以暂未对多窗口进行协调同步。


未对webelement类进行封装，基于webelement类的操作将不会同步。


如有不足之处，请各位大佬指正。

