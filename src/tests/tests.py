from unittest import TestCase

from src.simple_solution.towerjumps import run as simple_run
from src.accurate_solution.towerjumps import run as accurate_run

MOCK_INPUT_ALL_TOWERS_SAME_STATE = "src/tests/mock_inputs/all_towers_in_same_state.csv"
MOCK_INPUT_BOUNDARY_TOWERS_DIFFERENT_STATES = "src/tests/mock_inputs/boundary_towers_in_different_states.csv"
MOCK_INPUT_BOUNDARY_TOWERS_DIFFERENT_STATES_EVENLY = "src/tests/mock_inputs/boundary_towers_in_different_states_evenly.csv"

class Tests(TestCase):
    def test_all_towers_in_same_state(self):
        simple_results = simple_run(MOCK_INPUT_ALL_TOWERS_SAME_STATE, generate_csv=False)
        self.assertEqual(simple_results, '2021-01-03 21:00:00,New York,100.0')

        accurate_results = accurate_run(MOCK_INPUT_ALL_TOWERS_SAME_STATE, generate_csv=False)
        self.assertEqual(accurate_results, '2021-01-03 21:00:00,New York,100.0')

    def test_boundary_towers_in_different_states(self):
        simple_results = simple_run(MOCK_INPUT_BOUNDARY_TOWERS_DIFFERENT_STATES, generate_csv=False)
        self.assertEqual(simple_results, '2021-01-06 02:15:00,New York,66.67')

        # Even though we have more pings in NY, the average point belongs to CT. The confidence level could be higher if CT pings were farther from the border.
        accurate_results = accurate_run(MOCK_INPUT_BOUNDARY_TOWERS_DIFFERENT_STATES, generate_csv=False)
        self.assertEqual(accurate_results, '2021-01-06 02:15:00,Connecticut,56.09')
    
    def test_boundary_towers_in_different_states_evenly(self):
        simple_results = simple_run(MOCK_INPUT_BOUNDARY_TOWERS_DIFFERENT_STATES_EVENLY, generate_csv=False)
        self.assertEqual(simple_results, '2021-01-06 03:00:00,Connecticut,50.0')

        # Even though we have the same amount of pings in both states, the average point belongs to CT, this increases the confidence.
        accurate_results = accurate_run(MOCK_INPUT_BOUNDARY_TOWERS_DIFFERENT_STATES_EVENLY, generate_csv=False)
        self.assertEqual(accurate_results, '2021-01-06 03:00:00,Connecticut,88.96')