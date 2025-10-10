"""
BDM Copilot Engine Package

Core functionality for PDF processing, vector search, and knowledge management.
"""

from .pdf_processor import PDFProcessor, DocumentSearch
from .knowledge_base import KnowledgeBase

try:
    from .vector_db import VectorDatabase
    VECTOR_SEARCH_AVAILABLE = True
except ImportError:
    VECTOR_SEARCH_AVAILABLE = False
    VectorDatabase = None

__all__ = [
    'PDFProcessor',
    'DocumentSearch', 
    'KnowledgeBase',
    'VectorDatabase',
    'VECTOR_SEARCH_AVAILABLE'
]