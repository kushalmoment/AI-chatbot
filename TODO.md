# TODO List for Fixing Gemini API Error and Gunicorn Issue

## Tasks
- [x] Update gemini_service.py to use supported model "gemini-2.5-flash"
- [x] Test the API to ensure the 500 error is resolved
- [x] If issues persist, advise updating .env file to remove deprecated model (no issues found)
- [x] Replace gunicorn with waitress for Windows compatibility
- [x] Create run_server.py script to run the app with waitress

## Notes
- Error: 404 models/gemini-1.5-flash is not found
- Current model in code: Config.GENERATIVE_MODEL (defaults to gemini-2.0-flash, but .env overrides to gemini-pro)
- Solution: Hardcode "gemini-2.5-flash" in gemini_service.py
- Gunicorn issue: ModuleNotFoundError 'fcntl' on Windows
- Solution: Use Waitress instead of Gunicorn for Windows compatibility
