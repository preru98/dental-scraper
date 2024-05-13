# Problem
Develop a scraping tool using Python FastAPI framework to automate information retrieval from the target website dentalstall.com/shop/. The tool should scrape product name, price, and image from each page of the catalogue, without opening individual product cards.

Customizable settings should allow limiting the number of pages to scrape and provide a proxy string for scraping. Scraped information must be stored in a JSON file locally, following a specific format.

Additionally, provide notifications at the end of each scraping cycle about the number of products scraped and updated in the database. This notification can be printed to the console.

For implementation, adopt an object-oriented approach with considerations for type validation, data integrity, and processing efficiency. Include a retry mechanism for handling server errors, add simple authentication using a static token, and implement scraping results caching to prevent unnecessary updates to the database.

Design decisions should prioritize abstractions and modularity to enhance maintainability and extensibility of the tool.

# High Level Design
## FastAPI
The FastAPI application serves as the core component for handling HTTP requests and responses. It utilizes the asynchronous capabilities of Python to efficiently handle concurrent requests. The app consists of routers, services, and dependencies organized into modules within the dental package. Routers define the API endpoints for scraping and other operations, while services encapsulate business logic for data retrieval, storage, and notification. Dependencies provide reusable components such as authentication, caching, and error handling.

## Redis
Redis is used as an in-memory data store to cache scraping results and optimize performance. It serves as a key-value store for storing temporary data such as product details and pricing. By leveraging Redis, the application can quickly retrieve previously scraped data without making redundant requests to the target website. This enhances the responsiveness and efficiency of the scraping tool, especially when dealing with frequent requests or large datasets.

## JSON Store
The JSON store acts as a persistent storage mechanism for storing scraped data locally. Each product's information, including its title, price, and image path, is serialized into JSON format and stored in a structured manner. While Redis provides caching for temporary storage, the JSON store ensures data persistence across application restarts or failures. This dual-storage approach combines the benefits of in-memory caching with the reliability of file-based storage, providing a robust solution for managing scraped data.

# Directory Structure
```
.
├── Dockerfile                # Dockerfile for building the Docker image
├── Pipfile                   # Pipenv file specifying Python dependencies
├── Pipfile.lock              # Pipenv lock file for dependency versions
├── README.md                 # Markdown file containing project documentation
├── app.py                    # Python file containing FastAPI application setup
├── data.json                 # JSON file containing data used by the application
├── dental                    # Package containing application modules
│   ├── __init__.py           # Initialization file for the dental package
│   ├── constants             # Package containing constants used by the application
│   │   └── urls.py           # Python file containing URL constants
│   ├── dependencies          # Package containing application dependencies
│   │   ├── __init__.py       # Initialization file for the dependencies package
│   │   ├── authenticator.py  # Python file containing authentication logic
│   │   ├── cache.py          # Python file containing caching logic
│   │   ├── notifier.py       # Python file containing notification logic
│   │   └── store.py          # Python file containing data storage logic
│   ├── main.py               # Python file containing main FastAPI application setup
│   ├── routers               # Package containing FastAPI routers
│   │   ├── dental.py         # Python file containing routes related to dental data
│   │   └── health.py         # Python file containing routes related to health checks
│   ├── services              # Package containing application services
│   │   └── dental.py         # Python file containing dental-related services
│   └── utils                 # Package containing utility functions
│       └── download_utils.py # Python file containing utility functions for downloading
├── docker-compose.yaml       # Docker Compose file for defining multi-container Docker applications
├── main.py                   # Python file containing main entry point of the application
├── products.json             # JSON file containing product data used by the application
└── scripts                   # Directory containing scripts related to the project
    └── deploy.sh             # Shell script for deploying the application
```

# Deployment

The service is deployed on an EC2 instance with docker-compose

# Running the project

To run the project locally -

```
docker-compose up -d
```

## Testing locally

Health check - 
```curl --location 'http://0.0.0.0:8000/'```

Start scraping - 
```curl --location 'http://127.0.0.1:8000/start/?page_limit=1' \--header 'token: secret-token'```

Get scraped Products -
```curl --location 'http://127.0.0.1:8000/products/'```

## Testing live version

Health check - 
```curl --location 'http://13.232.73.216:8000/'```

Start scraping - 
```curl --location 'http://13.232.73.216:8000/start/?token=secret-token' \--header 'token: secret-token'```

Get scraped Products -
```curl --location 'http://13.232.73.216:8000/products/'```