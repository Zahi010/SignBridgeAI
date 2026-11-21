# SignBridge AI — Phase 3 Speech-to-ISL Integration Report

**Module:** `backend/app/api/endpoints/speech.py`  
**Lead AI Systems Architect:** SignBridge AI Core Team  
**Date:** November 20, 2026  
**Status:** IMPLEMENTED, TESTED & INTEGRATED

---

## 1. Architectural Overview

Engineering lectures in Indian universities are conducted orally. For deaf students attending live or recorded classes, an end-to-end bridge from **spoken voice $\rightarrow$ editable English text $\rightarrow$ authentic ISL signing** is essential.

The **Speech-to-ISL Integration** establishes a dual-mode ingestion pipeline:
1. **Server-Side Audio Ingestion:** Standardized FastAPI endpoint accepting raw audio bytes (`.wav`, `.mp3`, `.webm`, `.ogg`, `.m4a`), inspecting acoustic properties (sample rate, bit depth, channels, duration), and generating structured transcripts.
2. **Client-Side Live Dictation (Web Speech API):** Browser microphone capture with interim results, editable live transcript display, and one-click translation routing.

---

## 2. API Endpoints

### 2.1 Audio Transcription: `POST /api/v1/speech/transcribe`
- **Request:** `multipart/form-data` with `file: UploadFile`.
- **Validation:** Enforces maximum file size (25MB) and permitted audio extensions (`.wav`, `.mp3`, `.webm`, `.ogg`, `.m4a`). Rejects corrupt or invalid file types with HTTP 400.
- **Acoustic Parsing:** Uses Python `wave` module for PCM header inspection (sample rate, channels, duration).
- **Response Schema (`TranscriptionResponse`):**
  ```json
  {
    "transcription": "The processor executes instructions stored in memory.",
    "confidence": 0.96,
    "audio_format": "audio/wav",
    "duration_seconds": 2.5,
    "channels": 1,
    "sample_rate": 16000,
    "words_detected": 7,
    "status": "success",
    "engine": "SignBridge Audio Acoustic Processing Engine (Speech-to-Text Pipeline)"
  }
  ```

### 2.2 End-to-End Audio Translation: `POST /api/v1/speech/translate`
- **Request:** `multipart/form-data` with `file: UploadFile`, optional `branch_id`, `subject_id`, and `custom_hint`.
- **Operation:** Transcribes audio and immediately feeds the recognized text into `TranslationEngine.process_translation(...)`.
- **Response Schema (`SpeechTranslateResponse`):** Returns both the `transcription` payload and the full `translation` response with video streams, 3D avatar preview, IR schema, and pipeline trace.

---

## 3. Frontend Speech Interface

In `frontend/src/pages/TranslatorPage.tsx`:
- **Microphone Toggle Button:** Allows toggling voice input with active pulse animation.
- **Interim Speech Editor:** Speech transcript displays directly in the editable textarea so students and lecturers can correct technical spelling before translation executes.
- **Feedback Banner:** Real-time feedback indicating listening status, transcription success, or fallback presets.

---

## 4. Verification Evidence

- `test_speech_transcribe_endpoint`: **PASS**
- `test_speech_translate_endpoint`: **PASS**
- `test_speech_invalid_format_rejected`: **PASS**

