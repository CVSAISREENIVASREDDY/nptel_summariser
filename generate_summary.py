import argparse
import json
import os
import time
from google.api_core.exceptions import GoogleAPIError
import output_utils
from gemini import (
    generate_ai_response,
    generate_assignment_explanation,
    generate_extra_questions,
    is_api_key_valid,
)
from assignment_utils import get_assignment_text


def generate_week_content(
    api_key,
    week_number,
    videos,
    transcript_prompt,
    summary_prompt,
    assignment_prompt,
    should_generate_extra_questions,
):
    """Generates the HTML content for a single week."""
    output = ""
    output += f'<div class="week" id="week_{week_number}">'
    output += f'<h1 class="week-title">Week {week_number}</h1>'

    try:
        # Transcript Explanations
        output += "<h2>Transcript Explanations</h2>"
        for video in videos:
            heading = video["title"]
            print(f"  - Explaining transcript for: {heading}")
            response = generate_ai_response(
                api_key, transcript_prompt, video["transcript"]
            )
            output += f'<div class="chapter" id="{heading}">'
            output += f'<h3 class="heading">{heading}</h3>'
            output += response
            output += "</div>"

        # Weekly Summary
        output += "<h2>Weekly Summary</h2>"
        print("  - Generating weekly summary...")
        week_transcripts = "\\n\\n".join([video["transcript"] for video in videos])
        summary_response = generate_ai_response(
            api_key, summary_prompt, week_transcripts
        )
        output += summary_response

        # Assignment Explanation
        output += "<h2>Assignment Explanation</h2>"
        print("  - Explaining assignment...")
        assignment_text = get_assignment_text(week_number)
        assignment_response = generate_assignment_explanation(api_key, assignment_text)
        output += assignment_response

        # Additional Assignment Questions
        if should_generate_extra_questions:
            output += "<h2>Additional Assignment Questions</h2>"
            print("  - Generating new questions...")
            extra_questions_response = generate_extra_questions(
                api_key, summary_response, assignment_text
            )
            output += extra_questions_response

    except GoogleAPIError as e:
        print(f"    ERROR: A Google API error occurred: {e}")
        print("    Skipping this week and moving to the next one.")
        return None  # Return None to indicate failure
    except Exception as e:
        print(f"    ERROR: An unexpected error occurred: {e}")
        print("    Skipping this week and moving to the next one.")
        return None

    output += "</div>"
    return output


def combine_weekly_outputs(num_weeks, output_dir="weekly_outputs"):
    """Combines the weekly HTML files into a single summary file."""
    print("\\nCombining weekly files into final summary...")
    final_output = output_utils.HTML_HEAD
    final_output += "<h1>Table of Contents</h1>"
    for i in range(1, num_weeks + 1):
        final_output += f'<a href="#week_{i}">Week {i}</a><br>'

    for i in range(1, num_weeks + 1):
        week_file_path = os.path.join(output_dir, f"week_{i}.html")
        if os.path.exists(week_file_path):
            with open(week_file_path, "r", encoding="utf-8") as f:
                final_output += f.read()
            print(f"  - Appended week_{i}.html")

    final_output += output_utils.HTML_FOOT

    with open("playlist_summary.html", "w", encoding="utf-8") as f:
        f.write(final_output)
    print("Final summary saved to playlist_summary.html")


def main():
    parser = argparse.ArgumentParser(
        description="Generate a detailed summary from video transcripts."
    )
    parser.add_argument(
        "--transcript_file",
        default="transcripts.json",
        help="Path to the transcripts JSON file.",
    )
    parser.add_argument(
        "--transcript_prompt",
        default="Your task is to provide a detailed and clear explanation of the key concepts, theories, and formulas presented in the following transcript. Don't just summarize the content. Use the formulas from the transcript and render them cleanly using MathJax for all mathematical notation.",
        help="Prompt for explaining each video transcript in detail.",
    )
    parser.add_argument(
        "--summary_prompt",
        default="Summarize the main topics and key takeaways covered in the transcripts for this week.",
        help="Prompt for generating the weekly summary.",
    )
    parser.add_argument(
        "--assignment_prompt",
        default="Explain the questions and answers in the assignment, providing clear explanations for each concept.",
        help="Prompt for explaining the weekly assignment.",
    )
    parser.add_argument(
        "--generate_extra_questions",
        action="store_true",
        help="If set, generate new assignment questions based on the week's content.",
    )
    args = parser.parse_args()

    from dotenv import load_dotenv

    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key or not is_api_key_valid(api_key):
        print("Error: Please set a valid Gemini API key in the .env file.")
        return

    try:
        with open(args.transcript_file, "r", encoding="utf-8") as f:
            videos_by_week = json.load(f)
    except FileNotFoundError:
        print(
            f"Error: '{args.transcript_file}' not found. Please run your transcript fetching script first."
        )
        return

    output_dir = "weekly_outputs"
    os.makedirs(output_dir, exist_ok=True)
    print(f"Weekly output files will be saved in the '{output_dir}' directory.")

    num_weeks = len(videos_by_week)
    for i, (week_key, videos) in enumerate(videos_by_week.items()):
        week_number = week_key.split("_")[-1]
        week_file_path = os.path.join(output_dir, f"week_{week_number}.html")

        print(f"\\n--- Processing Week {week_number}/{num_weeks} ---")

        if os.path.exists(week_file_path):
            print(f"Output for Week {week_number} already exists. Skipping.")
            continue

        week_html = generate_week_content(
            api_key,
            week_number,
            videos,
            args.transcript_prompt,
            args.summary_prompt,
            args.assignment_prompt,
            args.generate_extra_questions,
        )

        if week_html:
            with open(week_file_path, "w", encoding="utf-8") as f:
                f.write(week_html)
            print(f"--- Successfully generated and saved Week {week_number} ---")
        else:
            print(f"--- Failed to generate content for Week {week_number} ---")

    combine_weekly_outputs(num_weeks, output_dir)


if __name__ == "__main__":
    main()