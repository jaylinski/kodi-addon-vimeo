import json
import sys
from unittest import TestCase
from unittest.mock import MagicMock, Mock
sys.modules["xbmc"] = MagicMock()
sys.modules["xbmcaddon"] = MagicMock()
sys.modules["xbmcgui"] = MagicMock()
from resources.lib.kodi.settings import Settings
from resources.lib.vimeo.api import Api


class ApiTestCase(TestCase):

    def setUp(self):
        self.api = Api(Settings(MagicMock()), "en", MagicMock(), MagicMock())
        self.api.api_cdn = "fastly_skyfire"

    def test_search_videos(self):
        with open("./tests/mocks/api_videos_search.json") as f:
            mock_data = f.read()

        self.api._do_api_request = Mock(return_value=json.loads(mock_data))

        self.api.video_av1 = True
        self.api.video_stream = "HLS (Adaptive)"
        res = self.api.search("foo", "bar")

        self.assertEqual(res.items[0].label, "kodi James")
        self.assertEqual(res.items[0].info["user"], "Foo User")
        self.assertEqual(res.items[0].uri, "https://player.vimeo.com/play/23910873/hls")
        self.assertEqual(res.items[0].thumb, "https://i.vimeocdn.com/video/74666133_200x150.jpg?r=pad")
        self.assertEqual(res.items[0].info["mediaUrlResolved"], True)

        self.assertEqual(res.items[1].label, "Kodi Sings")
        self.assertEqual(res.items[1].info["user"], "Bar User")
        self.assertEqual(res.items[1].uri, "https://player.vimeo.com/play/1352990485,1352990483,1352990478/hls")
        self.assertEqual(res.items[1].thumb, "https://i.vimeocdn.com/video/787910745_200x150.jpg?r=pad")
        self.assertEqual(res.items[1].info["mediaUrlResolved"], True)

        self.api.video_stream = "720p"
        res = self.api.search("foo", "videos")

        self.assertEqual(res.items[0].uri, "https://vimeo-prod-skyfire-std-us.storage.googleapis.com/01/2620/0/13101116/23910873.mp4")
        self.assertEqual(res.items[0].info["mediaUrlResolved"], True)

    def test_search_videos_av1(self):
        with open("./tests/mocks/api_videos_search_av1.json") as f:
            mock_data = f.read()

        self.api._do_api_request = Mock(return_value=json.loads(mock_data))
        self.api._hls_playlist_sanitize = Mock(return_value="/local/path")

        self.api.video_av1 = False
        self.api.video_stream = "HLS (Adaptive)"
        res = self.api.search("foo", "bar")

        self.assertEqual(res.items[0].label, "The Pet Files")
        self.assertEqual(res.items[0].uri, "https://player.vimeo.com/play/1666570518,1666570517,1666570516,1666570515,1666570514,1663613697,1663613671,1663613568,1663612618,1663612616/hls?")
        self.assertEqual(res.items[0].info["mediaUrlResolved"], True)

        self.api.video_stream = "1080p"
        res = self.api.search("foo", "bar")

        self.assertEqual(res.items[0].label, "The Pet Files")
        self.assertEqual(res.items[0].uri, "https://vimeo-prod-skyfire-std-us.storage.googleapis.com/01/3508/15/392544832/1663613697.mp4")

        self.api.video_av1 = True
        res = self.api.search("foo", "bar")

        self.assertEqual(res.items[0].label, "The Pet Files")
        self.assertEqual(res.items[0].uri, "https://vimeo-prod-skyfire-std-us.storage.googleapis.com/01/3508/15/392544832/1666570518.mp4")

    def test_search_videos_no_media_urls(self):
        with open("./tests/mocks/api_videos_search_fallback.json") as f:
            mock_data = f.read()

        self.api._do_api_request = Mock(return_value=json.loads(mock_data))
        self.api.video_stream = "720p"
        res = self.api.search("foo", "videos")

        self.assertEqual(res.items[0].uri, "/videos/13101116")
        self.assertEqual(res.items[0].info["mediaUrlResolved"], False)

    def test_search_videos_on_demand(self):
        with open("./tests/mocks/api_videos_search_on_demand.json") as f:
            mock_data = f.read()

        self.api._do_api_request = Mock(return_value=json.loads(mock_data))
        self.api.video_stream = "HLS (Adaptive)"
        res = self.api.search("foo", "videos")

        self.assertEqual(res.items[0].uri, "https://player.vimeo.com/play/1546650582/hls")
        self.assertEqual(res.items[0].info["mediaUrlResolved"], True)
        self.assertEqual(res.items[0].info["onDemand"], False)

        self.assertEqual(res.items[1].uri, "/ondemand/pages/25096/videos/97663163")
        self.assertEqual(res.items[1].info["mediaUrlResolved"], False)
        self.assertEqual(res.items[1].info["onDemand"], True)

        self.assertEqual(res.items[2].uri, "https://player.vimeo.com/play/120186138/hls")
        self.assertEqual(res.items[2].info["mediaUrlResolved"], True)
        self.assertEqual(res.items[2].info["onDemand"], False)

    def test_search_videos_no_hls(self):
        with open("./tests/mocks/api_videos_search_no_hls.json") as f:
            mock_data = f.read()

        self.api._do_api_request = Mock(return_value=json.loads(mock_data))
        self.api.video_stream = "HLS (Adaptive)"
        res = self.api.search("foo", "videos")

        self.assertEqual(res.items[0].label, "Zygote Balls at BIP, Florence, Italy")
        self.assertEqual(res.items[0].uri, "https://vimeo-prod-skyfire-std-us.storage.googleapis.com/01/54/0/270719/15090045.mp4")

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

        self.api.video_av1 = False
        res = self.api.channel("1")

        self.assertEqual(res.items[0].label, "The Pet Files")
        self.assertEqual(res.items[0].thumb, "https://i.vimeocdn.com/video/857679735_200x150.jpg?r=pad")
        self.assertEqual(res.items[0].uri, "https://vimeo-prod-skyfire-std-us.storage.googleapis.com/01/3508/15/392544832/1663613568.mp4")
        self.assertEqual(res.items[0].info["mediaUrlResolved"], True)

        self.api.video_av1 = True
        res = self.api.channel("1")

        self.assertEqual(res.items[0].label, "The Pet Files")
        self.assertEqual(res.items[0].thumb, "https://i.vimeocdn.com/video/857679735_200x150.jpg?r=pad")
        self.assertEqual(res.items[0].uri, "https://vimeo-prod-skyfire-std-us.storage.googleapis.com/01/3508/15/392544832/1666570517.mp4")

    def test_resolve_id(self):
        with open("./tests/mocks/api_videos_detail.json") as f:
            mock_data = f.read()

        self.api._do_api_request = Mock(return_value=json.loads(mock_data))

        res = self.api.resolve_id("352494023")

        self.assertEqual(res.items[0].label, "Beautiful Chaos")
        self.assertEqual(res.items[0].thumb, "https://i.vimeocdn.com/video/804395055_200x150.jpg?r=pad")
        self.assertEqual(res.items[0].uri, "/videos/352494023")

    def test_resolve_media_url(self):
        res = self.api.resolve_media_url("https://player.vimeo.com/play/1663612616/hls?123")
        self.assertEqual(res, "https://player.vimeo.com/play/1663612616/hls?123")

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

        # HLS stream (AV1)
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
