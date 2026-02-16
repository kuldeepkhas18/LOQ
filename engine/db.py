import os
import csv
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CSV_PATH = os.path.join(BASE_DIR, "contacts.csv")

con = sqlite3.connect(r"C:\code\LOQ\engine\LOQ.db")
cursor = con.cursor()

query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
cursor.execute(query)

#query = "INSERT INTO sys_command VALUES (null,'one note', 'C:\\Program Files\\Microsoft Office\\root\\Office16\\ONENOTE.exe')"
#cursor.execute(query)
#con.commit()

#query ="CREATE TABLE IF NOT EXISTS web_command(id integer primary key, name VARCHAR(100),url VARCHAR(1000))" 
#cursor.execute(query)

#query = "INSERT INTO web_command VALUES (null,'youtube', 'https://www.youtube.com/')"
#cursor.execute(query)
#con.commit()

#cursor.execute("UPDATE sys_command SET name = TRIM(LOWER('visual studio code'))")
#con.commit()
#print(con.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall())

cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (id integer primary key, name VARCHAR(200), mobile_no VARCHAR(255), email VARCHAR(255) NULL)''')


# Specify the column indices you want to import (0-based index)
# Example: Importing the 1st and 3rd columns

#desired_columns_indices = [0, 1]

#with open(CSV_PATH, 'r', encoding='utf-8') as csvfile:
    #csvreader = csv.reader(csvfile)
    #for row_number, row in enumerate(csvreader, start=1):
        # Skip rows that don't have enough columns
        #if len(row) < max(desired_columns_indices) + 1:
       #     print(f"Skipping row {row_number} (not enough columns): {row}")
      #      continue

        # Extract desired columns
     #   selected_data = [row[i] for i in desired_columns_indices]

        # Insert into database
    #    cursor.execute(
   #         "INSERT INTO contacts (name, mobile_no) VALUES (?, ?)",
  #          tuple(selected_data)
 #       )

# Commit and close
#con.commit()
#con.close()

#print("✅ Contacts import successfully!")



#### 4. Insert Single contacts (Optional)
#query = "INSERT INTO contacts VALUES (null,'umesh', '9981278087','null')"
#cursor.execute(query)
#con.commit()




#### 5. Search Contacts from database

#query = 'mummy'
#query = query.strip().lower()

#cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
#results = cursor.fetchall()
#if results:
 #   print("📞 Number:", results[0][0])
#else:
 #   print("❌ Contact not found")