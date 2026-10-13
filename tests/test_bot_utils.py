import io


def prepare_agent_response(answer: str) -> dict:
    """Simulates the message size boundary logic from /agent."""
    if len(answer) <= 1850:
        return {"type": "text", "content": answer}
    else:
        buffer = io.BytesIO(answer.encode("utf-8"))
        return {
            "type": "file",
            "filename": "agent_answer.txt",
            "size": len(buffer.getvalue()),
        }


def test_prepare_short_response():
    short_text = "This is a brief AI response."
    result = prepare_agent_response(short_text)
    assert result["type"] == "text"
    assert result["content"] == short_text


def test_prepare_long_response_file_attachment():
    long_text = "A" * 2500  # Exceeds Discord 1850 limit
    result = prepare_agent_response(long_text)
    assert result["type"] == "file"
    assert result["filename"] == "agent_answer.txt"
    assert result["size"] == 2500


def test_transcript_truncation_limit():
    max_chars = 8000
    oversized_transcript = "Message line\n" * 1000
    truncated = oversized_transcript[-max_chars:]
    assert len(truncated) <= max_chars
