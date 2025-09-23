from hypothesis import given, strategies as st
from evolution.core.cell import Cell
from evolution.behaviors.strategies import random_walk_strategy

# A strategy for generating valid energy values
positive_floats = st.floats(min_value=0, max_value=100, allow_nan=False, allow_infinity=False)

@given(energy=positive_floats, x=st.integers(min_value=0, max_value=100), y=st.integers(min_value=0, max_value=100))
def test_cell_energy_is_always_non_negative(energy, x, y):
    """Tests that a cell's energy is never negative."""
    cell = Cell(energy=energy, x=x, y=y, strategy=random_walk_strategy, genome=None)
    assert cell.energy >= 0
