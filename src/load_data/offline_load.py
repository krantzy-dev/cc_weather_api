import logging
from pathlib import Path

from sqlalchemy import text
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

SAMPLE_DUMP_PATH = Path(__file__).resolve().parent.parent.parent / "db" / "sample_dump.sql"

# Sequences must be resynced after inserting rows with explicit IDs, since
# --data-only dumps do not include sequence state.
_TABLES_WITH_SERIAL_ID = ["location", "metric", "measurement"]


def run_offline_load(db: Session) -> None:
    """Load a static, pre-captured dataset instead of live Open-Meteo data.

    Used when ONLINE=false, so the API can be demoed without network
    access. Executes the INSERT statements in db/sample_dump.sql, captured
    from a real backfill run, then resyncs auto-increment sequences so
    subsequently created rows don't collide with the dumped IDs.

    Args:
        db: Database session.
    """
    if not SAMPLE_DUMP_PATH.exists():
        logger.warning("sample dump not found at %s, skipping offline load", SAMPLE_DUMP_PATH)
        return

    sql = SAMPLE_DUMP_PATH.read_text()

    sql_lines = [
        line
        for line in sql.splitlines()
        if not line.strip().startswith("--") and not line.strip().startswith("\\")
    ]
    sql_without_comments = "\n".join(sql_lines)

    statements = [
        s.strip() for s in sql_without_comments.split(";") if s.strip() and "search_path" not in s
    ]

    db.execute(text("SET search_path TO public"))

    for statement in statements:
        db.execute(text(statement))

    for table in _TABLES_WITH_SERIAL_ID:
        db.execute(
            text(
                f"SELECT setval(pg_get_serial_sequence('{table}', 'id'), "
                f"COALESCE((SELECT MAX(id) FROM {table}), 1))"
            )
        )

    db.commit()
    logger.info("offline load complete: %d rows inserted", len(statements))
