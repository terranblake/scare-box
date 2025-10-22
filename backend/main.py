"""Main FastAPI application entry point."""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from backend.controller import ScareBoxController
from backend.websocket import manager
from backend.api import router, set_controller
from backend.config import config

# Create FastAPI app
app = FastAPI(
    title="Scare Box API",
    description="Halloween trick-or-treat experience controller",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.server.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create controller
controller = ScareBoxController()

# Set controller reference for API routes
set_controller(controller)

# Include API routes
app.include_router(router)


@app.on_event("startup")
async def startup_event():
    """Initialize system on startup."""
    print("=" * 60)
    print("SCARE BOX - Starting up...")
    print("=" * 60)

    await controller.initialize()

    print("\n🎃 Scare Box ready!")
    print(f"   API: http://{config.server.host}:{config.server.port}/api")
    print(f"   WebSocket: ws://{config.server.host}:{config.server.port}/ws")
    print(f"   Docs: http://{config.server.host}:{config.server.port}/docs\n")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    print("\nShutting down Scare Box...")
    await controller.stop()
    print("Goodbye! 👻")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "Scare Box API",
        "version": "1.0.0",
        "status": "running" if controller.is_running else "stopped",
        "docs": "/docs",
    }


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time communication."""
    await manager.connect(websocket)

    try:
        # Send initial status
        await websocket.send_json({
            "type": "connected",
            "data": {
                "message": "Connected to Scare Box",
                "state": controller.state_machine.get_state().value,
                "mode": controller.state_machine.get_mode().value,
            },
        })

        # Keep connection alive
        while True:
            # Wait for messages from client (optional)
            data = await websocket.receive_text()

            # Echo back (or handle commands)
            await websocket.send_json({
                "type": "echo",
                "data": data,
            })

    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=config.server.host,
        port=config.server.port,
        reload=True,
    )
