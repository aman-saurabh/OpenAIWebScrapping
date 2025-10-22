import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from openai import OpenAI
import pandas as pd

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

def scrape_bbc_headlines():
    """Scrapes top BBC News headlines."""
    url = "https://www.bbc.com/news"
    response = requests.get(url)
    # Sends an HTTP GET request to the website. The server responds with the actual HTML content of the page. For Example :
    """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Example Website</title>
    </head>
    <body>
        <h1>Welcome to Example.com!</h1>
        <p>This is a sample paragraph.</p>
    </body>
    </html>
    """

    response_text =response.text
    # response.text is nothing but just the raw HTML code in string format. It doesn't render the page i.e it doesn't remove tags and contains tags like <html>, <head>, <body>, <p>, <h1>  etc. For example:
    """
    <class 'str'>
    <!DOCTYPE html>
    <html>
    <head>
        <title>Example Website</title>
    </head>
    <body>
        <h1>Welcome to Example.com!</h1>
        <p>This is a sample paragraph.</p>
    </body>
    </html>
    """   

    soup = BeautifulSoup(response_text, 'html.parser')
    # BeautifulSoup is a Python library that parses HTML and XML so we can easily navigate the page. 'html.parser' is Python’s built-in parser.
    # BeautifulSoup(response.text, 'html.parser') creates a parsed HTML tree that we can search i.e. we can search for the content of tags like <h1> or <p> using it.
    # Think of soup as a structured map of the entire webpage.

    headlines = []    
    for item in soup.find_all('h2', limit=10):  # get first 10 headlines
        text = item.get_text().strip()
        if text:
            headlines.append(text)
    # soup.find_all(tag, limit) finds all HTML elements with a specific tag<h2>. Here, we search for <h2> tags because BBC uses them for headlines. limit=10 stops after the first 10 matches.
    # .get_text() extracts only the visible text inside the HTML tag (removes <h2> and other nested HTML). .strip() removes extra whitespace at the start and end.

    return headlines
    # Finally returning list of BBC headlines with a max limit of 10.

def summarize_headlines_with_gpt(headlines):
    """Summarizes headlines using GPT."""

    system_prompt = "You are an AI assistant that analyses content of a website"
    user_prompt = (
        "Summarize the following BBC headlines "
        "into a short news overview:\n\n"
        + "\n".join(f"- {h}" for h in headlines)
    )
    """

    There are 3 types of messages(also knows as prompts) in OpenAI. Message contains "role" and "content". 
    1.) System Prompt : 
    -> Sets the rules or persona for the AI for the rest of the conversation.
    For example : {"role": "system", "content": "You are a helpful assistant that explains concepts clearly to beginners."}

    2.) User Prompt :
    -> The user’s actual input/question/request.
    For example : {"role": "user", "content": "Explain what a variable is in Python."}

    3.) Assistant Prompt :
    -> Include previous AI responses to maintain conversation context. It is mainly used in multi-turn chat.
    For example :
    messages = [
        {"role": "system", "content": "You are a helpful assistant that explains concepts clearly to beginners."},
        {"role": "user", "content": "What is a function in Python?"},
        {"role": "assistant", "content": "A function is a reusable block of code that performs a task."},
        {"role": "user", "content": "Can you give me an example?"}
    ]

    """


    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=150
    )
    # max_tokens=150 — limits the length of GPT’s output (about 150 words/tokens).

    summary = response.choices[0].message.content.strip()
    return summary

if __name__ == "__main__":
    print("Scraping BBC News...")
    headlines = scrape_bbc_headlines()

    print(f"\nFetched {len(headlines)} headlines:\n")
    for h in headlines:
        print("•", h)

    print("\nGenerating summary with OpenAI...\n")
    summary = summarize_headlines_with_gpt(headlines)

    print("🧾 Summary:\n")
    print(summary)

    # Optional: Save to CSV
    df = pd.DataFrame({"headline": headlines})
    df.to_csv("bbc_headlines.csv", index=False)
    print("\n✅ Headlines saved to bbc_headlines.csv")
