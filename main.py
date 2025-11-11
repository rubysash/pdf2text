#!/usr/bin/env python3
import sys
import os
import platform

import sys
import os

# Hard fail if not inside 'pdf2text' venv
#if os.path.basename(sys.prefix) != "pdf2text":
#    print("ERROR: activate your 'pdf2text' virtual environment first.")
#    sys.exit(1)

# Strict import order, no fallback logic
import PyPDF2
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch


def extract_text_from_pdf(pdf_path):
    """
    Extract text from PDF while preserving page structure.
    Returns a list of text content per page.
    """
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            pages_text = []
            
            print(f"Processing {len(pdf_reader.pages)} pages...")
            
            for i, page in enumerate(pdf_reader.pages):
                text = page.extract_text()
                pages_text.append(text)
                print(f"  Page {i+1}: {len(text)} characters extracted")
            
            return pages_text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None


def create_text_only_pdf(pages_text, output_path):
    """
    Create a new PDF with only the extracted text.
    Uses simple formatting to maintain readability.
    """
    try:
        c = canvas.Canvas(output_path, pagesize=letter)
        width, height = letter
        
        # Margins and text settings
        left_margin = 0.75 * inch
        right_margin = width - 0.75 * inch
        top_margin = height - 0.75 * inch
        bottom_margin = 0.75 * inch
        
        font_size = 10
        line_height = font_size * 1.2
        
        for page_num, text in enumerate(pages_text):
            print(f"Creating page {page_num + 1}...")
            
            # Start at the top of the page
            y_position = top_margin
            
            # Split text into lines
            lines = text.split('\n')
            
            c.setFont("Helvetica", font_size)
            
            for line in lines:
                # Handle empty lines
                if not line.strip():
                    y_position -= line_height
                    if y_position < bottom_margin:
                        c.showPage()
                        y_position = top_margin
                        c.setFont("Helvetica", font_size)
                    continue
                
                # Wrap long lines to fit within margins
                max_width = right_margin - left_margin
                
                # Simple word wrapping
                words = line.split()
                current_line = ""
                
                for word in words:
                    test_line = current_line + " " + word if current_line else word
                    
                    # Check if line fits
                    if c.stringWidth(test_line, "Helvetica", font_size) <= max_width:
                        current_line = test_line
                    else:
                        # Draw current line and start new one
                        if current_line:
                            c.drawString(left_margin, y_position, current_line)
                            y_position -= line_height
                            
                            # Check if we need a new page
                            if y_position < bottom_margin:
                                c.showPage()
                                y_position = top_margin
                                c.setFont("Helvetica", font_size)
                        
                        current_line = word
                
                # Draw remaining text
                if current_line:
                    c.drawString(left_margin, y_position, current_line)
                    y_position -= line_height
                    
                    # Check if we need a new page
                    if y_position < bottom_margin:
                        c.showPage()
                        y_position = top_margin
                        c.setFont("Helvetica", font_size)
            
            # Only add new page if there are more pages to process
            if page_num < len(pages_text) - 1:
                c.showPage()
        
        c.save()
        print(f"Text-only PDF created: {output_path}")
        return True
        
    except Exception as e:
        print(f"Error creating PDF: {e}")
        return False


def get_file_size(file_path):
    """Get file size in MB."""
    size_bytes = os.path.getsize(file_path)
    return size_bytes / (1024 * 1024)


def main():
    if len(sys.argv) < 2:
        print("Usage: python pdf_text_compress.py <input_pdf> [output_pdf]")
        print("\nExample:")
        print("  python pdf_text_compress.py document.pdf")
        print("  python pdf_text_compress.py document.pdf compressed_document.pdf")
        sys.exit(1)
    
    input_pdf = sys.argv[1]
    
    if not os.path.exists(input_pdf):
        print(f"Error: File '{input_pdf}' not found.")
        sys.exit(1)
    
    # Generate output filename if not provided
    if len(sys.argv) >= 3:
        output_pdf = sys.argv[2]
    else:
        input_path = Path(input_pdf)
        output_pdf = str(input_path.parent / f"{input_path.stem}_text_only{input_path.suffix}")
    
    print(f"Input PDF: {input_pdf}")
    print(f"Original size: {get_file_size(input_pdf):.2f} MB")
    print()
    
    # Extract text
    pages_text = extract_text_from_pdf(input_pdf)
    
    if pages_text is None:
        print("Failed to extract text from PDF.")
        sys.exit(1)
    
    if not any(pages_text):
        print("Warning: No text found in PDF. The file may contain only images.")
        sys.exit(1)
    
    print()
    
    # Create text-only PDF
    if create_text_only_pdf(pages_text, output_pdf):
        print()
        print(f"Output PDF: {output_pdf}")
        print(f"New size: {get_file_size(output_pdf):.2f} MB")
        print(f"Size reduction: {(1 - get_file_size(output_pdf)/get_file_size(input_pdf)) * 100:.1f}%")
        print("\n✓ Compression complete!")
    else:
        print("Failed to create compressed PDF.")
        sys.exit(1)


if __name__ == "__main__":
    main()