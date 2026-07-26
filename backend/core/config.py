from pydantic_settings import BaseSettings
from pathlib import Path

ENV_PATH = Path(__file__).parent.parent / ".env"

class Settings(BaseSettings):
    supabase_url: str = ""
    supabase_anon_key: str = ""
    supabase_service_role_key: str = ""
    anthropic_api_key: str = ""
    gemini_api_key: str = ""
    email_sender: str = ""
    email_password: str = ""
    email_receiver: str = ""
    twilio_sid: str = ""
    twilio_token: str = ""
    twilio_whatsapp: str = ""
    whatsapp_number: str = ""
    ntfy_channel: str = "AMPLE-alerts-12345"

    class Config:
        env_file = str(ENV_PATH)
        extra = "ignore"

settings = Settings()