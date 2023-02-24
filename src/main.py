from pathlib import Path
import os
import sys


sys.path.append(str(Path(os.getcwd()).parent))


import uvicorn
from src.core.settings import settings


if __name__ == "__main__":
    uvicorn.run(
        'app:app', 
        reload=True,
        host=settings.host,
        port=settings.port
    )
