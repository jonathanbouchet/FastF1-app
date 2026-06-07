# Add F1 API Endpoint

A guided workflow for adding new endpoints to the FastF1 backend API.

## Steps

1. **Create or update the Pydantic model** in `src/models/`
   - Define request/response models with proper type hints
   - Place in the appropriate file (create new if needed)

2. **Add endpoint to `src/app.py`**
   - Make the endpoint `async def` to enable caching
   - Use appropriate HTTP method (GET, POST, etc.)
   - Include the response_model parameter
   - Add proper docstring
   - Use `fastapi.status` constants for HTTP status codes (e.g., `status.HTTP_404_NOT_FOUND`)
   - If caching is needed: inject `CacheService` via `cache: CacheService = Depends(get_cache)`
   - For cached endpoints: check cache first, fetch on miss, store result

3. **Add tests to `tests/test_endpoints.py`**
   - Minimum: one test per endpoint
   - Cover both success and error cases
   - Verify correct status codes and response structure
   - For cached endpoints: override `get_cache` dependency with `app.dependency_overrides[get_cache] = get_mock_cache`

4. **Update `README.md`**
   - Add endpoint to "API Endpoints" section
   - Use format: `- \`HTTP_METHOD /path\` — Description`
   - If caching is added, document cache key format

## Caching Pattern

For endpoints making expensive FastF1 calls:
```python
cache_key = f"f1:{param1}:{param2}:resource"
cached = await cache.get(cache_key)
if cached:
    return SomeModel(...cached["field"])
# ... fetch from FastF1 ...
await cache.set(cache_key, {"field": value})
```

## Reference

See CLAUDE.md for development guidelines and project structure details.
