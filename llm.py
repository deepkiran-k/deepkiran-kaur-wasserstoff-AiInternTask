from openai import OpenAI
from typing import Optional
import json


class LLMEmailAssistant:
    def __init__(self, openai_api_key):
        self.rate_limit_delay = 1.0# seconds
        self.client = OpenAI(api_key = openai_api_key)

    def summarize_email(self, email_body: str, ) -> str:
        """Generate a summary of an email, optionally with thread context."""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",  # or "gpt-3.5-turbo" if preferred
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": f"Summarize the following email:\n{email_body}"}
                ]
            )

            # ✅ Access the response correctly using dot notation
            summary = response.choices[0].message.content
            return summary

        except Exception as e:
            print(f"OpenAI API call failed: {e}")
            return "Error summarizing email."


    def generate_reply(self, email_body: str, thread_id: Optional[int] = None, tone: str = "professional") -> str:
        """Draft a reply with optional thread context."""
        prompt = f"""
        Draft a concise email reply. Tone: {tone}.
        Email to reply to: {email_body}
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",  # or "gpt-3.5-turbo" if preferred
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content":  prompt }
                    ]
            )

            reply  = response.choices[0].message.content
            return reply

        except Exception as e:
            print(f"OpenAI API call failed: {e}")
            return "Error generating reply."

    def detect_intent (self, email_body: str, ) -> str:
        """Generate a summary of an email, optionally with thread context."""
        try:
            prompt = (
                "Classify the intent of an email into one of the following detailed categories:\n"
                "- scheduling: Email proposes or discusses a meeting or event.\n"
                "- information_request: Email asks a question or requests information.\n"
                "- task_request: Email asks the recipient to complete a task or take an action.\n"
                "- follow_up: Email follows up on a previous conversation or request.\n"
                "- meeting_confirmation: Email confirms or reminds about an upcoming meeting.\n"
                "- status_update: Email provides a status update or notification.\n"
                "- announcement: Email shares a newsletter or announcement.\n"
                "- urgent: Email is urgent or highlights a critical issue.\n"
                "- invoice: Email involves billing, invoices, or payment details.\n"
                "- greeting: Email is a thank-you, greeting, or goodwill message.\n"
                "- other: Email does not fit into the above categories.\n\n"
                "Only return the **category name**, without explanation.\n\n"
                f"Email:\n\"\"\"{email_body}\"\"\""
            )

            response = self.client.chat.completions.create(
                model="gpt-4",  # or "gpt-3.5-turbo" if preferred
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ]
            )

            # ✅ Access the response correctly using dot notation
            summary = response.choices[0].message.content
            return summary

        except Exception as e:
            print(f"OpenAI API call failed: {e}")
            return "Error summarizing email."

    def extract_event_details(self, email_body: str, tone: str = "professional") -> str:
        """Draft a reply with optional thread context."""
        prompt = f"""
        You are an intelligent assistant. Extract calendar event details from the following email.

        Return ONLY in this JSON format:
        {{
          "summary": "<title of the meeting>",
          "description": "<brief description or agenda of the meeting>",
          "start_time": "<ISO 8601 format start time: YYYY-MM-DDTHH:MM:SS>",
          "end_time": "<ISO 8601 format end time: YYYY-MM-DDTHH:MM:SS>",
          "timezone": "<timezone like 'Asia/Kolkata'>",
          "attendees": ["<email1>", "<email2>"]
        }}

        If no meeting is being scheduled, return:
        {{
          "summary": null,
          "description": null,
          "start_time": null,
          "end_time": null,
          "timezone": "UTC",
          "attendees": []
        }}

        Email:
        \"\"\"{email_body}\"\"\"
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # or "gpt-3.5-turbo" if preferred
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ]
            )

            reply = response.choices[0].message.content
            return reply

        except Exception as e:
            print(f"OpenAI API call failed: {e}")
            return "Error generating reply."