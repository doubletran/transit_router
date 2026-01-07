




from __future__ import annotations
from dotenv import load_dotenv
import os
from pathlib import Path
import sys
import psycopg

load_dotenv()


# -----------------------------
# 1) CONFIG (edit these)
# -----------------------------
GTFS_DIR = Path("routing/Data/GTFS/sfo/gtfs_o/")  # <-- change to your folder
FILE_EXT = ".txt"  # GTFS usually .txt (can be ".csv" if you renamed)


# Table -> (filename, columns_in_file_order)
# This matches your COPY statements.
TABLES = {
    "calendar": (
        "calendar.txt",
        [
            "service_id",
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",
            "start_date",
            "end_date",
        ],
    ),
    "calendar_dates": (
        "calendar_dates.txt",
        ["service_id", "date", "exception_type"],
    ),
    "stop_times": (
        "stop_times.txt",
        [
            "trip_id",
            "arrival_time",
            "departure_time",
            "stop_id",
            "stop_sequence",
            "stop_headsign",
            "shape_dist_traveled",
            "timepoint"
        ],
    ),
    "trips": (
        "trips.txt",
        [
            "route_id",
            "service_id",
            "trip_id",
            "trip_headsign",
            "direction_id",
            "block_id",
            "shape_id",
            "wheelchair_accessible",
            "bikes_allowed"
        ],
    ),

    "routes": (
        "routes.txt",
        [
            "route_id",
            "agency_id",
            "route_short_name",
            "route_long_name",
            "route_url",
            "route_desc",
            "route_type",
            "route_color",
            "route_text_color",
            "route_sort_order"
        ],
    ),
    "shapes": (
        "shapes.txt",
        ["shape_id", "shape_pt_lat", "shape_pt_lon", "shape_pt_sequence", "shape_dist_traveled"],
    ),
    "stops": (
        "stops.txt",
        [
            "stop_id",
            "stop_code",
            "stop_name",
            "stop_desc",
            "stop_lat",
            "stop_lon",
            "zone_id",
            "stop_url"
        ],
    ),
}


# -----------------------------
# 2) LOADER LOGIC
# -----------------------------
def build_copy_sql(table: str, columns: list[str]) -> str:
    # Using STDIN so Python streams the file content into Postgres.
    cols = ", ".join(columns)
    return f"""
        COPY {table} ({cols})
        FROM STDIN
        WITH (FORMAT csv, HEADER true, DELIMITER ',');
    """.strip()


def copy_file_into_table(conn: psycopg.Connection, table: str, file_path: Path, columns: list[str]) -> None:
    if not file_path.exists():
        raise FileNotFoundError(f"Missing file for {table}: {file_path}")

    sql = build_copy_sql(table, columns)

    # Stream file into COPY ... FROM STDIN
    # (Works regardless of whether Postgres is local or remote.)
    with conn.cursor() as cur, file_path.open("r", encoding="utf-8") as f:
        with cur.copy(sql) as copy:
            for line in f:
                copy.write(line)


def main() -> int:
    # Basic validation
    if not GTFS_DIR.exists():
        print(f"❌ GTFS_DIR not found: {GTFS_DIR}")
        return 1

    # Allow user to rename to .csv etc.
    # If you set FILE_EXT, we’ll override filenames that end with .txt
    tables_resolved: dict[str, tuple[Path, list[str]]] = {}
    for table, (fname, cols) in TABLES.items():
        f = Path(fname)
        if FILE_EXT and f.suffix != FILE_EXT:
            f = f.with_suffix(FILE_EXT)
        tables_resolved[table] = (GTFS_DIR / f.name, cols)

    print("Connecting to PostgreSQL...")
    conn = psycopg.connect(
          host=os.getenv("DB_HOST"),
          port=os.getenv("DB_PORT"),
          dbname="sfo_gtfs",
          user=os.getenv("DB_USER"),
          password=os.getenv("DB_PASSWORD")
      )

    try:
        # For a clean all-or-nothing load:
        conn.autocommit = False

        # Recommended load order (parents first)
        load_order = [
            "routes",
            "calendar",
            "calendar_dates",
            "trips",
            "stops",
            "shapes",
            "stop_times",
        ]

        for table in load_order:
            file_path, cols = tables_resolved[table]
            print(f"➡️  Loading {table} from {file_path} ...")
            copy_file_into_table(conn, table, file_path, cols)
            print(f"✅ Loaded {table}")

        conn.commit()
        print("🎉 All tables loaded successfully (COMMIT).")
        return 0

    except Exception as e:
        conn.rollback()
        print("❌ Load failed. Rolled back (no partial inserts).")
        print(f"Error: {e}")
        return 2

    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
