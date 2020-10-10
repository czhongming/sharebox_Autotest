#!/usr/bin/env python
# encoding: utf-8
"""
@author: czm
@file: test_case_sharebox_whiteboard.py
@time: 2020/7/8 12:15
@desc:
"""
import time
import unittest
from utils.image_process import exists
from appium import webdriver
import os


class WhiteBoardTest(unittest.TestCase):
    def setUp(self) -> None:
        desired_caps = {
            'platformName': 'Android',
            'deviceName': '172.20.121.123',
            'appPackage': 'com.ruijie.whiteboard',
            'appActivity': 'com.zhishan.teamSoft.app.main.WhiteBoardActivity',
            'noReset': True,
        }
        self.driver = webdriver.Remote(
            command_executor='http://127.0.0.1:4723/wd/hub',
            desired_capabilities=desired_caps)
        time.sleep(3)

    def tearDown(self) -> None:
        self.driver.quit()

    def test_case_whiteboard(self):
        # 点击侧边栏，点击白板按钮
        self._click_side_bar()
        self._click_whiteboard_btn()
        # 检查是否成功进入白板
        time.sleep(2)
        self.assertTrue(self.driver.find_element_by_id("com.ruijie.whiteboard:id/iv_tool_preview_add"),
                        "进入白板失败")
        # 白板划线
        self.driver.swipe(400, 400, 800, 400)
        # 检查划线是否成功
        self.driver.save_screenshot("screen.png")
        self.assertTrue(exists("pen.png", "screen.png", need_completing_img_path=False), "白板书写不成功")
        os.remove("screen.png")
        # 添加白板页
        self.driver.find_element_by_id("com.ruijie.whiteboard:id/iv_tool_preview_add").click()
        time.sleep(1)
        # 检查是否添加成功
        page_num = self.driver.find_element_by_id("com.ruijie.whiteboard:id/tv_numAll").text
        self.assertTrue(page_num == str(2), "白板页添加错误，页码为{}".format(page_num))

    def _click_side_bar(self):
        self.driver.tap([(5, 540)])
        time.sleep(2)

    def _click_whiteboard_btn(self):
        self.driver.tap([(30, 400)])
