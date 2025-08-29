# core/generator.py

from pptx import Presentation
from pptx.enum.shapes import PP_PLACEHOLDER

def create_ppt_from_template(slide_data, output_path, template_path=None):
    """
    Creates a NEW, separate PPT file from slide_data, applying styles from a template.
    This version opens the template, deletes its slides, then adds new ones.
    """
    
    # If a template is provided, open it. Otherwise, create a blank presentation.
    if template_path:
        prs = Presentation(template_path)
        
        # --- THIS IS THE CORRECTED LOGIC ---
        # Get the list-like object of slide IDs
        slide_id_list = prs.slides._sldIdLst
        
        # Create a list of all slide elements to remove, as we can't iterate and remove from the same list
        slides_to_remove = list(slide_id_list)
        
        # Iterate through the list of slide elements and remove each one
        for slide_element in slides_to_remove:
            slide_id_list.remove(slide_element)
        # --- END OF CORRECTED LOGIC ---

    else:
        prs = Presentation()

    # Find a suitable "Title and Content" layout
    title_and_content_layout = None
    try:
        # Most templates have "Title and Content" at index 1
        title_and_content_layout = prs.slide_layouts[1]
    except IndexError:
        # Fallback to searching for a suitable layout if index 1 doesn't exist
        for layout in prs.slide_layouts:
            has_title = any(ph.placeholder_format.type == PP_PLACEHOLDER.TITLE for ph in layout.placeholders)
            has_body = any(ph.placeholder_format.type in (PP_PLACEHOLDER.BODY, PP_PLACEHOLDER.OBJECT) for ph in layout.placeholders)
            if has_title and has_body:
                title_and_content_layout = layout
                break
    
    # If no suitable layout is found, use the first one as a last resort
    if not title_and_content_layout and len(prs.slide_layouts) > 0:
        title_and_content_layout = prs.slide_layouts[0]
    else:
        # If there are no layouts at all (e.g., truly blank presentation), use the default
        title_and_content_layout = prs.slide_layouts.get_by_name("Title and Content") or prs.slide_layouts[1]


    # --- Create slides ---
    for item in slide_data:
        slide = prs.slides.add_slide(title_and_content_layout)
        
        title_shape = slide.shapes.title
        body_shape = None

        if title_shape:
            title_shape.text = item.get("title", "No Title")

        # Find the body placeholder on the slide
        for shape in slide.placeholders:
            if shape.placeholder_format.type in (PP_PLACEHOLDER.BODY, PP_PLACEHOLDER.OBJECT, PP_PLACEHOLDER.CONTENT):
                if shape.has_text_frame:
                    body_shape = shape
                    break
        
        if body_shape:
            tf = body_shape.text_frame
            tf.clear()
            
            points = item.get("points", [])
            if points:
                p = tf.paragraphs[0]
                p.text = points[0]
                
                for point_text in points[1:]:
                    p = tf.add_paragraph()
                    p.text = point_text
                    p.level = 0 # Ensure all points are at the top level

    prs.save(output_path)
    return output_path
