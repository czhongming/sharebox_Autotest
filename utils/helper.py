#!/usr/bin/env python
# encoding: utf-8
"""
@author: lee
@file: helper.py
@time: 2020/7/7 9:05
@desc:
"""
import time


class G(object):
    """Represent the globals variables"""
    BASEDIR = []
    ARM = None
    ENABLE_ARM = False

    @classmethod
    def add_arm(cls, arm):
        """
        Add device instance in G and set as current device.

        Examples:
            G.add_arm(Arm())

        Args:
            arm: arm to init

        Returns:
            None

        """
        cls.ARM = arm


def delay_after_operation():
    time.sleep(0.1)
