# Mein Deutsch Reader

A small personal reader for learning German (A1) through short stories.
Click any word to see its English meaning and hear it pronounced.

- Audio uses the browser's built-in German voice (no audio files).
- To add a story, paste a new object into the `STORIES` list in `index.html`.

## Audio
Clips in `audio/` are made automatically on GitHub by `.github/workflows/audio.yml`,
using Microsoft's natural German voice (edge-tts, voice set in `scripts/make_audio.py`).
After you add a story to `index.html` and push, the new clips appear within a few minutes.
