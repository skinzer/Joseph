import unittest

from joseph.exceptions import InvalidState
from joseph.utils import State


class TestState(unittest.TestCase):
    def setUp(self):
        self.state = State()
        self.default_states = (
            None,
            'STARTING',
            'RUNNING',
            'STOPPING',
            'STOPPED'
        )

    def tearDown(self):
        del self.state

    def test_test(self):
        self.assertTrue(True)

    def test_init(self):
        self.assertIsInstance(self.state, State)
        for state in self.default_states:
            self.assertIn(state, self.state.STATES)

    def test_custom_states(self):
        test_states = (
            "TEST_1",
            "TEST_2"
        )
        self.state = State(states=test_states)
        self.assertIn("TEST_1", self.state.STATES)
        self.assertNotIn("TEST_3", self.state.STATES)

        self.state.set_state("TEST_2")
        self.assertEqual(self.state, "TEST_2")

    def test_set_state(self):
        self.state.state = "STARTING"
        self.assertEqual(self.state, "STARTING")

        self.state.set_state("STARTING")
        self.assertEqual(self.state, "STARTING")

        with self.assertRaises(InvalidState):
            self.state.set_state("FOOBAR")

    def test_increase_state(self):
        self.assertEqual(self.state, None)
        self.state.increase_state()
        self.assertEqual(self.state, "STARTING")

    def test_decrease_state(self):
        self.state.set_state("STARTING")
        self.state.decrease_state()
        self.assertEqual(self.state, None)

    def test_current_index(self):
        self.assertEqual(self.state.current_index, 0)

        self.state.set_state("STARTING")
        self.assertEqual(self.state.current_index, 1)
        self.assertNotEqual(self.state.current_index, 0)

    def test_str(self):
        # Should return an empty string as no state has been set yet
        self.assertEqual(self.state, "")

        self.state.set_state("STARTING")
        self.assertEqual(self.state, "STARTING")

    def test_equal(self):
        self.assertTrue(self.state, None)
        self.assertFalse(self.state == False)
        self.assertFalse(self.state == True)
        self.assertFalse(self.state == "FOO")

        self.state.increase_state()
        self.assertEqual(self.state, "STARTING")
        self.assertTrue(self.state == "STARTING")
        self.assertFalse(self.state == True)
