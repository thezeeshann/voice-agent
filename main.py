import asyncio
import speech_recognition as sr
from openai import AsyncOpenAI
from dotenv import load_dotenv
from openai.helpers import LocalAudioPlayer
from prompt import SYSTEM_PROMPT

load_dotenv()
client = AsyncOpenAI()


async def tts(speech: str):
    # Convert text to speech using OpenAI TTS
    async with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="coral",
        input=speech,
        instructions="Speak in a cheerful and positive tone.",
        response_format="pcm",
    ) as response:
        await LocalAudioPlayer().play(response)


def listen(recognizer: sr.Recognizer) -> str | None:
    # Blocking mic capture + STT, run off the event loop via run_in_executor
    with sr.Microphone() as source:
        print("Say something!")
        recognizer.adjust_for_ambient_noise(source)
        recognizer.pause_threshold = 2
        audio = recognizer.listen(source)

    print("Processing Audio.... (STT)")
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        print("Couldn't understand that, please try again.")
        return None
    except sr.RequestError as e:
        print(f"STT service error: {e}")
        return None


async def main():
    recognizer = sr.Recognizer()
    history = [{"role": "system", "content": SYSTEM_PROMPT}]
    loop = asyncio.get_running_loop()

    while True:
        try:
            transcript = await loop.run_in_executor(None, listen, recognizer)
            if not transcript:
                continue
            print(f"You said: {transcript}")

            history.append({"role": "user", "content": transcript})

            response = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=history,
            )
            reply = response.choices[0].message.content
            history.append({"role": "assistant", "content": reply})

            print("Processing Audio.... (TTS)")
            print("AI Response: ", reply)
            await tts(speech=reply)
        except KeyboardInterrupt:
            print("\nCtrl+C received. Stopping agent...")
            break
        except Exception as e:
            print(f"Unexpected error, continuing: {e}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nAgent stopped.")
