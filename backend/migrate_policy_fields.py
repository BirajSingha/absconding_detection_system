from app import create_app, db
from sqlalchemy import text

def migrate():
    app = create_app()
    with app.app_context():
        print("Starting migration...")
        
        # List of columns to add and their types
        columns = [
            ("joining_date", "DATE"),
            ("probation_end_date", "DATE"),
            ("notice_period_days", "INTEGER DEFAULT 60"),
            ("service_bond_active", "BOOLEAN DEFAULT 1"), # SQLite uses 1 for True
            ("bond_penalty_amount", "FLOAT DEFAULT 100000.0")
        ]
        
        with db.engine.connect() as conn:
            for col_name, col_type in columns:
                try:
                    # Check if column exists strictly (SQLite pragma) or just try adding
                    # "ALTER TABLE candidates ADD COLUMN..."
                    conn.execute(text(f"ALTER TABLE candidates ADD COLUMN {col_name} {col_type}"))
                    print(f"Added column: {col_name}")
                except Exception as e:
                    if "duplicate column name" in str(e).lower():
                        print(f"Column {col_name} already exists.")
                    else:
                        print(f"Error adding {col_name}: {e}")
            
            conn.commit()
        print("Migration complete.")

if __name__ == "__main__":
    migrate()
