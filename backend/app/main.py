from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .routers import images, ops, auth, projects, catalog, share
from .database import create_tables


def create_app() -> FastAPI:
	app = FastAPI(title="Araba Modifiye API", version="0.1.0")

	app.add_middleware(
		CORSMiddleware,
		allow_origins=["*"],
		allow_credentials=False,
		allow_methods=["*"],
		allow_headers=["*"],
	)

	@app.get("/health")
	def health():
		return {"status": "ok"}

	# Include all routers
	app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
	app.include_router(projects.router, prefix="/api/v1/projects", tags=["projects"])
	app.include_router(images.router, prefix="/api/v1/images", tags=["images"])
	app.include_router(ops.router, prefix="/api/v1/ops", tags=["ops"])
	app.include_router(catalog.router, prefix="/api/v1/catalog", tags=["catalog"])
	app.include_router(share.router, prefix="/api/v1/share", tags=["share"])

	# Serve uploaded media files
	app.mount("/media", StaticFiles(directory="media"), name="media")

	@app.on_event("startup")
	async def startup_event():
		# Create database tables on startup
		create_tables()

	return app


app = create_app()

