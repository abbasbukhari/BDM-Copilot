"""
PDF Processing Engine for BDM Copilot

Handles extraction, chunking, and processing of Dell documentation PDFs.
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Any
import hashlib
import json
from datetime import datetime

from pypdf import PdfReader
import streamlit as st


class PDFProcessor:
    """Processes PDFs and extracts structured content."""
    
    def __init__(self, pdf_directory: str = "data/pdfs"):
        self.pdf_directory = Path(pdf_directory)
        self.processed_cache = {}
        
    def extract_text_from_pdf(self, pdf_path: Path) -> Dict[str, Any]:
        """Extract text content from a PDF file."""
        try:
            reader = PdfReader(pdf_path)
            
            # Extract metadata
            metadata = {
                "filename": pdf_path.name,
                "num_pages": len(reader.pages),
                "title": reader.metadata.title if reader.metadata and reader.metadata.title else pdf_path.stem,
                "author": reader.metadata.author if reader.metadata and reader.metadata.author else "Dell Technologies",
                "creation_date": reader.metadata.creation_date if reader.metadata and reader.metadata.creation_date else None,
                "file_size": pdf_path.stat().st_size,
                "processed_date": datetime.now().isoformat()
            }
            
            # Extract text from all pages
            pages_text = []
            for page_num, page in enumerate(reader.pages, 1):
                text = page.extract_text()
                if text.strip():  # Only add non-empty pages
                    pages_text.append({
                        "page_number": page_num,
                        "text": self._clean_text(text),
                        "char_count": len(text)
                    })
            
            return {
                "metadata": metadata,
                "pages": pages_text,
                "total_text": " ".join([page["text"] for page in pages_text])
            }
            
        except Exception as e:
            st.error(f"Error processing {pdf_path.name}: {str(e)}")
            return None
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize extracted text."""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove common PDF artifacts
        text = re.sub(r'[^\w\s\.\,\;\:\!\?\-\(\)\[\]\{\}\"\'\/\@\#\$\%\&\*\+\=\<\>\|\\]', '', text)
        
        # Normalize line breaks
        text = text.replace('\n', ' ').replace('\r', ' ')
        
        return text.strip()
    
    def chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[Dict[str, Any]]:
        """Split text into overlapping chunks for better context preservation."""
        if not text or len(text) < chunk_size:
            return [{"text": text, "chunk_id": 0, "start_char": 0, "end_char": len(text)}]
        
        chunks = []
        start = 0
        chunk_id = 0
        
        while start < len(text):
            end = start + chunk_size
            
            # Try to break at sentence boundaries
            if end < len(text):
                # Look for sentence endings within the last 200 characters
                sentence_end = text.rfind('.', start, end)
                if sentence_end > start + (chunk_size * 0.5):  # Don't break too early
                    end = sentence_end + 1
            
            chunk_text = text[start:end].strip()
            if chunk_text:
                chunks.append({
                    "text": chunk_text,
                    "chunk_id": chunk_id,
                    "start_char": start,
                    "end_char": end,
                    "char_count": len(chunk_text)
                })
                chunk_id += 1
            
            # Move start position with overlap
            start = end - overlap if end < len(text) else len(text)
        
        return chunks
    
    def process_all_pdfs(self) -> Dict[str, Any]:
        """Process all PDFs in the directory."""
        if not self.pdf_directory.exists():
            st.error(f"PDF directory {self.pdf_directory} does not exist")
            return {}
        
        pdf_files = list(self.pdf_directory.glob("*.pdf"))
        if not pdf_files:
            st.warning(f"No PDF files found in {self.pdf_directory}")
            return {}
        
        processed_docs = {}
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for idx, pdf_path in enumerate(pdf_files):
            status_text.text(f"Processing {pdf_path.name}...")
            
            # Extract text from PDF
            pdf_content = self.extract_text_from_pdf(pdf_path)
            if pdf_content:
                # Create chunks from the full text
                chunks = self.chunk_text(pdf_content["total_text"])
                
                # Add source information to each chunk
                for chunk in chunks:
                    chunk.update({
                        "source_file": pdf_path.name,
                        "source_title": pdf_content["metadata"]["title"],
                        "total_pages": pdf_content["metadata"]["num_pages"]
                    })
                
                processed_docs[pdf_path.name] = {
                    "metadata": pdf_content["metadata"],
                    "chunks": chunks,
                    "chunk_count": len(chunks)
                }
            
            progress_bar.progress((idx + 1) / len(pdf_files))
        
        status_text.text("✅ PDF processing complete!")
        return processed_docs
    
    def get_document_stats(self, processed_docs: Dict[str, Any]) -> Dict[str, Any]:
        """Generate statistics about processed documents."""
        if not processed_docs:
            return {}
        
        stats = {
            "total_documents": len(processed_docs),
            "total_chunks": sum(doc["chunk_count"] for doc in processed_docs.values()),
            "total_pages": sum(doc["metadata"]["num_pages"] for doc in processed_docs.values()),
            "total_size_mb": sum(doc["metadata"]["file_size"] for doc in processed_docs.values()) / (1024 * 1024),
            "documents": {}
        }
        
        for filename, doc in processed_docs.items():
            stats["documents"][filename] = {
                "title": doc["metadata"]["title"],
                "pages": doc["metadata"]["num_pages"],
                "chunks": doc["chunk_count"],
                "size_mb": doc["metadata"]["file_size"] / (1024 * 1024)
            }
        
        return stats


class DocumentSearch:
    """Simple text-based search for processed documents."""
    
    def __init__(self, processed_docs: Dict[str, Any]):
        self.processed_docs = processed_docs
        self.chunks = self._flatten_chunks()
    
    def _flatten_chunks(self) -> List[Dict[str, Any]]:
        """Flatten all chunks into a single searchable list."""
        all_chunks = []
        for doc_name, doc_data in self.processed_docs.items():
            for chunk in doc_data["chunks"]:
                chunk["document_name"] = doc_name
                all_chunks.append(chunk)
        return all_chunks
    
    def keyword_search(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Simple keyword-based search."""
        query_lower = query.lower()
        matches = []
        
        for chunk in self.chunks:
            text_lower = chunk["text"].lower()
            if query_lower in text_lower:
                # Calculate simple relevance score based on keyword frequency
                score = text_lower.count(query_lower) / len(chunk["text"].split())
                matches.append({
                    **chunk,
                    "relevance_score": score,
                    "match_preview": self._get_match_preview(chunk["text"], query, 200)
                })
        
        # Sort by relevance score
        matches.sort(key=lambda x: x["relevance_score"], reverse=True)
        return matches[:max_results]
    
    def _get_match_preview(self, text: str, query: str, preview_length: int = 200) -> str:
        """Get a preview of text around the match."""
        query_lower = query.lower()
        text_lower = text.lower()
        
        match_pos = text_lower.find(query_lower)
        if match_pos == -1:
            return text[:preview_length] + "..." if len(text) > preview_length else text
        
        start = max(0, match_pos - preview_length // 2)
        end = min(len(text), match_pos + len(query) + preview_length // 2)
        
        preview = text[start:end]
        if start > 0:
            preview = "..." + preview
        if end < len(text):
            preview = preview + "..."
        
        return preview