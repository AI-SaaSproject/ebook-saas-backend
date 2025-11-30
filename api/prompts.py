# api/prompts.py

def chapter_prompt(title: str, author: str, section_name: str, tone: str = "expert") -> str:
    """
    Returns a premium, high-quality ebook chapter prompt.
    Clean, consistent, professional output for your SaaS.
    """

    return (
        f"You are an expert author writing a premium ebook.\n\n"
        f"Book Title: {title}\n"
        f"Author: {author}\n"
        f"Chapter: {section_name}\n"
        f"Tone: {tone}\n\n"

        f"Write a full, polished, highly engaging chapter.\n"
        f"Include the following structure:\n"
        f"1. Overview\n"
        f"2. Deep Insights\n"
        f"3. Actionable Steps\n"
        f"4. Frameworks or Methods\n"
        f"5. Example Scenarios\n"
        f"6. A 'Pro Tip' box\n"
        f"7. Final Key Takeaways\n\n"

        f"Write in a premium ebook tone — clean, professional, and easy to read.\n"
        f"Minimum 500 words.\n"
    )
