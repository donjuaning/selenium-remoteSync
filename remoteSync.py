from selenium import webdriver
from contextlib import contextmanager
import socket
import os
import threading


class syncRemote():

    def __init__(self, command_executor='http://127.0.0.1:4444/wd/hub',
                 desired_capabilities=None, browser_profile=None, proxy=None,
                 keep_alive=False, file_detector=None, options=None, browser_name=None):
        self.create_driver(browser_name, options)
        self.browser = webdriver.Remote(command_executor=command_executor, desired_capabilities=desired_capabilities,
                                        browser_profile=browser_profile, proxy=proxy, keep_alive=keep_alive,
                                        file_detector=file_detector, options=options)
        self.socket_thread()

    def create_driver(self, browser_name, options):
        if browser_name == 'Chrome':
            driver_options = webdriver.ChromeOptions()
            for option in options.arguments:
                if option == '--headless' or option == '--disable-gpu' or option == '--no-sandbox':
                    pass
                else:
                    driver_options.add_argument(option)
            for item in options.experimental_options:
                driver_options.add_experimental_option(item, options.experimental_options[item])
            self.driver = webdriver.Chrome(options=driver_options)

        elif browser_name == 'FireFox':
            driver_options = webdriver.FirefoxOptions()
            for option in options.arguments:
                if option == '--headless' or option == '--disable-gpu' or option == '--no-sandbox':
                    pass
                else:
                    driver_options.add_argument(option)
            self.driver = webdriver.Firefox(options=driver_options)

        elif browser_name == 'Ie':
            driver_options = webdriver.IeOptions()
            for option in options.arguments:
                if option == '--headless' or option == '--disable-gpu' or option == '--no-sandbox':
                    pass
                else:
                    driver_options.add_argument(option)
            for item in options.additional_options:
                driver_options.add_additional_option(item, options.additional_options[item])
            self.driver = webdriver.Ie(options=options)

        elif browser_name == 'Edge':
            self.driver = webdriver.Edge()

    def sync(self):
        html_content = self.browser.page_source
        f = open('index.html', 'w')
        f.write(html_content)
        f.close()
        self.driver.get('http://localhost:10086/index.html')
        self.driver.delete_all_cookies()
        cookies = self.browser.get_cookies()
        for cookie in cookies:
            self.driver.add_cookie(cookie)


    def socket_thread(self):

        f = open('index.html', 'w')
        f.write('')
        f.close()

        t = threading.Thread(target=self.start_socket)
        t.start()

    def start_socket(self):
        self.sk = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        host = '127.0.0.1'
        port = 10086

        self.sk.bind((host, port))
        self.sk.listen(5)

        while True:
            if self.sk.fileno() < 0:
                break
            try:
                clientSk, addr = self.sk.accept()
                print("address is: %s" % str(addr))
                content = ''
                try:
                    f = open('index.html', 'r')
                    while True:
                        chunk = f.read()
                        if not chunk:
                            f.close()
                            break
                        content += chunk
                except:
                    pass

                # 省略了大部分头部信息
                headers = 'HTTP/1.1 200 OK\r\n'
                contentType = 'Content-Type: text/html; charset=utf-8\r\n'
                contentLen = 'Content-Length: ' + str(len(content)) + '\r\n'

                # 组合成响应报文 res
                res = headers + contentType + contentLen + '\r\n' + content

                # 编码后发送给浏览器，
                # 至此，本次通信结束
                clientSk.sendall(res.encode(encoding='UTF-8'))
                clientSk.close()

            except Exception as err:
                try:
                    clientSk.close()
                except:
                    pass

    @contextmanager
    def file_detector_context(self, file_detector_class, *args, **kwargs):
        self.browser.file_detector_context(file_detector_class, args, kwargs)

    @property
    def mobile(self):
        return self.browser.mobile

    @property
    def name(self):
        return self.browser.name

    def start_client(self):

        pass

    def stop_client(self):

        pass

    def start_session(self, capabilities, browser_profile=None):
        self.browser.start_session(capabilities, browser_profile)

    def create_web_element(self, element_id):
        return_results = self.browser.create_web_element(element_id)
        self.sync()
        return return_results

    def execute(self, driver_command, params=None):
        return_results = self.browser.execute(driver_command, params)
        self.sync()
        return return_results

    def get(self, url):

        self.browser.get(url)
        self.sync()

    @property
    def title(self):
        return self.browser.title

    def find_element_by_id(self, id):
        return self.browser.find_element_by_id(id)

    def find_elements_by_id(self, id):
        return self.browser.find_elements_by_id(id)

    def find_element_by_xpath(self, xpath):
        return self.browser.find_element_by_xpath(xpath)

    def find_elements_by_xpath(self, xpath):
        return self.browser.find_elements_by_xpath(xpath)

    def find_element_by_link_text(self, link_text):
        return self.browser.find_element_by_link_text(link_text)

    def find_elements_by_link_text(self, text):
        return self.browser.find_elements_by_id(text)

    def find_element_by_partial_link_text(self, link_text):
        return self.browser.find_element_by_partial_link_text(link_text)

    def find_elements_by_partial_link_text(self, link_text):
        return self.browser.find_elements_by_partial_link_text(link_text)

    def find_element_by_name(self, name):
        return self.browser.find_element_by_name(name)

    def find_elements_by_name(self, name):
        return self.browser.find_elements_by_name(name)

    def find_element_by_tag_name(self, name):
        return self.browser.find_element_by_tag_name(name)

    def find_elements_by_tag_name(self, name):
        return self.browser.find_elements_by_tag_name(name)

    def find_element_by_class_name(self, name):
        return self.browser.find_element_by_class_name(name)

    def find_elements_by_class_name(self, name):
        return self.browser.find_elements_by_class_name(name)

    def find_element_by_css_selector(self, css_selector):
        return self.browser.find_element_by_css_selector(css_selector)

    def find_elements_by_css_selector(self, css_selector):
        return self.browser.find_elements_by_css_selector(css_selector)

    def execute_async_script(self, script, *args):
        return_results = self.browser.execute_async_script(script, args)
        self.sync()
        return return_results

    def execute_script(self, script, *args):
        return_results = self.browser.execute_script(script, args)
        self.sync()
        return return_results

    @property
    def current_url(self):
        return self.browser.current_url

    @property
    def page_source(self):
        return self.browser.page_source

    def close(self):
        self.browser.close()
        self.driver.close()

    def quit(self):
        self.browser.quit()
        self.driver.quit()
        self.sk.close()
        os.remove('index.html')

    @property
    def current_window_handle(self):
        return self.browser.current_window_handle

    @property
    def window_handles(self):
        return self.browser.window_handles

    def maximize_window(self):
        self.browser.maximize_window()

    def fullscreen_window(self):
        self.browser.fullscreen_window()

    def minimize_window(self):
        self.browser.minimize_window()

    @property
    def switch_to(self):
        return self.browser.switch_to

    # Target Locators
    def switch_to_active_element(self):
        return self.browser.switch_to_active_element()

    def switch_to_window(self, window_name):
        self.browser.switch_to_window(window_name)

    def switch_to_frame(self, frame_reference):
        self.browser.switch_to_frame(frame_reference)

    def switch_to_default_content(self):
        self.browser.switch_to_default_content()

    def switch_to_alert(self):
        return self.browser.switch_to_alert()

    def back(self):
        self.browser.back()
        self.sync()

    def forward(self):
        self.browser.forward()
        self.sync()

    def refresh(self):
        self.browser.refresh()
        self.sync()

    def get_cookies(self):
        return self.browser.get_cookies()

    def get_cookie(self, name):
        return self.browser.get_cookie(name)

    def delete_cookie(self, name):
        self.browser.delete_cookie(name)
        self.sync()

    def delete_all_cookies(self):
        self.browser.delete_all_cookies()
        self.sync()

    def add_cookie(self, cookie_dict):
        self.browser.add_cookie(cookie_dict)
        self.sync()

    # Timeouts
    def implicitly_wait(self, time_to_wait):
        self.browser.implicitly_wait(time_to_wait)

    def set_script_timeout(self, time_to_wait):
        self.browser.set_script_timeout(time_to_wait)

    def set_page_load_timeout(self, time_to_wait):
        self.browser.set_page_load_timeout(time_to_wait)

    def find_element(self, by, value=None):
        return self.browser.find_element(by, value)

    def find_elements(self, by, value=None):
        return self.browser.find_elements(by, value)

    @property
    def desired_capabilities(self):
        return self.browser.desired_capabilities

    def get_screenshot_as_file(self, filename):
        return self.browser.get_screenshot_as_file(filename)

    def save_screenshot(self, filename):
        return self.browser.save_screenshot(filename)

    def get_screenshot_as_png(self):
        return self.browser.get_screenshot_as_png()

    def get_screenshot_as_base64(self):
        return self.browser.get_screenshot_as_base64()

    def set_window_size(self, width, height, windowHandle='current'):
        self.browser.set_window_size(width, height, windowHandle)
        self.driver.set_window_size(width, height, windowHandle)

    def get_window_size(self, windowHandle='current'):
        return self.browser.get_window_size(windowHandle)

    def set_window_position(self, x, y, windowHandle='current'):
        self.browser.set_window_position(x, y, windowHandle)
        self.driver.set_window_position(x, y, windowHandle)

    def get_window_position(self, windowHandle='current'):
        return self.browser.get_window_position(windowHandle)

    def get_window_rect(self):
        return self.browser.get_window_rect()

    def set_window_rect(self, x=None, y=None, width=None, height=None):
        self.driver.set_window_rect(x, y, width, height)
        return self.browser.set_window_rect(x, y, width, height)

    @property
    def file_detector(self):
        return self.browser.file_detector

    @file_detector.setter
    def file_detector(self, detector):
        self.browser.file_detector = detector

    @property
    def orientation(self):
        return self.browser.orientation()

    @orientation.setter
    def orientation(self, value):
        self.browser.orientation = value

    @property
    def application_cache(self):
        return self.browser.application_cache

    @property
    def log_types(self):
        return self.browser.log_types

    def get_log(self, log_type):
        return self.browser.get_log(log_type)
