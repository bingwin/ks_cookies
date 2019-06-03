from selenium import webdriver
import redis

r =redis.Redis(host="127.0.0.1", port=6379)

proxy = r.rpoplpush('https_proxy', 'https_proxy').decode()

options = webdriver.ChromeOptions()
# options.binary_location = r"D:\software_location\cent_install\CentBrowser\Application\chrome.exe"
options.binary_location = '/usr/bin/google-chrome-stable'

# Linux 环境下配置
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-extensions')
options.add_argument('--disable-gpu')

options.add_argument("--proxy-server=http://%s" % (proxy))

driver = webdriver.Chrome(executable_path='/home/seeta/zhangyanchao/chromedriver_install/chromedriver',
						  chrome_options=options)
# driver = webdriver.Chrome(executable_path='D:\projects\Weibo_projects\kuaishou\chromedriver.exe',
#                           chrome_options=options)

# # 设置代理
# # options.add_argument("--proxy-server=http://%s" % (pro))
# options.add_argument("--proxy-server=http://%s" % ('119.129.236.251:4206'))

# # 使用 PhantomJS 初始化
# service_args = ['--proxy=119.129.236.251:4206', '--proxy-type=socks5', ]
# driver = webdriver.PhantomJS(r'C:\Users\Administrator\Desktop\phantomjs-2.1.1-windows\phantomjs-2.1.1-windows\bin\phantomjs.exe', service_args=service_args)

# # 一定要注意，=两边不能有空格，不能是这样--proxy-server = http://202.20.16.82:10152
# driver = webdriver.Chrome(chrome_options=options)
# driver.maximize_window()

# # 查看本机ip，查看代理是否起作用
# driver.get("http://httpbin.org/ip")
# print(driver.page_source)

driver.get('https://live.kuaishou.com/')
cookies = driver.get_cookies()
print(driver.page_source)
