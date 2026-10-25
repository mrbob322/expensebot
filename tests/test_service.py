import pytest
from expensebot import ExpenseService, NotFoundError, ValidationError


def test_add_get_delete(tmp_path):
    s = ExpenseService(str(tmp_path / "t.db"))
    e = s.add(100, "Еда", "обед")
    assert s.get(e.id).amount == 100
    s.delete(e.id)
    with pytest.raises(NotFoundError):
        s.get(e.id)


def test_validation(tmp_path):
    s = ExpenseService(str(tmp_path / "t.db"))
    with pytest.raises(ValidationError):
        s.add(0, "Еда")
