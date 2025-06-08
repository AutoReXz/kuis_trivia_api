# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-06-08

### Added
- 🎉 Initial release of Kuis Trivia API
- FastAPI-based REST API for Indonesian trivia questions
- 4 categories: Geography (geografi), Science (sains), History (sejarah), General (umum)
- JSON file storage for questions data
- Swagger/OpenAPI documentation at `/docs`
- CORS support for web and mobile applications
- Docker containerization
- Google Cloud Run deployment
- Health check endpoint
- Comprehensive README with usage examples

### Features
- **GET /**: API information and status
- **GET /health**: Health check endpoint
- **GET /kategori**: Get available categories
- **GET /soal**: Get quiz questions with optional filtering
  - Query parameters: `kategori`, `jumlah`
  - Supports random selection from all or specific categories
- **POST /soal**: Add new questions (future feature)
- **GET /soal/{id}**: Get specific question by ID (future feature)
- **DELETE /soal/{id}**: Delete question by ID (future feature)

### Technical Details
- Built with FastAPI and Python 3.8+
- Deployed on Google Cloud Run
- Live API: https://kuis-trivia-api-263444552508.asia-southeast2.run.app
- Automatic CI/CD with Cloud Build
- Docker support for local development

### Documentation
- Complete API documentation with Swagger UI
- Flutter integration examples
- cURL examples for testing
- Python and JavaScript client examples
- Comprehensive README with setup and deployment instructions

## [Unreleased]

### Planned Features
- User authentication and authorization
- Question difficulty levels
- User statistics and leaderboards
- Admin panel for question management
- Question reporting and moderation
- Rate limiting and abuse prevention
- Database migration from JSON to PostgreSQL
- Caching layer with Redis
- Question images and multimedia support
