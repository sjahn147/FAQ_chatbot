from typing import Dict, Optional
import json
import os

class ContextManager:
    def __init__(self):
        self.contexts: Dict[str, str] = {}
        self.context_file = "contexts.json"
        self._load_contexts()

    def _load_contexts(self):
        if os.path.exists(self.context_file):
            with open(self.context_file, 'r', encoding='utf-8') as f:
                self.contexts = json.load(f)

    def _save_contexts(self):
        with open(self.context_file, 'w', encoding='utf-8') as f:
            json.dump(self.contexts, f, ensure_ascii=False, indent=2)

    def get_context(self, context_id: str) -> Optional[str]:
        return self.contexts.get(context_id)

    def save_context(self, context_id: str, context: str):
        self.contexts[context_id] = context
        self._save_contexts()

    def delete_context(self, context_id: str):
        if context_id in self.contexts:
            del self.contexts[context_id]
            self._save_contexts()

context_manager = ContextManager()

def get_context(context_id: str) -> Optional[str]:
    return context_manager.get_context(context_id)

def save_context(context_id: str, context: str):
    context_manager.save_context(context_id, context)

def delete_context(context_id: str):
    context_manager.delete_context(context_id) 