from openai import AsyncOpenAI
from app.core.config import settings
from app.core.logger import logger

# Initialize conditionally based on whether we have a real key or a mock
if settings.OPENAI_API_KEY and settings.OPENAI_API_KEY != "mocked_key":
    client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
else:
    client = None

async def analyze_and_generate_response(comment: str) -> dict:
    """
    Анализирует текст с помощью OpenAI и генерирует автоответ.
    Реализует Graceful Fallback на случай недоступности AI или если используется мок-ключ.
    """
    fallback_response = {
        "sentiment": "unknown",
        "auto_reply": "Спасибо за ваше обращение! Мы получили ваше сообщение и скоро свяжемся с вами."
    }

    if not client:
        logger.info("AI is running in Mock mode (no real API key provided). Using fallback response.")
        return fallback_response

    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Analyze the sentiment of the user's comment (positive, neutral, negative) and generate a polite auto-reply for them in Russian. Return the response strictly as JSON with keys 'sentiment' and 'auto_reply'."},
                {"role": "user", "content": comment}
            ],
            response_format={ "type": "json_object" },
            timeout=10.0
        )
        
        import json
        result = json.loads(response.choices[0].message.content)
        return {
            "sentiment": result.get("sentiment", "unknown"),
            "auto_reply": result.get("auto_reply", fallback_response["auto_reply"])
        }
    except Exception as e:
        logger.error(f"AI API call failed: {str(e)}. Using fallback response.")
        return fallback_response
