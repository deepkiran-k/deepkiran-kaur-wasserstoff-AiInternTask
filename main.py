import json
from database import create_db_connection, fetch_email_fr_db, store_emails, store_llm_results
from gmail import authenticate_gmail, list_messages, create_service, send_reply
from llm import LLMEmailAssistant
from slack import send_message
from mycalendar import create_calendar_event, create_calendar_service
from web_search import web_search

def main():
    try:

        with open("/Users/chalkdigital/Downloads/AIEmailAssistant/AIEA/config.json", "r") as file:
            content = file.read()
            config = json.loads(content)
            print("host %s" % config['dbhost'])

        conn = create_db_connection(config['dbhost'], config['dbuser'], config['dbname'])

        #Fetch emails from Gmail
        creds = authenticate_gmail(config['google_secret_key'])

        #Build the Gmail API client
        service = create_service(creds)
        service1 = create_calendar_service(creds)
        msgs = list_messages(service)

        #save msgs in db
        store_emails(msgs, conn)
        print(msgs)

        #Context Understanding with LLM
        llm = LLMEmailAssistant(config['openai_api_key'])
        emails = fetch_email_fr_db(conn)
        #emails = []
        for email in emails:
            emailSummary =  llm.summarize_email(email['body'])
            print('Email summary [' + emailSummary + ']')

            email_intent = llm.detect_intent(email['body'])
            print("Email intent [ " + email_intent + ']')

            # 🔍 Handle web search emails
            if email_intent.lower() == "web_search":
                print("Web search intent detected. Extracting search query...")

                search_query = llm.extract_search_query(email['body'])  # You’ll define this method
                print("Search query:", search_query)

                search_results = web_search(
                    config['google_api_key'],
                    config['google_cse_id'],
                    search_query
                )
                search_context = "\n".join(search_results)

                # Feed the search results + original email to generate a contextual reply
                email_reply = llm.generate_reply_with_web_results(email['body'], search_context)
                print("Generated reply with web search [ " + email_reply + ']')
            else:
                # Default reply
                email_reply = llm.generate_reply(email['body'])

            print("Email reply [ " + email_reply + ']')

            store_llm_results(conn, email['id'], emailSummary, email_intent, email_reply )

            #Slack integration
            send_message(config["slack_token"], config["slack_channel"], emailSummary)

            #Automated Reply Generation
            send_reply(service, email, email_reply )

            #Calendar scheduling:
            if email_intent.lower() == "scheduling":
                print("Scheduling intent detected. Extracting event details...")

                raw_event_details = llm.extract_event_details(email['body'])
                event_details = json.loads(raw_event_details) if isinstance(raw_event_details,
                                                                            str) else raw_event_details

                summary = event_details['summary']
                description = event_details['description']
                starttime = event_details['start_time']
                endtime = event_details['end_time']
                timezone = event_details['timezone']
                attendees = event_details.get('attendees', [])

                create_calendar_event(service1, summary, description, starttime, endtime, timezone, attendees)





    except Exception as e:
        print(f'An error occurred: {e}')

if __name__ == '__main__':
    main()