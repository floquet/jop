import unittest
from geo_utils.satellite_utils import read_satellite_file, group_satellites, generate_latex

class TestSatelliteUtils(unittest.TestCase):

    def test_read_satellite_file(self):
        # Mock satellite file content
        test_file = "test_satellites.txt"
        with open(test_file, "w") as f:
            f.write("Line 1\nLine 2\nLine 3\nLine 4\nLine 5\nLine 6\n")
        
        data = read_satellite_file(test_file)
        self.assertEqual(data, ["Line 1", "Line 4"])

    def test_group_satellites(self):
        data = ["ASIASAT 8 (AMOS-7)", "ASIASAT 9", "AEHF-1 (USA 214)"]
        grouped = group_satellites(data)
        self.assertIn("ASIASAT", grouped)
        self.assertEqual(len(grouped["ASIASAT"]), 2)
        self.assertIn("AEHF", grouped)

    def test_generate_latex(self):
        grouped = {"ASIASAT": ["ASIASAT 8 (AMOS-7)", "ASIASAT 9"]}
        latex = generate_latex(grouped)
        self.assertIn("\\begin{enumerate}", latex)
        self.assertIn("\\item ASIASAT", latex)
        self.assertIn("\\item ASIASAT 8 (AMOS-7)", latex)

if __name__ == "__main__":
    unittest.main()

