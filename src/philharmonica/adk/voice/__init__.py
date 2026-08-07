"""Voice pipeline — speak with an agent over speech-to-text and text-to-speech.

A :class:`VoicePipeline` chains three stages: a :class:`STTModel`
transcribes audio, a :class:`VoiceWorkflow` (typically
:class:`SingleAgentVoiceWorkflow` driving one agent) produces the text to
say, and a :class:`TTSModel` synthesizes speech. The result is a
:class:`StreamedAudioResult` that yields
:class:`~philharmonica.adk.voice.events.VoiceStreamEvent` objects — audio
chunks and turn/session lifecycle markers — as they are produced.

Audio is raw PCM ``bytes`` throughout; ``numpy`` is an optional helper
for converting captured sample arrays. The speech models are
provider-agnostic abstractions — concrete OpenAI implementations live in
``llms/openai/`` and are imported from there.

Example::

    from philharmonica.adk import Agent
    from philharmonica.adk.voice import (
        AudioInput,
        SingleAgentVoiceWorkflow,
        VoicePipeline,
    )
    from philharmonica.adk.llms.openai import OpenAISTTModel, OpenAITTSModel

    pipeline = VoicePipeline(
        workflow=SingleAgentVoiceWorkflow(Agent(name="Assistant")),
        stt_model=OpenAISTTModel(),
        tts_model=OpenAITTSModel(),
    )
    result = await pipeline.run(AudioInput(data=pcm_bytes))
    async for event in result.stream():
        if event.type == "voice_stream_event_audio":
            play(event.data)

See ``docs/voice/`` and ``examples/voice/``.
"""

from __future__ import annotations

from philharmonica.adk.voice.audio import (
    DEFAULT_CHANNELS,
    DEFAULT_SAMPLE_RATE,
    DEFAULT_SAMPLE_WIDTH,
    AudioInput,
    StreamedAudioInput,
    pcm16_from_float32,
    pcm16_from_int16,
)
from philharmonica.adk.voice.events import (
    VoiceStreamEvent,
    VoiceStreamEventAudio,
    VoiceStreamEventError,
    VoiceStreamEventLifecycle,
)
from philharmonica.adk.voice.exceptions import STTError, STTWebsocketError, TTSError, VoiceError
from philharmonica.adk.voice.pipeline import VoicePipeline
from philharmonica.adk.voice.pipeline_config import VoicePipelineConfig
from philharmonica.adk.voice.result import StreamedAudioResult
from philharmonica.adk.voice.splitter import TextSplitter, sentence_splitter
from philharmonica.adk.voice.stt import (
    StreamedTranscriptionSession,
    STTModel,
    STTModelSettings,
    TurnDetection,
    TurnDetectionMode,
)
from philharmonica.adk.voice.tts import TTSModel, TTSModelSettings
from philharmonica.adk.voice.workflow import (
    SingleAgentVoiceWorkflow,
    VoiceWorkflow,
    VoiceWorkflowCallbacks,
)

__all__ = [
    "DEFAULT_CHANNELS",
    "DEFAULT_SAMPLE_RATE",
    "DEFAULT_SAMPLE_WIDTH",
    "AudioInput",
    "STTError",
    "STTModel",
    "STTModelSettings",
    "STTWebsocketError",
    "SingleAgentVoiceWorkflow",
    "StreamedAudioInput",
    "StreamedAudioResult",
    "StreamedTranscriptionSession",
    "TTSError",
    "TTSModel",
    "TTSModelSettings",
    "TextSplitter",
    "TurnDetection",
    "TurnDetectionMode",
    "VoiceError",
    "VoicePipeline",
    "VoicePipelineConfig",
    "VoiceStreamEvent",
    "VoiceStreamEventAudio",
    "VoiceStreamEventError",
    "VoiceStreamEventLifecycle",
    "VoiceWorkflow",
    "VoiceWorkflowCallbacks",
    "pcm16_from_float32",
    "pcm16_from_int16",
    "sentence_splitter",
]
