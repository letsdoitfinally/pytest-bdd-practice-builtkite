"""
conftest.py (root) — pytest hooks for BDD scenario reporting.
"""

import logging

logger = logging.getLogger("bdd")
logging.basicConfig(level=logging.INFO, format="%(message)s")


def pytest_bdd_before_scenario(request, feature, scenario):
    logger.info("\n┌─ SCENARIO: %s", scenario.name)
    logger.info("│  Feature : %s", feature.name)


def pytest_bdd_after_scenario(request, feature, scenario):
    # rep_call is NOT available here (set during teardown).
    # Use a flag set by pytest_bdd_step_error instead.
    had_error = getattr(request.node, "_bdd_step_failed", False)
    status = "FAILED ✗" if had_error else "PASSED ✓"
    logger.info("└─ %s\n", status)


def pytest_bdd_step_error(request, feature, scenario, step, step_func, step_func_args, exception):
    request.node._bdd_step_failed = True   # flag read by after_scenario
    logger.error("   ✗ Step failed: %s %s", step.keyword, step.name)
    logger.error("     Error: %s", exception)


def pytest_bdd_after_step(request, feature, scenario, step, step_func, step_func_args):
    logger.info("│  ✓ %s %s", step.keyword, step.name)
