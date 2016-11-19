import asynctest

from joseph.core import Joseph


class TestCore(asynctest.TestCase):
    use_default_loop = True
    forbid_get_event_loop = False

    def setUp(self):
        self.joseph = Joseph()

    def tearDown(self):
        del self.joseph

    def test_test(self):
        self.assertTrue(True)
