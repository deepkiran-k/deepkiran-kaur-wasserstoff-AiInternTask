from openai import OpenAI
from typing import Optional



class LLMEmailAssistant:
    def __init__(self, openai_api_key):
        self.rate_limit_delay = 1.0# seconds
        self.client = OpenAI(api_key = openai_api_key)

    def summarize_email(self, email_body: str, ) -> str:
        """Generate a summary of an email, optionally with thread context."""
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # or "gpt-3.5-turbo" if preferred
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



    def detect_intent(self, email_body: str) -> str:
        """Classify email intent."""
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # or "gpt-4" if preferred
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": f"Classify the intent of this email. Respond ONLY with one of these:" +
                                    "- INQUIRY (question needing response)" +
                                    "- REQUEST (action required)" +
                                    "- INFORMATIONAL (no response needed)" +
                                     "- OTHER Email: {email_body}"}
                ]
            )
            intent = response.choices[0].message.content
            return intent
        except Exception as e:
            print(f"OpenAI API call failed: {e}")
            return "Error detecting intent of email."


    def generate_reply(self, email_body: str, thread_id: Optional[int] = None, tone: str = "professional") -> str:
        """Draft a reply with optional thread context."""
        prompt = f"""
        Draft a concise email reply. Tone: {tone}.
        Email to reply to: {email_body}
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # or "gpt-3.5-turbo" if preferred
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