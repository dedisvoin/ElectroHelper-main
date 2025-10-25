import dotenv
import os

dotenv.load_dotenv()


PROXY = {
    'http': f'http://{os.getenv("PROXY_LOGIN")}@{os.getenv("PROXY_HOST")}:{os.getenv("PROXY_PORT_HTTP")}',
    'https': f'http://{os.getenv("PROXY_LOGIN")}@{os.getenv("PROXY_HOST")}:{os.getenv("PROXY_PORT_HTTPS")}',
}
API_KEY = os.getenv("GEMINI_API_KEY")
