# Django Yahoo Finance Scraper

This project is a Django web application that utilizes Django UI with Jinja templates. It employs various external tools and libraries to scrape data from Yahoo Finance, perform background tasks, and establish WebSocket connections for real-time data transfer to the frontend.

## Features

- Scrapes data from Yahoo Finance for stock tracking.
- Utilizes Redis as a message broker for Celery.
- Celery and Celery Beat handle periodic execution of scraping tasks.
- Django Channels establish WebSocket connections for real-time data transfer to the frontend.

## External Tools and Libraries

- **Redis:** Acts as a message broker for Celery, facilitating task queueing and communication.
- **Celery:** Executes background tasks asynchronously, handling scraping tasks triggered by Celery Beat.
- **Celery Beat:** Schedules periodic execution of scraping tasks.
- **Django Channels:** Facilitates WebSocket connections between the backend and frontend for real-time data transfer.
- **Yahoo_fin Library:** Used to scrape data from Yahoo Finance for stock tracking purposes.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/varun2602/livestocktrack.git
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Make sure Redis, celery and celery beat are installed and running on your system.

4. Run migrations:

```bash
python manage.py migrate
```

5. Start the Django development server:

```bash
python manage.py runserver
```

6. Access the application at `http://localhost:8000`.

## Usage

1. Navigate to the homepage and explore available stock tracking features.
2. Real-time data updates will be displayed through WebSocket connections established via Django Channels.
3. Background scraping tasks are handled by Celery and Celery Beat, ensuring periodic updates of stock data.

