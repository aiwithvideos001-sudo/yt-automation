name: Daily YouTube Upload

on:
  schedule:
    - cron: '30 3 * * *'
    - cron: '30 7 * * *'
    - cron: '30 12 * * *'
  workflow_dispatch:

jobs:
  upload:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt
      - run: python main.py
        env:
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
          PIXABAY_API_KEY: ${{ secrets.PIXABAY_API_KEY }}
          YOUTUBE_CREDENTIALS: ${{ secrets.YOUTUBE_CREDENTIALS }}
