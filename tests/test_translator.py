#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest

from translator import Translate


class TestGoogleTranslate(unittest.TestCase):
    def test_en_to_ru(self):
        self.test_text = "Good morning"
        self.result_text = "Доброе утро"
        self.translate = Translate(
            from_language="en", to_language="ru", provider="google"
        )
        self.assertEqual(self.result_text, self.translate.go(self.test_text))

    def test_ru_to_en(self):
        self.test_text = "Доброе утро"
        self.result_text = "Good morning"
        self.translate = Translate(
            from_language="ru", to_language="en", provider="google"
        )
        self.assertEqual(self.result_text, self.translate.go(self.test_text))
