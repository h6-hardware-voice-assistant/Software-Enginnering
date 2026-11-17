# Team H6 — Final Demonstration Video

The approved output filename for the combined Sprint 1 and Sprint 2 presentation recording is:

`docs/demo/H6_Final_Project_Demonstration.mp4`

## Upload status

**Verify the uploaded asset:** [Open the final presentation MP4](./H6_Final_Project_Demonstration.mp4). The link works only once the actual MP4 has been committed to this directory. The recording is approximately 31 MB and must be uploaded from a computer using Git (instructions below); creating this Markdown file alone does not upload the video.

## Upload from the computer containing the MP4

From a working clone of `h6-hardware-voice-assistant/Software-Enginnering`:

```powershell
git pull --ff-only
New-Item -ItemType Directory -Force -Path docs/demo | Out-Null
Copy-Item -LiteralPath "C:\path\to\H6_Final_Project_Demonstration.mp4" -Destination "docs/demo/H6_Final_Project_Demonstration.mp4"
git add docs/demo/H6_Final_Project_Demonstration.mp4
git commit -m "docs(demo): add Team H6 combined final presentation recording"
git push origin main
```

Check that the video appears in the repository after the push, then open it using [final presentation demo](./H6_Final_Project_Demonstration.mp4).

## Evidence scope

The project demonstrates real voice capture using a phone microphone and Raspberry Pi, command recognition, validation, and simulated multimedia state changes using `InMemoryPlayer`. This is **not evidence of audible playback** through an actual hardware audio device.

This final combined video supplements the separate sprint video deliverables requested by the course checklist: a 1-minute Sprint 1 outcome and a 2-minute Sprint 2 outcome. Those should be uploaded separately if they have not yet been submitted.
