import mysql.connector
import datetime
import json
from prompt import generate_with_gemini, base_prompt

# connect to your database
conn = mysql.connector.connect(
    host="sql.freedb.tech",
    user="freedb_SilvEduEng",
    password="@5fr7VubE4k*cX4",
    database="freedb_dbEngTest"
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

categories = ["Grammar", "Vocabulary", "Reading", "WordForm", "GuidedCloze", "Phonetics", "Rearrangement", "SentenceTransformation", "Stress"]
for category in categories:
    prompt = base_prompt(category)
    questions = json.loads(generate_with_gemini(prompt))
    insert_into_db(category, questions)

conn.commit()
cursor.close()
conn.close()
print(f"[{datetime.datetime.now()}] Questions inserted.")