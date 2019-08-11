import json
import sys
from unittest import TestCase
from unittest.mock import MagicMock, Mock
sys.modules['xbmc'] = MagicMock()
sys.modules['xbmcaddon'] = MagicMock()
sys.modules['xbmcgui'] = MagicMock()
from resources.lib.kodi.settings import Settings
from resources.lib.vimeo.api import Api


class ApiTestCase(TestCase):

    def setUp(self):
        self.api = Api(settings=Settings(MagicMock()), lang="en", vfs=MagicMock())
        self.api.api_cdn = "fastly_skyfire"

    def test_search(self):
        with open("./tests/mocks/api_videos_search.json") as f:
            mock_data = f.read()

        self.api._do_api_request = Mock(return_value=json.loads(mock_data))

        res = self.api.search("foo", "bar")

        self.assertEqual(res.items[0].label, "kodi James")
        self.assertEqual(res.items[0].info["user"], "Foo User")
        self.assertEqual(res.items[0].uri, "/videos/13101116")
        self.assertEqual(res.items[0].thumb, "https://i.vimeocdn.com/video/74666133_200x150.jpg?r=pad")

        self.assertEqual(res.items[1].label, "Kodi Sings")
        self.assertEqual(res.items[1].info["user"], "Bar User")
        self.assertEqual(res.items[1].uri, "/videos/339780805")
        self.assertEqual(res.items[1].thumb, "https://i.vimeocdn.com/video/787910745_200x150.jpg?r=pad")

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

    def test_resolve_id(self):
        with open("./tests/mocks/api_videos_detail.json") as f:
            mock_data = f.read()

        self.api._do_api_request = Mock(return_value=json.loads(mock_data))

        res = self.api.resolve_id("352494023")
        self.assertEqual(res.items[0].label, "Beautiful Chaos")
        self.assertEqual(res.items[0].thumb, "https://i.vimeocdn.com/video/804395055_200x150.jpg?r=pad")
        self.assertEqual(res.items[0].uri, "/videos/352494023")

    def test_resolve_media_url(self):
        with open("./tests/mocks/api_video_config.json") as f:
            mock_data = f.read()

        self.api._hls_playlist_master_remove_av1_streams = Mock(return_value="/local/path")

        # HLS stream
        self.api.video_stream = "HLS (Adaptive)"
        self.api._do_player_request = Mock(return_value=json.loads(mock_data))
        res = self.api.resolve_media_url("/videos/13101116")
        self.assertEqual(res, "/local/path")

        # Progressive
        self.api.video_stream = "360p"
        self.api._do_player_request = Mock(return_value=json.loads(mock_data))
        res = self.api.resolve_media_url("/videos/13101116")
        self.assertEqual(res, "https://gcs-vimeo.akamaized.net/exp=1560644298~acl=%2A%2F1363060449.mp4%shortened")

        # Progressive (fallback)
        self.api.video_stream = "720p"
        self.api._do_player_request = Mock(return_value=json.loads(mock_data))
        res = self.api.resolve_media_url("/videos/13101116")
        self.assertEqual(res, "https://gcs-vimeo.akamaized.net/exp=1560644298~acl=%2A%2F1363060455.mp4%shortened")

        with open("./tests/mocks/api_video_config_av1.json") as f:
            mock_data = f.read()

        # HLS stream (AV1 fallback)
        self.api.video_stream = "HLS (Adaptive)"
        self.api._do_player_request = Mock(return_value=json.loads(mock_data))
        res = self.api.resolve_media_url("/videos/13101116")
        self.assertEqual(res, "/local/path")
