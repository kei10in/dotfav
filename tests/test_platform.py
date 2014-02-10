# -*- coding: utf-8 -*-

from dotfav.symlink import PlatformFilter


class TestPlatformFilter():
    def test_returns_empty_on_empty_config(self):
        config = []
        sut = PlatformFilter()
        assert len(list(sut(config))) == 0

    def test_returns_empty_on_no_supported_platform(self):
        config = [{
            'os' : ['win32'],
            'targets' : [['src', 'dest']]
        }]
        sut = PlatformFilter('linux')
        assert len(list(sut(config))) == 0

    def test_returns_targets_if_platform_matched(self):
        config = [{
            'os' : ['linux'],
            'targets' : [['src', 'dest']]
        }]
        sut = PlatformFilter('linux')
        actual = list(sut(config))
        assert len(actual) == 1
        assert actual[0] == ('src', 'dest')
