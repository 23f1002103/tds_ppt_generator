# core/generator.py

from pptx import Presentation
from pptx.enum.shapes import PP_PLACEHOLDER

def create_ppt_from_template(slide_data, output_path, template_path=None):
    """
    Creates a NEW, separate PPT file from slide_data, applying styles from a template.
    This version opens the template, deletes its slides, then adds new ones.
    """
    
    if template_path:
        prs = Presentation(template_path)
        
        slide_id_list = prs.slides._sldIdLst
        slides_to_remove = list(slide_id_list)
        
        for slide_element in slides_to_remove:
            slide_id_list.remove(slide_element)

    else:
        prs = Presentation()

    # Find a suitable "Title and Content" layout
    title_and_content_layout = None
    try:
        title_and_content_layout = prs.slide_layouts[1]
    except IndexError:
        for layout in prs.slide_layouts:
            has_title = any(ph.placeholder_format.type == PP_PLACEHOLDER.TITLE for ph in layout.placeholders)
            has_body = any(ph.placeholder_format.type in (PP_PLACEHOLDER.BODY, PP_PLACEHOLDER.OBJECT) for ph in layout.placeholders)
            if has_title and has_body:
                title_and_content_layout = layout
                break
    
    if not title_and_content_layout and len(prs.slide_layouts) > 0:
        title_and_content_layout = prs.slide_layouts[0]
    elif not title_and_content_layout:
        title_and_content_layout = prs.slide_layouts.get_by_name("Title and Content") or prs.slide_layouts[1]

    # --- Create slides ---
    for item in slide_data:
        slide = prs.slides.add_slide(title_and_content_layout)
        
        title_shape = slide.shapes.title
        body_shape = None

        if title_shape:
            title_shape.text = item.get("title", "No Title")

        # --- THIS IS THE CORRECTED LOGIC ---
        # Find the body placeholder on the slide, removing the invalid 'CONTENT' check
        for shape in slide.placeholders:
            if shape.placeholder_format.type in (PP_PLACEHOLDER.BODY, PP_PLACEHOLDER.OBJECT):
                if shape.has_text_frame:
                    body_shape = shape
                    break
        # --- END OF CORRECTED LOGIC ---
        
        if body_shape:
            tf = body_shape.text_frame
            tf.clear()
            
            points = item.get("points", [])
            if points:
                # Handle cases where points might not be a list
                if isinstance(points, list) and len(points) > 0:
                    p = tf.paragraphs[0]
                    p.text = str(points[0]) # Ensure text is a string
                    
                    for point_text in points[1:]:
                        p = tf.add_paragraph()
                        p.text = str(point_text) # Ensure text is a string
                        p.level = 0
                elif isinstance(points, str): # Handle if LLM returns a single string
                    p = tf.paragraphs[0]
                    p.text = points


    prs.save(output_path)
    return output_path

