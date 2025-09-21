# Restaurant Finder 🍽️

An AI-powered restaurant recommendation system that helps users find the perfect dining experience based on their preferences.

## Features

- **AI-Powered Search**: Uses Google Gemini AI to understand natural language requests
- **Comprehensive Data**: Restaurant database with ratings, cuisine types, and location data
- **Smart Filtering**: Filter by cuisine, price range, rating, and distance
- **AWS Integration**: Data storage and retrieval from AWS S3
- **Modular Architecture**: Clean OOP design with separation of concerns

## Project Structure

```
restaurant-finder/
├── src/                    # Source code
│   ├── api/               # API clients (Gemini, AWS)
│   ├── models/            # Data models
│   ├── services/          # Business logic
│   └── utils/             # Utility functions
├── configs/               # Configuration files
├── data/                  # Data storage
│   ├── raw/              # Original data files
│   └── processed/        # Processed data
├── notebooks/             # Jupyter notebooks
├── tests/                 # Test files
└── scripts/               # Utility scripts
```

## Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd restaurant-finder
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure AWS credentials**
   - Create `configs/rootkey.csv` with your AWS credentials
   - Format: `Access key ID,Secret access key`

5. **Configure Gemini API**
   - Get your Gemini API key from Google AI Studio
   - Set it as an environment variable or in the code

## Usage

### Basic Usage

```python
from src.main import main
main()
```

### Programmatic Usage

```python
from src.services.restaurant_service import RestaurantService
from src.models.request import RestaurantRequest, CuisineType, PriceRange

# Initialize service
service = RestaurantService()

# Create search request
request = RestaurantRequest(
    location="Los Angeles, CA",
    cuisine=CuisineType.CHINESE,
    price_range=PriceRange.MODERATE,
    rating_min=4.0
)

# Search for restaurants
response = service.search_restaurants(request)
print(f"Found {response.total_count} restaurants")
```

## API Classes

### Core Services

- **`RestaurantService`**: Main service for restaurant operations
- **`PromptService`**: Manages AI prompts and configurations
- **`GeminiClient`**: Handles Gemini AI API interactions
- **`AWSClient`**: Manages AWS S3 operations

### Data Models

- **`Restaurant`**: Restaurant data model
- **`RestaurantRequest`**: Search request model
- **`RestaurantResponse`**: Search response model

## Configuration

### Prompts Configuration (`configs/prompts.yaml`)

```yaml
prompts:
  request_reformatter:
    version: "1.0"
    description: "Reformats user requests into structured API calls"
    system: |
      You are a helpful assistant...
    examples:
      - input: "I want Italian food near me"
        output: '{"cuisine": "Italian", "location": "current location"}'
```

## Development

### Running Tests

```bash
python -m pytest tests/
```

### Code Structure

The project follows a clean architecture pattern:

- **API Layer**: External service integrations
- **Service Layer**: Business logic and orchestration
- **Model Layer**: Data structures and validation
- **Utility Layer**: Helper functions and configuration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For questions or issues, please open an issue on GitHub.
