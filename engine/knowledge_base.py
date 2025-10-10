"""
Knowledge Base Manager for BDM Copilot

Main interface for managing document processing and search.
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

import streamlit as st
from .pdf_processor import PDFProcessor, DocumentSearch
from .vector_db import VectorDatabase


class KnowledgeBase:
    """Main knowledge base manager that coordinates PDF processing and search."""
    
    def __init__(self, pdf_directory: str = "data/pdfs", cache_file: str = "data/processed/kb_cache.json"):
        self.pdf_directory = Path(pdf_directory)
        self.cache_file = Path(cache_file)
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize components
        self.pdf_processor = PDFProcessor(pdf_directory)
        self.vector_db = VectorDatabase()
        self.document_search = None
        
        # Load cached data if available
        self.processed_docs = self._load_cache()
        if self.processed_docs:
            self.document_search = DocumentSearch(self.processed_docs)
    
    def _load_cache(self) -> Dict[str, Any]:
        """Load processed documents from cache."""
        if not self.cache_file.exists():
            return {}
        
        try:
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            st.warning(f"Failed to load cache: {str(e)}")
            return {}
    
    def _save_cache(self, data: Dict[str, Any]) -> bool:
        """Save processed documents to cache."""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, default=str)
            return True
        except Exception as e:
            st.error(f"Failed to save cache: {str(e)}")
            return False
    
    def is_initialized(self) -> bool:
        """Check if knowledge base has been initialized with documents."""
        return bool(self.processed_docs)
    
    def needs_rebuild(self) -> bool:
        """Check if knowledge base needs to be rebuilt."""
        if not self.processed_docs:
            return True
        
        # Check if any PDFs are newer than the cache
        if not self.cache_file.exists():
            return True
        
        cache_time = self.cache_file.stat().st_mtime
        for pdf_file in self.pdf_directory.glob("*.pdf"):
            if pdf_file.stat().st_mtime > cache_time:
                return True
        
        return False
    
    def build_knowledge_base(self, use_embeddings: bool = True) -> bool:
        """Build the knowledge base from PDF files."""
        try:
            st.info("🔄 Building knowledge base from Dell PDFs...")
            
            # Process all PDFs
            processed_docs = self.pdf_processor.process_all_pdfs()
            if not processed_docs:
                st.error("No documents were processed successfully.")
                return False
            
            # Save to cache
            if self._save_cache(processed_docs):
                self.processed_docs = processed_docs
                self.document_search = DocumentSearch(processed_docs)
                
                # Add to vector database if embeddings are available
                if use_embeddings and self.vector_db.is_available():
                    st.info("🧠 Generating vector embeddings...")
                    self.vector_db.add_documents(processed_docs)
                
                st.success("✅ Knowledge base built successfully!")
                return True
            else:
                st.error("Failed to save processed documents.")
                return False
                
        except Exception as e:
            st.error(f"Failed to build knowledge base: {str(e)}")
            return False
    
    def search(self, query: str, search_type: str = "keyword", max_results: int = 5) -> List[Dict[str, Any]]:
        """Search the knowledge base."""
        if not self.is_initialized():
            st.warning("Knowledge base not initialized. Please build it first.")
            return []
        
        if search_type == "semantic" and self.vector_db.is_available():
            return self.vector_db.semantic_search(query, max_results)
        else:
            return self.document_search.keyword_search(query, max_results)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get comprehensive statistics about the knowledge base."""
        stats = {
            "initialized": self.is_initialized(),
            "needs_rebuild": self.needs_rebuild(),
            "last_updated": None,
            "pdf_stats": {},
            "search_stats": {},
            "vector_stats": {}
        }
        
        if self.cache_file.exists():
            stats["last_updated"] = datetime.fromtimestamp(
                self.cache_file.stat().st_mtime
            ).isoformat()
        
        if self.processed_docs:
            stats["pdf_stats"] = self.pdf_processor.get_document_stats(self.processed_docs)
        
        if self.document_search:
            stats["search_stats"] = {
                "total_searchable_chunks": len(self.document_search.chunks),
                "keyword_search_available": True
            }
        
        if self.vector_db.is_available():
            stats["vector_stats"] = self.vector_db.get_database_stats()
            stats["search_stats"]["semantic_search_available"] = True
        else:
            stats["search_stats"]["semantic_search_available"] = False
        
        return stats
    
    def clear_cache(self) -> bool:
        """Clear the knowledge base cache."""
        try:
            if self.cache_file.exists():
                self.cache_file.unlink()
            
            self.processed_docs = {}
            self.document_search = None
            
            if self.vector_db.is_available():
                self.vector_db.clear_database()
            
            st.success("✅ Knowledge base cache cleared!")
            return True
        except Exception as e:
            st.error(f"Failed to clear cache: {str(e)}")
            return False
    
    def get_document_preview(self, document_name: str, max_chunks: int = 3) -> Dict[str, Any]:
        """Get a preview of a specific document."""
        if not self.is_initialized() or document_name not in self.processed_docs:
            return {}
        
        doc = self.processed_docs[document_name]
        preview_chunks = doc["chunks"][:max_chunks]
        
        return {
            "metadata": doc["metadata"],
            "chunk_count": doc["chunk_count"],
            "preview_chunks": preview_chunks
        }
    
    def find_relevant_content(self, discovery_notes: str, max_results: int = 10) -> Dict[str, Any]:
        """Find content relevant to customer discovery notes."""
        if not discovery_notes.strip():
            return {"results": [], "search_terms": [], "summary": "No discovery notes provided"}
        
        # Extract key terms from discovery notes
        search_terms = self._extract_search_terms(discovery_notes)
        
        # Perform searches with different terms
        all_results = []
        for term in search_terms[:5]:  # Limit to top 5 terms
            results = self.search(term, search_type="semantic" if self.vector_db.is_available() else "keyword", max_results=3)
            for result in results:
                result["search_term"] = term
                all_results.append(result)
        
        # Remove duplicates and sort by relevance
        unique_results = self._deduplicate_results(all_results)
        
        return {
            "results": unique_results[:max_results],
            "search_terms": search_terms,
            "summary": f"Found {len(unique_results)} relevant chunks across {len(set(r['source_file'] for r in unique_results))} documents"
        }
    
    def _extract_search_terms(self, text: str) -> List[str]:
        """Extract relevant search terms from discovery notes."""
        # Common Dell product/technology terms
        dell_terms = [
            "vxrail", "powerstore", "powerflex", "powerscale", "prosupport",
            "vmware", "hci", "hyperconverged", "storage", "compute",
            "virtualization", "cloud", "backup", "replication", "ai", "ml"
        ]
        
        text_lower = text.lower()
        found_terms = []
        
        # Find Dell-specific terms
        for term in dell_terms:
            if term in text_lower:
                found_terms.append(term)
        
        # Add other important keywords (basic extraction)
        words = text_lower.split()
        important_words = [
            w for w in words 
            if len(w) > 4 and w not in ["that", "this", "with", "from", "they", "have", "been", "will", "would", "could", "should"]
        ]
        found_terms.extend(important_words[:10])  # Limit additional terms
        
        return list(set(found_terms))  # Remove duplicates
    
    def _deduplicate_results(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate results based on chunk content."""
        seen_chunks = set()
        unique_results = []
        
        for result in results:
            chunk_id = f"{result.get('source_file', '')}_{result.get('metadata', {}).get('chunk_id', result.get('chunk_id', ''))}"
            if chunk_id not in seen_chunks:
                seen_chunks.add(chunk_id)
                unique_results.append(result)
        
        # Sort by relevance score
        return sorted(unique_results, key=lambda x: x.get('similarity_score', x.get('relevance_score', 0)), reverse=True)