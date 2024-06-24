import pstats
import cProfile
import unittest


def run_tests():
    loader = unittest.TestLoader()
    suite = loader.discover("..")
    runner = unittest.TextTestRunner()
    runner.run(suite)


if __name__ == "__main__":
    cProfile.run("run_tests()",
                 "unit_tests.prof")

    p = pstats.Stats("unit_tests.prof")
    p.sort_stats("cumulative").print_stats(20)

