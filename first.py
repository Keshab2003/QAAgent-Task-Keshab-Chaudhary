from youtube_transcript_api import YouTubeTranscriptApi

video_id = "IK62Rk47aas"  # Recruter.ai video
transcript = YouTubeTranscriptApi.get_transcript(video_id)

# Combine the transcript text
full_text = "\n".join([entry["text"] for entry in transcript])

# Save to file
with open("recruter_transcript.txt", "w", encoding="utf-8") as f:
    f.write(full_text)

print("Transcript saved to recruter_transcript.txt")
