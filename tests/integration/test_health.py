def test_placeholder(db_session):
    """Verify the test database fixture works end-to-end."""
    from sqlalchemy import text

    result = db_session.execute(text("SELECT 1")).scalar()
    assert result == 1
