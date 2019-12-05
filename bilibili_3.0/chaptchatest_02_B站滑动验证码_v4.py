"""
__title__ = ''
__author__ = 'Thompson'
__mtime__ = '2018/7/29'
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""

import random
import time

from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from PIL import Image

class Crack():
    def __init__(self, username, passwd):
        self.url = 'https://passport.bilibili.com/login'
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 100)
        self.BORDER = 5
        self.passwd = passwd
        self.username = username

    def open(self):
        """
        打开浏览器,并输入查询内容
        """
        self.browser.get(self.url)
        # 用户名的输入框
        keyword = self.wait.until(EC.presence_of_element_located((By.ID, 'login-username')))
        keyword.send_keys(self.username) # 输入用户名
        # 密码的输入框
        keyword = self.wait.until(EC.presence_of_element_located((By.ID, 'login-passwd')))
        keyword.send_keys(self.passwd)
        # 登陆按钮，点击，让验证码出现
        btn = self.browser.find_element_by_xpath('//a[@class="btn btn-login"]')
        btn.click()

    def get_images(self, bg_filename='./images/bzyzm.png', fullbg_filename='./images/bzyzmfull.png'):
        """
        获取验证码图片
        @bg_filename：带阴影的背景图保存的路径
        @fullbg_filename：不带阴影的图片保存的路径
        :return: 图片的location信息
        """
        time.sleep(2)
        myjs = 'document.getElementsByClassName("geetest_canvas_slice")[0].style.display="none";'
        self.browser.execute_script(myjs)
        web_filename = './images/web.jpg'
        self.browser.save_screenshot(web_filename)
        myjs = 'document.getElementsByClassName("geetest_canvas_slice")[0].style.display="block";'
        self.browser.execute_script(myjs)

        element = self.browser.find_element_by_xpath('//canvas[@class="geetest_canvas_bg geetest_absolute"]')
        location = element.location
        size = element.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size['width']
        print('验证码位置', top, bottom, left, right)
        screenshot = Image.open(web_filename)
        # 截取带阴影的验证码图片
        captcha = screenshot.crop((left, top, right, bottom))
        captcha.save(bg_filename)


        myjs = 'document.getElementsByClassName("geetest_canvas_fullbg")[0].style.display="block";' #
        self.browser.execute_script(myjs)
        self.browser.save_screenshot(web_filename)
        element = self.browser.find_element_by_class_name('geetest_canvas_fullbg')
        print('element:',element)
        location = element.location
        size = element.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size[
            'width']
        print('验证码位置', top, bottom, left, right)
        screenshot = Image.open(web_filename)
        # 截取不带阴影的验证码图片
        captcha = screenshot.crop((left, top, right, bottom))
        captcha.save(fullbg_filename)
        myjs = 'document.getElementsByClassName("geetest_canvas_fullbg")[0].style.display="none";'
        self.browser.execute_script(myjs)

    def is_pixel_equal(self, img1, img2, x, y):
        """
        判断两个像素是否相同
        :param image1: 图片1
        :param image2: 图片2
        :param x: 位置x
        :param y: 位置y
        :return: 像素是否相同
        """
        # 取两个图片的指定位置的像素点
        # load()加载Image对象的像素
        pix1 = img1.load()[x, y]
        pix2 = img2.load()[x, y]
        threshold = 60
        if (abs(pix1[0] - pix2[0]) < threshold and abs(pix1[1] - pix2[1]) < threshold and abs(
                        pix1[2] - pix2[2]) < threshold):
            return True
        else:
            return False


    def get_gap(self, img1, img2):
        """
        获取缺口偏移量
        :param img1: 不带缺口图片
        :param img2: 带缺口图片
        :return:
        """
        left = 10
        # size是Image对象的属性，表示图片尺寸（宽，高）
        for i in range(left, img1.size[0]): #  宽，水平方向
            for j in range(img1.size[1]): # 高，垂直方向
                if not self.is_pixel_equal(img1, img2, i, j):
                    left = i
                    return left
        return left


    def get_track(self, distance):
        """
        根据偏移量获取移动轨迹
        :param distance: 偏移量
        :return: 移动轨迹
        """
        # 移动轨迹
        track = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = distance * 0.7
        # 计算间隔
        t = 0.1
        # 初速度
        v = 0

        while current < distance:
            if current < mid:
                # 加速度为正2
                a = 40
            else:
                # 加速度为负3
                a = -24
            # 初速度v0
            v0 = v
            # 当前速度v = v0 + at
            v = v0 + a * t
            # 移动距离x = v0t + 1/2 * a * t^2
            move = v0 * t + 1 / 2 * a * t * t
            # 当前位移
            current += move
            # 加入轨迹
            track.append(round(move))
            #print('forword', current, distance)

        v = 0

        print(current,distance)
        move = distance - current
        # 加入轨迹
        track.append(round(move))


        return track

    def get_slider(self):
        """
        获取滑块
        :return: 滑块对象
        """
        while True:
            try:
                slider = self.browser.find_element_by_xpath('//div[@class="geetest_slider_button"]')
                break
            except:
                time.sleep(0.5)
        return slider

    def move_to_gap(self, slider, track):
        """
        拖动滑块到缺口处
        :param slider: 滑块
        :param track: 轨迹
        :return:
        """
        ActionChains(self.browser).click_and_hold(slider).perform()
        while track:
            #x = random.choice(track)
            x=track.pop(0)
            ActionChains(self.browser).move_by_offset(xoffset=x, yoffset=0).perform()
            #track.remove(x)
            #time.sleep(0.0001)
        time.sleep(2)
        print('release')
        ActionChains(self.browser).release(slider).perform()
        time.sleep(2)
        #self.browser.quit()

    def crack(self):
        # 打开浏览器
        self.open()

        # 保存的图片名字
        bg_filename = './images/bzyzm.png'
        fullbg_filename = './images/bzyzmfull.png'
        # 获取图片
        self.get_images(bg_filename,fullbg_filename)
        # 加载验证码带阴影背景图和全背景图
        bg_img = Image.open(bg_filename)
        fullbg_img = Image.open(fullbg_filename)
        #获取缺口位置
        gap = self.get_gap(fullbg_img, bg_img)
        print('缺口位置', gap)
        # 生成移动的轨迹
        track = self.get_track(gap - self.BORDER)
        print('滑动滑块')
        #print(track)

        # 点按呼出缺口
        slider = self.get_slider()
        # 拖动滑块到缺口处
        self.move_to_gap(slider, track)
        #
        time.sleep(1)
        try:
            mspan = self.browser.find_elements_by_class_name('gt_info_content')
            if len(mspan) > 0:
                info = mspan.text
                print('info:',info)
                if '怪物吃了拼图' in info:
                    print(mspan.text)
                    time.sleep(2)
                    self.crack()

            mspan = self.browser.find_elements_by_class_name('gt_info_type')
            if len(mspan) > 0:
                info = mspan[0].text
                print('info:', info)
                if '验证失败:' in info:
                    time.sleep(2)
                    self.crack()
        except Exception as e:
            print(e)



if __name__ == '__main__':
    crack = Crack('username', 'passwd')
    crack.crack()
    print('验证成功')