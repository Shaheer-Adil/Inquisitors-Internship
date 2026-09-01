# Gemini Setup

1. Create a local `.env` file by copying `.env.example`.
2. Put your Gemini API key only in that local `.env` file:

```text
GEMINI_API_KEY=your_key_here
```

3. Never paste the API key into source code, screenshots, public repositories, or the ZIP you share.
4. The distributed Day-3 ZIP intentionally does **not** include `.env`.
5. Keep `.env.example` as the safe template.

The application reads `.env` from the project root automatically.
