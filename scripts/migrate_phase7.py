import sqlite3
from pathlib import Path

db_path = Path("backend/signbridge.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def add_col(table, col, col_def):
    cursor.execute(f"PRAGMA table_info({table})")
    cols = [info[1] for info in cursor.fetchall()]
    if col not in cols:
        print(f"Adding column '{col}' to table '{table}'...")
        cursor.execute(f"ALTER TABLE {table} ADD COLUMN {col} {col_def}")

add_col("phase5_validation_projects", "protocol_reference", "VARCHAR(100) DEFAULT 'SB-PILOT-2026-v1.0'")
add_col("phase5_validation_projects", "status", "VARCHAR(50) DEFAULT 'PREPARATION'")
add_col("phase5_validation_projects", "institutional_partner", "VARCHAR(200)")
add_col("phase5_validation_projects", "irb_approval_ref", "VARCHAR(100)")
add_col("phase5_validation_projects", "target_completion_date", "DATETIME")

add_col("phase5_validation_tasks", "assigned_reviewer_id", "INTEGER")
add_col("phase5_validation_tasks", "deadline", "DATETIME")
add_col("phase5_validation_tasks", "is_pilot_task", "BOOLEAN DEFAULT 0")

conn.commit()
conn.close()
print("Phase 7 database schema migration successfully applied.")
