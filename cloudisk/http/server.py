from pathlib import Path

import uvicorn

import cloudisk
from cloudisk.globals import context


def run(host: str = "0.0.0.0", port: int = 8000) -> None:
    """
    Run server with the given parameters.

    Parameters
    ----------
    host : str, optional
        Host address to run server in. By default, 0.0.0.0.
    port : int
        Port to run server in. By default, 8000.
    """
    context.root.update_space()

    uvicorn.run(
        app="cloudisk.http.config:app",
        host=host,
        port=port,
        log_level="info",
        reload=True,
        reload_dirs=[Path(cloudisk.__file__).parent],
        reload_includes=["*.py"],
    )
