# api/main.py

from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
import tempfile
from typing import Optional
import sys
import json

# Add the backend directory to Python path to import core modules
# Change the sys.path line to:
backend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend')
sys.path.append(backend_path)

try:
    from core.llm_handler import generate_slide_content
    from core.generator import create_ppt_from_template
except ImportError as e:
    print(f"Import error: {e}")
    print(f"Backend path: {backend_path}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Python path: {sys.path}")
    # Don't raise here, let it fail at runtime so we can see the error
    
app = FastAPI(title="Text to PowerPoint Generator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate-ppt")
async def generate_ppt(
    text_content: str = Form(...),
    guidance: str = Form(""),
    llm_provider: str = Form(...),
    api_key: str = Form(...),
    filename: str = Form(...),
    template_file: Optional[UploadFile] = File(None)
):
    temp_dir = tempfile.mkdtemp()
    
    try:
        template_path = None
        if template_file:
            template_path = os.path.join(temp_dir, template_file.filename)
            with open(template_path, "wb") as buffer:
                shutil.copyfileobj(template_file.file, buffer)
        
        # 1. Generate structured slide content from LLM
        slide_data = generate_slide_content(
            text_content=text_content,
            guidance=guidance,
            llm_provider=llm_provider,
            api_key=api_key
        )
        
        if not slide_data:
            raise ValueError("LLM failed to generate slide content.")

        # 2. Create PPT with template styling
        safe_filename = f"{filename.replace(' ', '_')}.pptx"
        output_path = os.path.join(temp_dir, safe_filename)
        
        create_ppt_from_template(
            slide_data=slide_data,
            output_path=output_path,
            template_path=template_path
        )
        
        # 3. Return the file response
        return FileResponse(
            path=output_path,
            media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            filename=safe_filename
        )
        
    except Exception as e:
        # Clean up on error
        shutil.rmtree(temp_dir, ignore_errors=True)
        print("=== Exception in /generate-ppt ===")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/")
def read_root():
    return {"message": "Welcome to the PowerPoint Generator API! This endpoint is working on Vercel."}

@app.get("/health")
def health_check():
    return {"status": "healthy", "platform": "vercel"}

# Export the app for Vercel - this is what Vercel will use
app = app