"""
tests/step_defs/test_add_to_cart.py

Binds the add_to_cart.feature scenarios to pytest-bdd.
All step definitions are resolved from tests/conftest.py.
"""

import pytest
from pytest_bdd import scenarios, parsers, given, when, then

# Wire every Scenario in the feature file to this test module.
scenarios("add_to_cart.feature")

# ── Scenario Outline specific step (inline example) ───────────────────────────
# The Outline's <qty> and <expected_total> are already handled by the shared
# steps in conftest.py.  Nothing extra needed here — scenarios() picks them up.
