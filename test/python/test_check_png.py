from unittest import TestCase

from main.python.check_png import check_png


class Test(TestCase):
    def test_check_png(self):
        check_png("../resources/DSC_3_thumb.png")
