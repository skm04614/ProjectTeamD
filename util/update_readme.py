import os

from testing_suite import extract_latest_test_scenarios

_README_PATH = os.path.join(os.path.dirname(__file__), "../README.md")
_LATEST_TC_LIST_PATH = os.path.join(os.path.dirname(__file__), "../testing_suite/latest_test.list")


def update_readme():
    extract_latest_test_scenarios()
    with open(_LATEST_TC_LIST_PATH, "r", encoding="UTF-8") as f:
        new_tcs_content = f.readlines()

    with open(_README_PATH, "r", encoding="UTF-8") as f:
        readme_content = f.readlines()

    idx0 = readme_content.index("# Test 시나리오 리스트 조회\n") + 2
    idx1 = readme_content.index("# Test 수행\n") - 1
    new_readme_content = readme_content[:idx0] + new_tcs_content + readme_content[idx1:]

    with open(_README_PATH, "w", encoding="UTF-8") as file:
        file.write("".join(new_readme_content))


if __name__ == "__main__":
    update_readme()
