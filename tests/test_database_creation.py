from waystone.extensions import db


def test_database_creation(client):
    # test that the created tables are actually created in the database
    expected_tables = ["project", "milestone", "criteria"]
    actual_tables = db.metadata.tables.keys()

    for table in expected_tables:
        assert table in actual_tables
        print(f"Table {table} exists in the database")

    
