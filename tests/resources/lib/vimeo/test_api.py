import json
import sys

from unittest import TestCase
from unittest.mock import MagicMock, Mock
sys.modules["xbmc"] = xbmcMock = MagicMock()
sys.modules["xbmcaddon"] = MagicMock()
sys.modules["xbmcgui"] = MagicMock()
from resources.lib.kodi.settings import Settings
from resources.lib.vimeo.api import Api, PasswordRequiredException


class ApiTestCase(TestCase):

    def setUp(self):
        self.api = Api(Settings(MagicMock()), "en", MagicMock(), MagicMock())
        self.api.api_cdn = "fastly_skyfire"
        xbmcMock.getUserAgent = Mock(return_value="A User-Agent String")

    def test_search_videos(self):
        with open("./tests/mocks/api_videos_search.json") as f:
            mock_data = f.read()

        self.api._do_api_request = Mock(return_value=json.loads(mock_data))

        self.api.video_av1 = True
        self.api.video_stream = "HLS (Adaptive)"
        res = self.api.search("foo", "bar")

        self.assertEqual(res.items[0].label, "kodi James")
        self.assertEqual(res.items[0].info["user"], "Foo User")
        self.assertEqual(res.items[0].uri, "/videos/13101116")
        self.assertEqual(res.items[0].hasSubtitles, False)
        self.assertEqual(res.items[0].thumb, "https://i.vimeocdn.com/video/74666133_200x150.jpg?r=pad")

        self.assertEqual(res.items[1].label, "Kodi Sings")
        self.assertEqual(res.items[1].info["user"], "Bar User")
        self.assertEqual(res.items[1].uri, "/videos/339780805")
        self.assertEqual(res.items[1].hasSubtitles, False)
        self.assertEqual(res.items[1].thumb, "https://i.vimeocdn.com/video/787910745_200x150.jpg?r=pad")

        # The third item is not playable, so it should not be listed
        self.assertEqual(len(res.items), 2)

    def test_search_videos_no_media_urls(self):
        with open("./tests/mocks/api_videos_search_fallback.json") as f:
            mock_data = f.read()

        self.api._do_api_request = Mock(return_value=json.loads(mock_data))
        self.api.video_stream = "720p"
        res = self.api.search("foo", "videos")

        self.assertEqual(res.items[0].uri, "/videos/13101116")

    def test_search_videos_on_demand(self):
        with open("./tests/mocks/api_videos_search_on_demand.json") as f:
            mock_data = f.read()

        self.api._do_api_request = Mock(return_value=json.loads(mock_data))
        self.api.video_stream = "HLS (Adaptive)"
        res = self.api.search("foo", "videos")

        self.assertEqual(res.items[0].uri, "/videos/372251058")
        self.assertEqual(res.items[0].info["onDemand"], False)

        self.assertEqual(res.items[1].uri, "/ondemand/pages/25096/videos/97663163")
        self.assertEqual(res.items[1].info["onDemand"], True)

        self.assertEqual(res.items[2].uri, "/videos/31158028")
        self.assertEqual(res.items[2].info["onDemand"], False)

    def test_search_videos_live(self):
        with open("./tests/mocks/api_videos_search_live.json") as f:
            mock_data = f.read()

        self.api._do_api_request = Mock(return_value=json.loads(mock_data))
        self.api.video_stream = "HLS (Adaptive)"
        res = self.api.search("foo", "videos")

        self.assertEqual(res.items[0].uri, "/videos/401626792")
        self.assertEqual(res.items[0].info["live"], True)

        self.assertEqual(res.items[1].uri, "/videos/76321431")
        self.assertEqual(res.items[1].info["live"], False)

    def test_search_users(self):
        with open("./tests/mocks/api_users_search.json") as f:
            mock_data = f.read()

        self.api._do_api_request = Mock(return_value=json.loads(mock_data))

        res = self.api.search("foo", "bar")

        self.assertEqual(res.items[0].label, "Petzl-sport")
        self.assertEqual(res.items[0].info["country"], "France")
        self.assertEqual(res.items[0].thumb, "https://i.vimeocdn.com/portrait/377115_300x300")
        self.assertEqual(res.items[0].uri, "/users/3255081/videos")

        self.assertEqual(res.items[1].label, "DSN Digital Sport Network")
        self.assertEqual(res.items[1].info["country"], "")
        self.assertEqual(res.items[1].thumb, "https://i.vimeocdn.com/portrait/18463331_300x300")
        self.assertEqual(res.items[1].uri, "/users/64177650/videos")

    def test_search_channels(self):
        with open("./tests/mocks/api_channels_search.json") as f:
            mock_data = f.read()

        self.api._do_api_request = Mock(return_value=json.loads(mock_data))

        res = self.api.search("foo", "bar")

        self.assertEqual(res.items[0].label, "Sport")
        self.assertEqual(res.items[0].thumb, "https://i.vimeocdn.com/video/801804973_640x360.jpg?r=pad")
        self.assertEqual(res.items[0].uri, "/channels/1084121/videos")

        self.assertEqual(res.items[1].label, "Jonica Sport")
        self.assertEqual(res.items[1].thumb, "https://i.vimeocdn.com/video/684400644_640x360.jpg?r=pad")
        self.assertEqual(res.items[1].uri, "/channels/452847/videos")

    def test_search_groups(self):
        with open("./tests/mocks/api_groups_search.json") as f:
            mock_data = f.read()

        self.api._do_api_request = Mock(return_value=json.loads(mock_data))

        res = self.api.search("foo", "bar")

        self.assertEqual(res.items[0].label, "Action Sport - Action Brothers")
        self.assertEqual(res.items[0].thumb, "https://i.vimeocdn.com/video/804634360_640x360.jpg?r=pad")
        self.assertEqual(res.items[0].uri, "/groups/15103/videos")

        self.assertEqual(res.items[1].label, "Sport")
        self.assertEqual(res.items[1].thumb, "https://i.vimeocdn.com/video/804929738_640x360.jpg?r=pad")
        self.assertEqual(res.items[1].uri, "/groups/809/videos")

    def test_channel_videos(self):
        with open("./tests/mocks/api_videos_channel.json") as f:
            mock_data = f.read()

        self.api._do_api_request = Mock(return_value=json.loads(mock_data))
        self.api.video_stream = "720p"

        res = self.api.channel("1")

        self.assertEqual(res.items[0].label, "The Pet Files")
        self.assertEqual(res.items[0].thumb, "https://i.vimeocdn.com/video/857679735_200x150.jpg?r=pad")
        self.assertEqual(res.items[0].uri, "/videos/392544832")

    def test_categories(self):
        with open("./tests/mocks/api_categories.json") as f:
            mock_data = f.read()

        self.api._do_api_request = Mock(return_value=json.loads(mock_data))

        res = self.api.categories()

        self.assertEqual(res.items[0].label, "Animation")
        self.assertEqual(res.items[0].thumb, "https://i.vimeocdn.com/video/858725975_640x360.jpg?r=pad")
        self.assertEqual(res.items[0].uri, "/categories/animation/videos")

        self.assertEqual(res.items[1].label, "Travel")
        self.assertEqual(res.items[1].thumb, "https://i.vimeocdn.com/video/649307891_640x360.jpg?r=pad")
        self.assertEqual(res.items[1].uri, "/categories/travel/videos")

    def test_trending(self):
        with open("./tests/mocks/api_videos_trending.json") as f:
            mock_data = f.read()

        self.api._do_api_request = Mock(return_value=json.loads(mock_data))

        res = self.api.categories()

        self.assertEqual(res.items[0].label, "Feeling Love for Filmfest Dresden")
        self.assertEqual(res.items[1].label, "Lecture: The Meeting with Nadav Kander")
        self.assertEqual(res.items[2].label, "Stay Home")

    def test_resolve_id(self):
        with open("./tests/mocks/api_videos_detail.json") as f:
            mock_data = f.read()

        self.api._do_api_request = Mock(return_value=json.loads(mock_data))

        res = self.api.resolve_id("352494023")

        self.assertEqual(res.items[0].label, "Beautiful Chaos")
        self.assertEqual(res.items[0].thumb, "https://i.vimeocdn.com/video/804395055_200x150.jpg?r=pad")
        self.assertEqual(res.items[0].uri, "/videos/352494023")

        with open("./tests/mocks/api_videos_detail_live.json") as f:
            mock_data = f.read()

        self.api._do_api_request = Mock(return_value=json.loads(mock_data))

        res = self.api.resolve_id("401749070")

        self.assertEqual(res.items[0].label, "Vespers & Benediction: 6PM (CT)")
        self.assertEqual(res.items[0].thumb, "https://i.vimeocdn.com/video/default-live_200x150?r=pad")
        self.assertEqual(res.items[0].uri, "/videos/401749070")

        with open("./tests/mocks/api_videos_detail_unlisted.json") as f:
            mock_data = f.read()

        self.api._do_api_request = Mock(return_value=json.loads(mock_data))

        res = self.api.resolve_id("355062058:5293454954")

        self.assertEqual(res.items[0].label, "An unlisted Vimeo Video")
        self.assertEqual(res.items[0].uri, "/videos/355062058:5293454954")

    def test_resolve_id_password_protected(self):
        with open("./tests/mocks/api_videos_detail_invalid_params.json") as f:
            mock_data = f.read()

        self.api._do_api_request = Mock(return_value=json.loads(mock_data))

        self.assertRaises(PasswordRequiredException, self.api.resolve_id, "216913310")

    def test_resolve_id_texttracks(self):
        with open("./tests/mocks/api_videos_detail_texttracks.json") as f:
            mock_data = f.read()

        self.api._do_api_request = Mock(return_value=json.loads(mock_data))

        res = self.api.resolve_id("140786188")

        self.assertEqual(res.items[0].label, "Impardonnable (English subtitle)")
        self.assertEqual(res.items[0].uri, "/videos/140786188")
        self.assertEqual(res.items[0].hasSubtitles, True)

    def test_resolve_media_url(self):
        with open("./tests/mocks/api_videos_detail.json") as f:
            mock_data = f.read()

        # Progressive
        self.api.video_av1 = False
        self.api.video_stream = "360p"
        self.api._do_api_request = Mock(return_value=json.loads(mock_data))
        res = self.api.resolve_media_url("/videos/352494023")
        self.assertEqual(res, "https://vimeo-prod-skyfire-std-us.storage.googleapis.com/01/498/14/352494023/1430794413.mp4")

        # Progressive (AV1)
        self.api.video_av1 = True
        self.api.video_stream = "1080p"
        self.api._do_api_request = Mock(return_value=json.loads(mock_data))
        res = self.api.resolve_media_url("/videos/352494023")
        self.assertEqual(res, "https://vimeo-prod-skyfire-std-us.storage.googleapis.com/01/498/14/352494023/1446202906.mp4")

        # Progressive (fallback)
        self.api.video_av1 = False
        self.api.video_stream = "720p"  # Resolution does not exist in API response
        self.api._do_api_request = Mock(return_value=json.loads(mock_data))
        res = self.api.resolve_media_url("/videos/352494023")
        self.assertEqual(res, "https://vimeo-prod-skyfire-std-us.storage.googleapis.com/01/498/14/352494023/1430794570.mp4")

        # HLS stream
        self.api.video_stream = "HLS (Adaptive)"
        self.api._do_api_request = Mock(return_value=json.loads(mock_data))
        res = self.api.resolve_media_url("/videos/352494023")
        self.assertEqual(res, "https://player.vimeo.com/play/1446216704/hls")

        with open("./tests/mocks/api_videos_detail_live.json") as f:
            mock_data = f.read()

        # Live stream (HLS)
        self.api.video_stream = "HLS (Adaptive)"
        self.api._do_api_request = Mock(return_value=json.loads(mock_data))
        res = self.api.resolve_media_url("/videos/401749070")
        self.assertEqual(res, "https://player.vimeo.com/live/7e80cc02-afdd-48fc-9a49-95078c7fbcd3/playlist/hls")

        # Live stream (HLS fallback)
        self.api.video_stream = "720p"
        self.api._do_api_request = Mock(return_value=json.loads(mock_data))
        res = self.api.resolve_media_url("/videos/401749070")
        self.assertEqual(res, "https://player.vimeo.com/live/7e80cc02-afdd-48fc-9a49-95078c7fbcd3/playlist/hls")

    def test_resolve_media_url_on_demand(self):
        with open("./tests/mocks/api_ondemand_video.json") as f:
            mock_data = f.read()

        self.api._do_api_request = Mock(return_value=json.loads(mock_data))
        self.api.video_stream = "HLS (Adaptive)"

        res = self.api.resolve_media_url("/ondemand/pages/25096")
        self.assertEqual(res, "https://player.vimeo.com/play/260864877/hls")

    def test_resolve_media_url_fallback(self):
        with open("./tests/mocks/player_video_config.json") as f:
            mock_data = f.read()

        self.api.api_fallback = True
        self.api.video_av1 = False

        # Progressive
        self.api.video_stream = "360p"
        self.api._do_player_request = Mock(return_value=json.loads(mock_data))
        res = self.api.resolve_media_url("/videos/13101116")
        self.assertEqual(res, "https://gcs-vimeo.akamaized.net/exp=1570994045~acl=%2A%2F1363060449.mp4%shortened")

        # Progressive (fallback)
        self.api.video_stream = "720p"
        self.api._do_player_request = Mock(return_value=json.loads(mock_data))
        res = self.api.resolve_media_url("/videos/13101116")
        self.assertEqual(res, "https://gcs-vimeo.akamaized.net/exp=1570994045~acl=%2A%2F1363060455.mp4%shortened")

        with open("./tests/mocks/player_video_config_av1.json") as f:
            mock_data = f.read()

        self.api.video_av1 = False

        # HLS stream
        self.api.video_stream = "HLS (Adaptive)"
        self.api._do_player_request = Mock(return_value=json.loads(mock_data))
        res = self.api.resolve_media_url("/videos/13101116")
        self.assertEqual(res, "https://skyfire.vimeocdn.com/avc")

        self.api.video_av1 = True

        # HLS stream (AV1)
        self.api.video_stream = "HLS (Adaptive)"
        self.api._do_player_request = Mock(return_value=json.loads(mock_data))
        res = self.api.resolve_media_url("/videos/13101116")
        self.assertEqual(res, "https://skyfire.vimeocdn.com/av1")

    def test_resolve_media_url_macos(self):
        with open("./tests/mocks/api_videos_detail.json") as f:
            mock_data = f.read()

        xbmcMock.getUserAgent = Mock(return_value="A Mac OS X User Agent")

        self.api.video_stream = "1080p"
        self.api._do_api_request = Mock(return_value=json.loads(mock_data))
        res = self.api.resolve_media_url("/videos/123")
        self.assertEqual(res, "http://a.b/c.mp4|User-Agent=pyvimeo%201.0.11%3B%20%28http%3A//developer.vimeo.com/api/docs%29")

    def test_text_tracks(self):
        with open("./tests/mocks/web.vtt") as f:
            mock_data_webvtt = f.read()

        with open("./tests/mocks/api_videos_texttracks.json") as f:
            mock_data = f.read()

        self.api._do_request = Mock(return_value=mock_data_webvtt)
        self.api._do_api_request = Mock(return_value=json.loads(mock_data))
        res = self.api.resolve_texttracks("/videos/12345/texttracks")

        self.assertEqual(res[0]["uri"], "/videos/503121159/texttracks/11718998")
        self.assertEqual(res[0]["language"], "en-US")
        self.assertTrue(res[0]["srt"].startswith("1\n00:00:08,850 --> 00:00:10,350\nMy love.\n\n"))

        self.assertEqual(res[1]["uri"], "/videos/503121159/texttracks/11719013")
        self.assertEqual(res[1]["language"], "fr")
