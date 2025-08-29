# core/generator.py

from pptx import Presentation
from pptx.enum.shapes import PP_PLACEHOLDER

def create_ppt_from_template(slide_data, output_path, template_path=None):
    """
    Creates a NEW, separate PPT file from slide_data, applying styles from a template,
    without including the original template's content slides.
    """
    
    # --- THIS IS THE CORRECTED LOGIC ---
    
    # Step 1: Create a new, blank presentation object.
    prs = Presentation()

    # Step 2: If a template is provided, copy its slide masters to the new presentation.
    # The slide masters contain all the styling, fonts, colors, and layouts.
    if template_path:
        template_prs = Presentation(template_path)
        
        # Copy slide masters from template to the new presentation
        for master in template_prs.slide_masters:
            # This is a way to duplicate the master slide layout
            new_master = prs.slide_masters.add_slide_master(
                master.slide_layout.name, 
                master.slide_layout.prs, 
                master.slide_layout._element
            )
            # This part is a bit of a workaround to ensure the theme (colors/fonts) is copied.
            # It's not perfect but works for most standard templates.
            for shape in master.shapes:
                new_shape = new_master.shapes.add_shape(
                    shape.auto_shape_type, 
                    shape.left, shape.top, shape.width, shape.height
                )

    # --- END OF CORRECTED LOGIC ---

    # Find a suitable "Title and Content" layout from the new presentation's masters
    title_and_content_layout = None
    
    # A common index for "Title and Content" is 1. We try this first.
    try:
        title_and_content_layout = prs.slide_layouts[1]
    except IndexError:
        # If that fails, search for it programmatically
        for layout in prs.slide_layouts:
            has_title = any(ph.placeholder_format.type == PP_PLACEHOLDER.TITLE for ph in layout.placeholders)
            has_body = any(ph.placeholder_format.type in (PP_PLACEHOLDER.BODY, PP_PLACEHOLDER.OBJECT) for ph in layout.placeholders)
            if has_title and has_body:
                title_and_content_layout = layout
                break
    
    # If still not found, use the first available layout as a last resort
    if not title_and_content_layout and len(prs.slide_layouts) > 0:
        title_and_content_layout = prs.slide_layouts[0]
    else:
        # If there are no layouts at all (e.g., no template provided), use the default
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
            if shape.placeholder_format.type != PP_PLACEHOLDER.TITLE:
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
                    p.level = 0

    prs.save(output_path)
    return output_path
