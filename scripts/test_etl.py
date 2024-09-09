import unittest
from scripts.etl import extract_data, transform_data
from datetime import datetime

class TestETL(unittest.TestCase):

    def test_extract_data(self):
        data = extract_data()
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

    def test_transform_data(self):
        data = [(1, 1, 23.5, 60.2, datetime.now())]
        transformed = transform_data(data)
        self.assertEqual(len(transformed), 1)
        self.assertIn("temperature_celsius", transformed[0])

if __name__ == "__main__":
    unittest.main()