import csv
import sqlite3

seat_type = "ALL"

CSV_FILE = "CSAB_Round_{num}_Result_{seat_type}.csv"
DB_FILE = "CSAB_Seat_Allotment.db"

# Connect to SQLite
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS CSAB_Seat_Allotment(
    round INT,
    institute_name TEXT,
    academic_program TEXT,
    quota TEXT,
    seat_type TEXT,
    gender TEXT,
    opening_rank INT,
    closing_rank INT
);
""")
conn.commit()

for i in range(1, 4):
    rows_to_insert = []
    fp = CSV_FILE.format(num=i, seat_type=seat_type)
    with open(fp, 'r', newline='') as f:
        reader = csv.reader(f, delimiter='\t')

        for row in reader:
            row = [col.strip() for col in row]

            # Convert last 2 columns to int
            row[-2] = int(row[-2])
            row[-1] = int(row[-1])

            rows_to_insert.append(tuple(row))

    # Insert into DB
    cursor.executemany(f"""
    INSERT INTO CSAB_Seat_Allotment
    VALUES ({i}, ?, ?, ?, ?, ?, ?, ?)
    """, rows_to_insert)


    conn.commit()

    print(f"Round {i}: {len(rows_to_insert)} rows inserted")

conn.close()





