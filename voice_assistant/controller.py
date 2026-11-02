"""Multimedia controller (SAD section 2.6, SRS FR-03 to FR-09).

The controller is the only module that talks to the media player. Each method
maps exactly one validated command to exactly one player operation, which is
what keeps NFR-03 (a valid command never triggers a different operation)
testable.

Playback, navigation and volume operations use the same backend interface.
"""

from __future__ import annotations

from voice_assistant.errors import PlayerOperationError
from voice_assistant.player import MediaPlayerBackend, PAUSED, PLAYING


class MultimediaController:
    """Maps each validated command to exactly one player operation."""

    def __init__(self, player: MediaPlayerBackend) -> None:
        self._player = player

    @property
    def player(self) -> MediaPlayerBackend:
        return self._player

    @staticmethod
    def _raise_backend_error(operation: str, exc: Exception) -> None:
        if isinstance(exc, PlayerOperationError):
            raise exc
        raise PlayerOperationError(operation, str(exc)) from exc

    def pause_media(self) -> str:
        if self._player.state != PLAYING:
            raise PlayerOperationError(
                "pause",
                f"nothing is playing (player is {self._player.state})",
            )

        try:
            self._player.pause()
        except Exception as exc:
            self._raise_backend_error("pause", exc)

        if self._player.state != PAUSED:
            raise PlayerOperationError(
                "pause",
                f"player did not pause (state is {self._player.state})",
            )

        return "pause"

    # FR-03
    def play_media(self) -> str:
        """Start the selected media using only the backend's play operation."""
        try:
            self._player.play()
            if self._player.state != PLAYING:
                raise PlayerOperationError("play", "player did not start playback")
        except PlayerOperationError:
            raise
        except Exception as exc:
            raise PlayerOperationError("play", str(exc)) from exc

        return "play"

    # FR-05
    def resume_media(self) -> str:
        """Resume paused media."""
        if self._player.state != PAUSED:
            raise PlayerOperationError(
                "resume",
                f"nothing is paused (player is {self._player.state})",
            )

        try:
            self._player.resume()
        except PlayerOperationError:
            raise
        except Exception as exc:
            raise PlayerOperationError("resume", str(exc)) from exc

        if self._player.state != PLAYING:
            raise PlayerOperationError(
                "resume",
                f"player did not resume (state is {self._player.state})",
            )

        return "resume"

    # FR-06 / FR-07
    def increase_volume(self) -> str:
        """Increase volume within the backend's limits."""
        try:
            self._player.volume_up()
        except PlayerOperationError:
            raise
        except Exception as exc:
            raise PlayerOperationError("volume_up", str(exc)) from exc

        return "volume_up"

    def decrease_volume(self) -> str:
        """Decrease volume within the backend's limits."""
        try:
            self._player.volume_down()
        except PlayerOperationError:
            raise
        except Exception as exc:
            raise PlayerOperationError("volume_down", str(exc)) from exc

        return "volume_down"

    # FR-08
    def next_media(self) -> str:
        """Move to the next media item."""
        try:
            self._player.next_item()
        except PlayerOperationError:
            raise
        except Exception as exc:
            raise PlayerOperationError("next_item", str(exc)) from exc

        return "next"

    # FR-09
    def previous_media(self) -> str:
        """Move to the previous media item."""
        try:
            self._player.previous_item()
        except PlayerOperationError:
            raise
        except Exception as exc:
            raise PlayerOperationError("previous_item", str(exc)) from exc

        return "previous"
