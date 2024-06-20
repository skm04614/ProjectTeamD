import importlib
import sys

import scenario_test.scenario


def run_scenario(scenario_name):
    try:
        importlib.reload(sys.modules['scenario_test.scenario'])
        import scenario_test.scenario

        scenario_class = getattr(scenario_test.scenario, scenario_name.upper(), None)
        if scenario_class is None:
            raise AttributeError("INVALID COMMAND")

        scenario_instance = scenario_class()
        scenario_instance.execute()

    except AttributeError as e:
        print(e)
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scenario_runner.py <scenario_name>")
    else:
        run_scenario(sys.argv[1])
