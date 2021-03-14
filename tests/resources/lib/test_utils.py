from unittest import TestCase
from resources.lib.utils import m3u8_fix_audio, m3u8_without_av1, webvtt_to_srt


class UtilsTestCase(TestCase):

    def test_m3u8_without_av1(self):
        with open("./tests/mocks/hls_master.m3u8") as f:
            m3u8 = f.read()

        with open("./tests/mocks/hls_master_without_av1.m3u8") as f:
            m3u8_expected = f.read()

        # It removes AV1 streams
        m3u8_filtered = m3u8_without_av1(m3u8, "https://player.vimeo.com/play/c/522720145/hls")
        self.assertEqual(m3u8_expected, m3u8_filtered)

        # It leaves data as is if no AV1 stream is found
        m3u8_filtered = m3u8_without_av1(m3u8_expected, "https://player.vimeo.com/play/c/522720145/hls")
        self.assertEqual(m3u8_expected, m3u8_filtered)

    def test_m3u8_fixed_audio(self):
        with open("./tests/mocks/hls_master_without_av1.m3u8") as f:
            m3u8 = f.read()

        with open("./tests/mocks/hls_master_without_av1_fixed_audio.m3u8") as f:
            m3u8_expected = f.read()

        # It fixes audio URIs
        m3u8_filtered = m3u8_fix_audio(m3u8)
        self.assertEqual(m3u8_expected, m3u8_filtered)

    def test_webvtt_to_srt(self):
        with open("./tests/mocks/web.vtt") as f:
            webvtt = f.read()

        with open("./tests/mocks/web.srt") as f:
            srt = f.read()

        converted_subtitle = webvtt_to_srt(webvtt)
        self.assertEqual(srt, converted_subtitle)
