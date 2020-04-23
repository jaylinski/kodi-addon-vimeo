from unittest import TestCase
from resources.lib.vimeo.utils import webvtt_to_srt


class UtilsTestCase(TestCase):

    def test_webvtt_to_srt(self):
        with open("./tests/mocks/web.vtt") as f:
            webvtt = f.read()

        with open("./tests/mocks/web.srt") as f:
            srt = f.read()

        converted_subtitle = webvtt_to_srt(webvtt)
        self.assertEqual(srt, converted_subtitle)
