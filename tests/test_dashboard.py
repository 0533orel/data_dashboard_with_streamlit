import unittest
import pandas as pd
from dashboard_data import filter_movies, load_movies
from streamlit.testing.v1 import AppTest

class DashboardTests(unittest.TestCase):
    def test_filters_intersect(self):
        data = pd.DataFrame({"genre": ["Drama","Drama","Comedy"], "year": [2000,2020,2000], "score": [8,8,8]})
        self.assertEqual(list(filter_movies(data, ["Drama"], (1999,2001), (7,9)).index), [0])
        self.assertTrue(filter_movies(data, [], (1999,2021), (0,10)).empty)

    def test_repository_dataset(self):
        data = load_movies()
        self.assertFalse(data.empty)
        self.assertFalse(data[["name","genre","year","score"]].isna().any().any())

    def test_ui_and_empty_state(self):
        app = AppTest.from_file("data_analysis.py").run(timeout=30)
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(len(app.metric), 3)
        app.sidebar.multiselect[0].set_value([]).run()
        self.assertEqual(len(app.exception), 0)
        self.assertIn("No movies", app.info[0].value)

if __name__ == "__main__":
    unittest.main()
