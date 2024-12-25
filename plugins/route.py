# (©)Codexbotz
#rymme

from aiohttp import web
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    logger.info("Root route accessed")
    return web.json_response("CodeXBotz")

@routes.get("/status", allow_head=True)
async def status_handler(request):
    logger.info("Status route accessed")
    return web.json_response({"status": "running", "version": "1.0.0"})

@routes.post("/upload")
async def upload_handler(request):
    try:
        data = await request.post()
        file = data.get('file')
        if not file:
            raise ValueError("No file provided")
        
        # Process the file (e.g., save it, perform operations, etc.)
        # For now, just log the file name
        logger.info(f"File uploaded: {file.filename}")

        return web.json_response({"message": "File uploaded successfully"})
    except Exception as e:
        logger.error(f"Error in upload route: {e}")
        return web.json_response({"error": str(e)}, status=500)

@routes.get("/info/{user_id}")
async def user_info_handler(request):
    user_id = request.match_info.get('user_id')
    logger.info(f"Info route accessed for user_id: {user_id}")
    
    # Fetch user info from the database or perform other operations
    # For demonstration, returning a dummy response
    user_info = {"user_id": user_id, "name": "John Doe", "email": "john.doe@example.com"}

    return web.json_response(user_info)

# Add CORS support if needed
# from aiohttp_cors import setup as setup_cors, ResourceOptions
# cors = setup_cors(app, defaults={
#     "*": ResourceOptions(
#         allow_credentials=True,
#         expose_headers="*",
#         allow_headers="*",
#     )
# })
# for route in list(routes):
#     cors.add(route)