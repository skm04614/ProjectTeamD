import os.path
import inspect
import importlib.util
from glob import glob
from typing import Callable


def get_tests() -> dict[str, Callable]:
    test_functions = {}

    for test_file in glob(os.path.join(os.path.dirname(__file__), "tc_*.py")):
        spec = importlib.util.spec_from_file_location("", test_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        members = inspect.getmembers(module,
                                     predicate=lambda fn: inspect.isfunction(fn) and fn.__name__.startswith("tc_"))
        test_functions.update({member[1].__name__: member[1] for member in members})

    return test_functions


def execute_scenario(scenario: str) -> bool:
    testable_scenarios = get_tests()

    trimmed_scenario = scenario[:46]
    print(f"* {trimmed_scenario} {'-' * (50 - len(trimmed_scenario))} ",
          end="",
          flush=True)

    if scenario not in testable_scenarios:
        print("DOES NOT EXIST!!!")
        return False

    print("Run...", end="", flush=True)
    if not testable_scenarios[scenario]():
        print("FAIL!")
        return False

    print("Pass")
    return True
