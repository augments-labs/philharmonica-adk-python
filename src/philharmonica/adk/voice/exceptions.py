"""Exception hierarchy for the voice subsystem.

Every voice error derives from ``VoiceError``, which in turn
derives from the framework-wide ``PhilharmonicaError``.
Catching ``PhilharmonicaError`` therefore catches voice failures too, while
``VoiceError`` narrows to the speech pipeline.
"""

from __future__ import annotations

from philharmonica.adk.exceptions import PhilharmonicaError


class VoiceError(PhilharmonicaError):
    """Base class for every failure raised by the voice subsystem."""


class STTError(VoiceError):
    """Speech-to-text transcription failed."""


class TTSError(VoiceError):
    """Text-to-speech synthesis failed."""


class STTWebsocketError(STTError):
    """A realtime speech-to-text websocket session failed.

    Raised when the realtime transcription websocket cannot be
    established, sends a protocol error, or closes unexpectedly mid
    session.
    """
