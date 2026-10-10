# Speech-to-Speech (S2S) Voice Agent

A chain-structured speech-to-speech agent: mic input → text → LLM reply → spoken audio.

## Architecture (chained pipeline)

``` text
Mic → STT (Google Web Speech) → LLM (gpt-4o-mini, 
with conversation history) → TTS (gpt-4o-mini-tts, streamed) → Speaker
```

- **STT**: `speech_recognition` captures mic audio with energy-based VAD, transcribes via Google Web Speech.
- **LLM**: `gpt-4o-mini` generates a reply, using full conversation history for context.
- **TTS**: `gpt-4o-mini-tts` streams PCM audio, played locally via `LocalAudioPlayer`.

## Use cases

- Customer support IVR / voice assistants
- Accessibility tools (hands-free interfaces)
- Language-practice tutors
- In-car / smart-home voice control
- Telehealth intake, outbound call agents
