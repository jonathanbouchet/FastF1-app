# Add F1 API Endpoint

A guided workflow for adding new endpoints to the FastF1 backend API.

## Steps

1. **Create or update the Pydantic model** in `src/models/`
   - Define request/response models with proper type hints
   - Place in the appropriate file (create new if needed)

2. **Add endpoint to `src/app.py`**
   - Use appropriate HTTP method (GET, POST, etc.)
   - Include the response_model parameter
   - Add proper docstring
   - Use `fastapi.status` constants for HTTP status codes (e.g., `status.HTTP_404_NOT_FOUND`)

3. **Add tests to `tests/test_endpoints.py`**
   - Minimum: one test per endpoint
   - Cover both success and error cases
   - Verify correct status codes and response structure

4. **Update `README.md`**
   - Add endpoint to "API Endpoints" section
   - Use format: `- \`HTTP_METHOD /path\` — Description`

## Reference

See CLAUDE.md for development guidelines and project structure details.
