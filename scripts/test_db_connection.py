import os
import sys

import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    print("DATABASE_URL not set. Check your .env file.")
    sys.exit(1)


def main():
    print("Connecting to Supabase Postgres...")
    conn = psycopg2.connect(DATABASE_URL, connect_timeout=10)

    try:
        with conn.cursor() as cur:
            # 1. Basic connectivity + version
            cur.execute("SELECT version();")
            print("Connected. Postgres version:")
            print(" ", cur.fetchone()[0])

            # 2. Confirm pgvector is actually enabled, not just assumed
            cur.execute(
                "SELECT extname, extversion FROM pg_extension WHERE extname = 'vector';"
            )
            row = cur.fetchone()
            if row:
                print(f"pgvector enabled (version {row[1]}).")
            else:
                print("pgvector NOT enabled — go back to Step 2.")
                sys.exit(1)

            # 3. Functional check, not just a metadata check — actually use the type
            cur.execute("SELECT '[1,2,3]'::vector AS test_vector;")
            print("Vector type functional test:", cur.fetchone()[0])

            # 4. Cosine distance operator sanity check, since that's what you'll
            #    actually be using for dedup similarity scoring in Week 3
            cur.execute("SELECT '[1,2,3]'::vector <=> '[1,2,4]'::vector AS cosine_distance;")
            print("Cosine distance operator works:", cur.fetchone()[0])

        conn.commit()
        print("\nAll checks passed.")

    except Exception as e:
        print(f"\nConnection or query failed: {e}")
        sys.exit(1)

    finally:
        conn.close()


if __name__ == "__main__":
    main()