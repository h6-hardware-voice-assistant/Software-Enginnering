"""Multimedia controller (SAD section 2.6, SRS FR-03 to FR-09).

The controller is the only module that talks to the media player. Each method
maps exactly one validated command to exactly one player operation, which is
what keeps NFR-03 (a valid command never triggers a different operation)
testable.

Implemented here: `play_media` (FR-03, story #9), `pause_media` (FR-04,
story #10) and `resume_media` (FR-05, story #11). The remaining operations are
owned by Sprint 2 stories and raise `NotImplementedError` until then, so
an unfinished operation can never silently perform the wrong action.
"""

from __future__ import annotations

from voice_assistant.errors import PlayerOperationError
from voice_assistant.player import MediaPlayerBackend, PAUSED, PLAYING


class MultimediaController:
    """Maps multimedia operations onto a `MediaPlayerBackend`."""

    def __init__(self, player: MediaPlayerBackend) -> None:
        self._player = player

    @property
    def player(self) -> MediaPlayerBackend:
        """The backend under control; exposed for state assertions and feedback."""
        return self._player

    # -- FR-04 ------------------------------------------------------------
    def pause_media(self) -> str:
        """Pause the currently playing item without closing the player (FR-04).

        Returns the operation name that was performed. Raises
        `PlayerOperationError` when nothing is playing or the player rejects the
        request; no other operation is attempted in that case (FR-11).
        """
        if self._player.state != PLAYING:
            raise PlayerOperationError(
                "pause", f"nothing is playing (player is {self._player.state})"
            )

        try:
            self._player.pause()
        except PlayerOperationError:
            raise
        except Exception as exc:  # backend/hardware fault, reported not retried
            raise PlayerOperationError("pause", str(exc)) from exc

        if self._player.state != PAUSED:
            raise PlayerOperationError(
                "pause", f"player did not pause (state is {self._player.state})"
            )
        return "pause"

    # -- FR-03 ------------------------------------------------------------
    def play_media(self) -> str:
        """Start the selected media using only the backend's play operation.

        A rejected request, backend fault or unchanged player state is reported
        as a player error. No alternate operation or retry is attempted.
        """
        try:
            self._player.play()
            if self._player.state != PLAYING:
                raise PlayerOperationError("play", "player did not start playback")
        except PlayerOperationError:
            raise
        except Exception as exc:
            raise PlayerOperationError("play", str(exc)) from exc
        return "play"

    def resume_media(self) -> str:
        """Resume paused media (FR-05, story #11)."""
        if self._player.state != PAUSED:
            raise PlayerOperationError(
                "resume", f"nothing is paused (player is {self._player.state})"
            )

        try:
            self._player.resume()
        except PlayerOperationError:
            raise
        except Exception as exc:
            raise PlayerOperationError("resume", str(exc)) from exc

        if self._player.state != PLAYING:
            raise PlayerOperationError(
                "resume", f"player did not resume (state is {self._player.state})"
            )

        return "resume"

    # -- Owned by Sprint 2 stories ---------------------------------------
    def increase_volume(self) -> str:
        """FR-06 — story #16."""
        raise NotImplementedError("FR-06 increase_volume is story #16")

    def decrease_volume(self) -> str:
        """FR-07 — story #16."""
        raise NotImplementedError("FR-07 decrease_volume is story #16")

    def next_media(self) -> str:
        """FR-08 — story #17."""
        try:
            self._player.next_item()
        except PlayerOperationError:
            raise
        except Exception as exc:
            raise PlayerOperationError("next_item", str(exc)) from exc
        return "next"

    def previous_media(self) -> str:
        """FR-09 — story #18."""
        try:
            self._player.previous_item()
        except PlayerOperationError:
            raise
        except Exception as exc:
            raise PlayerOperationError("previous_item", str(exc)) from exc
        return "previous"
