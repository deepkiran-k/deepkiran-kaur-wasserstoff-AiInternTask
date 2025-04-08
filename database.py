import mysql.connector
from mysql.connector import Error
import traceback
import sys
from typing import Optional

def create_db_connection(dbhost, dbuser, dbname):
    try:
        conn = mysql.connector.connect(
            host= dbhost,
            user= dbuser,
            database= dbname
        )
        return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def fetch_email_fr_db(conn):
    '''conn = create_db_connection(dbhost, dbuser, dbname)
    if conn is None:
        return []
    print('connected to db')'''
    cursor =None
    try:
        cursor = conn.cursor(buffered=True)
        query = 'SELECT id, sender, recipient, subject, body, timestamp, attachment_count FROM emails LIMIT 1'
        print('exe query [' + query + ']')
        cursor.execute(query)
        print('row count ' + str(cursor.rowcount))
        emails = []
        if cursor.rowcount > 0:
            results = cursor.fetchall()
            for result in results:
                email = {}
                email['id'] = result[0]
                email['sender'] = result[1]
                email['recipient'] = result[2]
                email['subject'] = result[3]
                email['body']= result[4]
                email['timestamp'] = result[5]
                email['attachment_count']= result[6]
                emails.append(email)

        cursor.close()
        print(f"Successfully fetch {len(emails)} emails")

        return emails

    except Exception as e:
        print(f"Error fetch emails: {e}")
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback,
                                  limit=2, file=sys.stdout)
        conn.rollback()
        return []
    finally:
        '''if conn.is_connected():
            conn.close()'''


def store_emails(emails, conn):
    '''conn = create_db_connection(dbhost, dbuser, dbname)
    if conn is None:
        return []'''

    email_ids = []  # Store the generated IDs
    try:
        cursor = conn.cursor()

        for email in emails:
            # Insert email and get its ID
            cursor.execute('''
            INSERT INTO emails (
                msg_id, sender, recipient, subject, body, timestamp, attachment_count
            ) VALUES (%s,%s, %s, %s, %s, %s, %s)
            ''', (
                email['msg_id'],
                email['sender'],
                email['recipient'],
                email['subject'],
                email['body'],
                email['timestamp'],
                email['attachment_count']
            ))
            email_id = cursor.lastrowid
            email_ids.append(email_id)  # Store the ID

            # Store attachments if they exist
            if email['attachments']:
                for attachment in email['attachments']:
                    file_path = f"/attachments/{email_id}/{attachment['file_name']}"
                    cursor.execute('''
                    INSERT INTO email_attachments (
                        email_id, file_name, file_path, file_type, file_size
                    ) VALUES (%s, %s, %s, %s, %s)
                    ''', (
                        email_id,
                        attachment['file_name'],
                        file_path,
                        attachment['file_type'],
                        attachment['file_size']
                    ))

        conn.commit()
        print(f"Successfully stored {len(emails)} emails with attachments")
        return email_ids  # Return the list of IDs

    except Error as e:
        print(f"Database error: {e}")
        conn.rollback()
        return []
    finally:
        #if conn.is_connected():
        cursor.close()
           # conn.close()


def store_llm_results(conn, email_id: int, summary: str, intent: str, reply: Optional[str] = None) -> bool:

    try:
        cursor = conn.cursor()


        cursor.execute('''
            INSERT INTO llm_results (
                    email_id, summary, intent, generated_reply, model_used
                ) VALUES (%s, %s, %s, %s, %s)
            ''', (
        email_id,
        summary,
        intent,
        reply,
        "gpt-3.5-turbo"
        ))

        conn.commit()
        print(f"LLM results stored for emails.")
        cursor.close()

    except Exception as e:
        conn.rollback()
        print(f"Error storing LLM results: {e}")
