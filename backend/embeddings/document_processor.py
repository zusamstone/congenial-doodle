"""
Document Processing Module

Handles extraction of text from various document formats:
- PDF files
- Word documents (DOCX)
- PowerPoint presentations (PPTX)
- Plain text files
- Markdown files
- HTML (via web scraping)
"""

import logging
from pathlib import Path
from typing import Dict, Any, Optional
import mimetypes

# Import document processing libraries
try:
    import pypdf
except ImportError:
    pypdf = None

try:
    from docx import Document as DocxDocument
except ImportError:
    DocxDocument = None

try:
    from pptx import Presentation
except ImportError:
    Presentation = None

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

try:
    import markdown
except ImportError:
    markdown = None


logger = logging.getLogger(__name__)


class DocumentProcessor:
    """
    Processes various document formats and extracts text.

    Supported formats:
    - PDF (.pdf)
    - Word (.docx)
    - PowerPoint (.pptx)
    - Text (.txt)
    - Markdown (.md)
    - HTML (.html, .htm)

    Example:
        ```python
        processor = DocumentProcessor()

        text, metadata = processor.process_file("document.pdf")
        print(f"Extracted {len(text)} characters")
        ```
    """

    def __init__(self):
        """Initialize document processor."""
        self.supported_extensions = {
            ".pdf": self._process_pdf,
            ".docx": self._process_docx,
            ".pptx": self._process_pptx,
            ".txt": self._process_text,
            ".md": self._process_markdown,
            ".html": self._process_html,
            ".htm": self._process_html,
        }

        logger.info("DocumentProcessor initialized")

    def process_file(self, file_path: str) -> tuple[str, Dict[str, Any]]:
        """
        Process a file and extract text.

        Args:
            file_path: Path to the file

        Returns:
            Tuple of (extracted_text, metadata)

        Raises:
            ValueError: If file format not supported
            FileNotFoundError: If file doesn't exist
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        extension = path.suffix.lower()

        if extension not in self.supported_extensions:
            raise ValueError(
                f"Unsupported file format: {extension}. "
                f"Supported: {', '.join(self.supported_extensions.keys())}"
            )

        logger.info(f"Processing file: {path.name} ({extension})")

        # Process based on extension
        processor_func = self.supported_extensions[extension]
        text = processor_func(path)

        # Generate metadata
        metadata = self._generate_metadata(path, text)

        logger.info(f"Extracted {len(text)} characters from {path.name}")

        return text, metadata

    def _process_pdf(self, path: Path) -> str:
        """Extract text from PDF file."""
        if pypdf is None:
            raise ImportError("pypdf is required for PDF processing. Install with: pip install pypdf")

        text_parts = []

        with open(path, 'rb') as file:
            reader = pypdf.PdfReader(file)

            for page_num, page in enumerate(reader.pages, start=1):
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)

        return "\n\n".join(text_parts)

    def _process_docx(self, path: Path) -> str:
        """Extract text from Word document."""
        if DocxDocument is None:
            raise ImportError("python-docx is required for DOCX processing. Install with: pip install python-docx")

        doc = DocxDocument(path)

        # Extract paragraphs
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]

        # Extract tables
        table_texts = []
        for table in doc.tables:
            for row in table.rows:
                row_text = " | ".join(cell.text for cell in row.cells)
                if row_text.strip():
                    table_texts.append(row_text)

        # Combine
        all_text = paragraphs + table_texts
        return "\n\n".join(all_text)

    def _process_pptx(self, path: Path) -> str:
        """Extract text from PowerPoint presentation."""
        if Presentation is None:
            raise ImportError("python-pptx is required for PPTX processing. Install with: pip install python-pptx")

        prs = Presentation(path)
        text_parts = []

        for slide_num, slide in enumerate(prs.slides, start=1):
            slide_texts = []

            for shape in slide.shapes:
                if hasattr(shape, "text") and shape.text.strip():
                    slide_texts.append(shape.text)

            if slide_texts:
                text_parts.append(f"--- Slide {slide_num} ---\n" + "\n".join(slide_texts))

        return "\n\n".join(text_parts)

    def _process_text(self, path: Path) -> str:
        """Extract text from plain text file."""
        with open(path, 'r', encoding='utf-8', errors='ignore') as file:
            return file.read()

    def _process_markdown(self, path: Path) -> str:
        """Extract text from Markdown file."""
        with open(path, 'r', encoding='utf-8', errors='ignore') as file:
            md_text = file.read()

        # Optionally convert to HTML and strip tags
        if markdown:
            html = markdown.markdown(md_text)
            if BeautifulSoup:
                soup = BeautifulSoup(html, 'html.parser')
                return soup.get_text()

        # Return raw markdown if libraries not available
        return md_text

    def _process_html(self, path: Path) -> str:
        """Extract text from HTML file."""
        with open(path, 'r', encoding='utf-8', errors='ignore') as file:
            html = file.read()

        if BeautifulSoup is None:
            # Fallback: return raw HTML
            logger.warning("BeautifulSoup not available, returning raw HTML")
            return html

        soup = BeautifulSoup(html, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        # Get text
        text = soup.get_text()

        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)

        return text

    def _generate_metadata(self, path: Path, text: str) -> Dict[str, Any]:
        """Generate metadata for processed document."""
        stat = path.stat()

        metadata = {
            "filename": path.name,
            "file_path": str(path.absolute()),
            "file_size": stat.st_size,
            "file_type": path.suffix.lower(),
            "char_count": len(text),
            "word_count": len(text.split()),
            "mime_type": mimetypes.guess_type(path)[0] or "unknown",
        }

        # Add format-specific metadata
        if path.suffix.lower() == ".pdf":
            # Could add page count here
            pass

        return metadata

    def is_supported(self, file_path: str) -> bool:
        """
        Check if a file format is supported.

        Args:
            file_path: Path to the file

        Returns:
            True if supported, False otherwise
        """
        extension = Path(file_path).suffix.lower()
        return extension in self.supported_extensions

    def get_supported_formats(self) -> list[str]:
        """Get list of supported file formats."""
        return list(self.supported_extensions.keys())
