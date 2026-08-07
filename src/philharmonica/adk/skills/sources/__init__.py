"""Skill source loaders.

Provides adapters for loading skills from different sources:
filesystem directories, remote URLs, etc.
"""

from philharmonica.adk.skills.sources.base import SkillSource
from philharmonica.adk.skills.sources.directory import DirectorySkillSource
from philharmonica.adk.skills.sources.remote import RemoteSkillSource

__all__ = [
    "DirectorySkillSource",
    "RemoteSkillSource",
    "SkillSource",
]
