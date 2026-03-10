# data-retrieval
Welcome to the data retrieval section of this project! Here is where I get courses data from the UWaterloo Open API, process it to filter for the interesting courses to keep for the game, and run some data analysis to ensure the most intuitive and balanced gameplay!

## Order to run scripts
**(The order to run python scripts to generate `courses.json` in frontend $lib)**
1. Run `uwuc_scraper.py` to scrape subjects from the undergraduate calendar. (I wanted to keep this to exactly the subjects found on the calendar so I didn't want to just call the API again) Should output to `ucal_subjects.json`
2. Run `fetch-source.py` to call the UWaterloo API to get the courses. This requires a `UW_API_KEY` environment variable in a `.env` file. Should output to `first-pass.json`
3. Run `filter-playable.py` to filter and aggregate courses into each playable course. Should output to `courses-source.json`
4. Run `prep-embeddings.py` to get the embeddings for each course. Requires a `HUGGINGFACE_API_KEY` environment variable in a `.env` file (key obtained from https://huggingface.co/).
There should now be a `courses.json` file in `$lib/domain/server`!