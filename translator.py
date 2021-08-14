#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

import translators as ts

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


class Translate:
    """
    Класс переводчик текста
    """

    def __init__(
        self,
        from_language: str = "en",
        to_language: str = "ru",
        provider: str = "google",
    ) -> str:
        self.from_language = from_language
        self.to_language = to_language
        self.provider = provider
        if self.provider == "google":
            self.translate = ts.google

    def go(self, text: str) -> str:
        self.text = text
        self.result = str(
            self.translate(
                self.text,
                from_language=self.from_language,
                to_language=self.to_language,
            )
        )
        assert self.result != "", "Text not translated"
        return self.result
