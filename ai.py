import mysql.connector
import datetime
import json
from prompt import generate_with_gemini, base_prompt

# connect to your database
conn = mysql.connector.connect(
    host="sql102.infinityfree.com",
    user="if0_38953247",
    password="Qt13112007",
    database="if0_38953247_dbEngTest"
)

cursor = conn.cursor()

def insert_into_db(category, questions):
    table_name = f"db{category}"
    for q in questions:
        sql = f"""
        INSERT INTO {table_name} (COL2, COL3, COL4, generated_at)
        VALUES (%s, %s, %s, NOW())
        """
        data = (
            q["question"],
            q["answer"],
            q["explanation"],
        )
        cursor.execute(sql, data)   

categories = ["Grammar", "Vocabulary", "Reading", "Wordform", "GuidedCloze", "Phonetics", "Rearrangement", "SentenceTransformation", "Stress"]
for category in categories:
    prompt = base_prompt(category)
    questions = json.loads(generate_with_gemini(prompt))
    insert_into_db(category, questions)

conn.commit()
cursor.close()
conn.close()
print(f"[{datetime.datetime.now()}] Questions inserted.")