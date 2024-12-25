# (©)Codexbotz
# @iryme

from aiohttp import web
from aiohttp.web_middlewares import normalize_path_middleware
from aiohttp.web_middlewares import middleware
from aiohttp.web_response import json_response
from .route import routes
import logging
from aiohttp_cors import setup as setup_cors, ResourceOptions

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Middleware for error handling
@middleware
async def handle_errors(request, handler):
    try:
        response = await handler(request)
        return response
    except web.HTTPException as ex:
        logger.error(f"HTTP error: {ex}")
        return json_response({"error": str(ex)}, status=ex.status)
    except Exception as ex:
        logger.error(f"Server error: {ex}")
        return json_response({"error": "Internal server error"}, status=500)

async def web_server():
    # Create the web application
    web_app = web.Application(
        client_max_size=30000000,
        middlewares=[normalize_path_middleware(), handle_errors]
    )
    # Add routes to the web application
    web_app.add_routes(routes)

    # Setup CORS
    cors = setup_cors(web_app, defaults={
        "*": ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })
    # Configure CORS on all routes
    for route in list(web_app.router.routes()):
        cors.add(route)

    return web_app