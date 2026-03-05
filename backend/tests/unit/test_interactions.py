"""Unit tests for interaction filtering logic."""

from app.models.interaction import InteractionLog
from app.routers.interactions import _filter_by_item_id


def _make_log(id: int, learner_id: int, item_id: int) -> InteractionLog:
    return InteractionLog(id=id, learner_id=learner_id, item_id=item_id, kind="attempt")


def test_filter_returns_all_when_item_id_is_none() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, None)
    assert result == interactions


def test_filter_returns_empty_for_empty_input() -> None:
    result = _filter_by_item_id([], 1)
    assert result == []


def test_filter_returns_interaction_with_matching_ids() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, 1)
    assert len(result) == 1
    assert result[0].id == 1

# backend/tests/unit/test_interactions.py

def test_filter_excludes_interaction_with_different_learner_id() -> None:
    """Test that filter includes interactions with matching item_id but different learner_id."""
    interactions = [
        _make_log(1, 1, 1),  # id=1, learner_id=1, item_id=1
        _make_log(2, 2, 1),  # id=2, learner_id=2, item_id=1 - этот должен быть включен
        _make_log(3, 1, 2),  # id=3, learner_id=1, item_id=2
        _make_log(4, 2, 2),  # id=4, learner_id=2, item_id=2
    ]

    result = _filter_by_item_id(interactions, 1)

    assert len(result) == 2
    assert result[0].id == 1
    assert result[0].learner_id == 1
    assert result[0].item_id == 1
    assert result[1].id == 2
    assert result[1].learner_id == 2
    assert result[1].item_id == 1

# ============= НОВЫЕ ТЕСТЫ ДЛЯ EDGE CASES =============

def test_filter_with_item_id_zero_returns_empty() -> None:
    """Test that filtering with item_id=0 returns empty list when no interactions have item_id=0."""
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, 0)
    assert result == []


def test_filter_with_negative_item_id_returns_empty() -> None:
    """Test that filtering with negative item_id returns empty list."""
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, -1)
    assert result == []


def test_filter_with_max_item_id() -> None:
    """Test filtering with very large item_id."""
    interactions = [_make_log(1, 1, 999999), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, 999999)
    assert len(result) == 1
    assert result[0].id == 1
    assert result[0].item_id == 999999


def test_filter_with_multiple_matching_items() -> None:
    """Test filtering when multiple interactions have the same item_id."""
    interactions = [
        _make_log(1, 1, 1),
        _make_log(2, 2, 1),
        _make_log(3, 3, 1),
        _make_log(4, 4, 2),
        _make_log(5, 5, 3),
    ]
    result = _filter_by_item_id(interactions, 1)
    assert len(result) == 3
    assert all(i.item_id == 1 for i in result)
    assert [i.id for i in result] == [1, 2, 3]


def test_filter_preserves_interaction_kind() -> None:
    """Test that filtering preserves all attributes including kind."""
    interactions = [
        InteractionLog(id=1, learner_id=1, item_id=1, kind="view"),
        InteractionLog(id=2, learner_id=2, item_id=1, kind="attempt"),
        InteractionLog(id=3, learner_id=3, item_id=1, kind="complete"),
    ]
    result = _filter_by_item_id(interactions, 1)
    assert len(result) == 3
    assert [i.kind for i in result] == ["view", "attempt", "complete"]
