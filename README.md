# Playlist Summarizer

This project is a Python application that generates detailed summaries and explanations from a YouTube playlist. It fetches video transcripts, uses the Gemini AI to generate explanations and summaries, and then creates an HTML report. It also includes a Streamlit application to view the generated content.

## Features

-   Fetches video transcripts from a YouTube playlist.
-   Generates detailed explanations of key concepts, theories, and formulas from the transcripts.
-   Creates weekly summaries of the main topics and key takeaways.
-   Explains the questions and answers in the weekly assignments.
-   Optionally generates additional assignment questions.
-   Combines all the generated content into a single HTML file.
-   Provides a Streamlit web interface to navigate and view the weekly content.

## How to Use

1.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

2.  **Set up your environment:**

    Create a `.env` file in the root directory and add your Gemini API key:

    ```
    GEMINI_API_KEY=your_api_key
    ```

3.  **Fetch transcripts:**

    You need to have a `transcripts.json` file in the root directory. The project does not include the script to fetch the transcripts, so you need to create it separately. The `transcripts.json` file should have the following structure:

    ```json
    {
      "week_1": [
        {
          "title": "Video Title 1",
          "transcript": "..."
        },
        {
          "title": "Video Title 2",
          "transcript": "..."
        }
      ],
      "week_2": [
        ...
      ]
    }
    ```

4.  **Generate the summary:**

    Run the `generate_summary.py` script to generate the HTML report:

    ```bash
    python generate_summary.py
    ```

    This will create a `playlist_summary.html` file and a `weekly_outputs` directory with individual HTML files for each week.

5.  **Run the Streamlit app:**

    To view the generated content in a web interface, run the Streamlit app:

    ```bash
    streamlit run app.py
    ```

## Files

-   `app.py`: The main Streamlit application file.
-   `generate_summary.py`: The main script to generate the summaries.
-   `gemini.py`: A module to interact with the Gemini AI API.
-   `assignment_utils.py`: A module to read the assignment PDF files.
-   `output_utils.py`: A module with HTML templates.
-   `requirements.txt`: A list of Python dependencies.
-   `transcripts.json`: A file containing the video transcripts (you need to create this file).
-   `playlist_summary.html`: The final HTML report.
-   `weekly_outputs/`: A directory with individual HTML files for each week.
-   `assignments/`: A directory with the weekly assignment PDF files.
