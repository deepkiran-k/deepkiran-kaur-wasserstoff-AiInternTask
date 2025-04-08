import json
from database import create_db_connection, fetch_email_fr_db, store_emails, store_llm_results
from gmail import authenticate_gmail, list_messages, create_service
from llm import LLMEmailAssistant


def main():
    try:
        with open("config.json", "r") as file:
            content = file.read()
            config = json.loads(content)
            print("host %s" % config['dbhost'])

        conn = create_db_connection(config['dbhost'], config['dbuser'], config['dbname'])

        #Fetch emails from Gmail
        creds = authenticate_gmail(config['google_secret_key'])

        # Build the Gmail API client
        service = create_service(creds)

        msgs = list_messages(service)
        #save msgs in db
        store_emails(msgs, conn)
        #print(msgs)

        llm = LLMEmailAssistant(config['openai_api_key'])
        emails = fetch_email_fr_db(conn)
       
        for email in emails:
            emailSummary =  llm.summarize_email(email['body'])
            print('Email summary [' + emailSummary + ']')

            email_intent = llm.detect_intent(email['body'])
            print("Email intent [ " + email_intent + ']')

            email_reply = llm.generate_reply(email['body'])
            print("Generated reply [ " + email_reply + ']')

            store_llm_results(conn, email['id'], emailSummary, email_intent, email_reply )

    except Exception as e:
        print(f'An error occurred: {e}')

if __name__ == '__main__':
    main()
