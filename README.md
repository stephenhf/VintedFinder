
# VintedFinder

A Python script that scrapes Vinted for listings matching specified keywords and a maximum price, then automatically emails the results.

## Features

- Scrapes Vinted for listings based on specified keywords
- Filters listings by a maximum price
- Automatically sends an email with the new listings
- Runs in headless mode for efficiency
- Detailed logging and error handling

## Requirements

- Python 3.6 or higher
- Google Chrome browser
- ChromeDriver
- `selenium` library
- `webdriver_manager` library
- `smtplib` library (standard library)
- `email` library (standard library)
- `python-dotenv` library

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/StephenHF/VintedFinder.git
    cd VintedFinder
    ```

2. Create and activate a virtual environment:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scriptsctivate`
    ```

3. Install the required Python packages:

    ```sh
    pip install -r requirements.txt
    ```

4. Set up your credentials and search parameters:

    ### Using Environment Variables

    - Create a `.env` file in the project directory with the following content:

      ```env
      EMAIL_ADDRESS=your_email
      APP_PASSWORD=your_app_password
      RECIPIENT_EMAIL=recipient_email
      MAX_PRICE=1
      KEYWORDS=keyword1,keyword2,keyword3
      ```

    - `MAX_PRICE` sets the maximum price for the listings.
    - `KEYWORDS` is a comma-separated list of keywords to search for.

## Usage

Run the script:

    ```sh
    python vinted_finder.py
    ```

The script will scrape Vinted for listings matching the specified keywords and send an email with the details of the new listings.

## Contributing

Feel free to submit issues or pull requests if you have any improvements or suggestions.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
