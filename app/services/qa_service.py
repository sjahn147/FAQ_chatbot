import json
from typing import Dict, List, Optional
from pathlib import Path

class QAService:
    def __init__(self):
        self.qa_data_path = Path(__file__).parent.parent / "core" / "qa_data.json"
        self.qa_data = self._load_qa_data()

    def _load_qa_data(self) -> Dict:
        """Q&A 데이터를 로드합니다."""
        try:
            with open(self.qa_data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Q&A 데이터 로드 중 오류 발생: {str(e)}")
            return {"categories": {}}

    def get_all_categories(self) -> List[Dict]:
        """모든 카테고리 정보를 반환합니다."""
        return [
            {"id": cat_id, "title": data["title"]}
            for cat_id, data in self.qa_data["categories"].items()
        ]

    def get_qa_pairs_by_category(self, category_id: str) -> List[Dict]:
        """특정 카테고리의 Q&A 쌍을 반환합니다."""
        category = self.qa_data["categories"].get(category_id)
        if not category:
            return []
        return category["qa_pairs"]

    def get_all_qa_pairs(self) -> List[Dict]:
        """모든 Q&A 쌍을 반환합니다."""
        all_pairs = []
        for category in self.qa_data["categories"].values():
            all_pairs.extend(category["qa_pairs"])
        return all_pairs

    def format_qa_context(self) -> str:
        """Q&A 데이터를 컨텍스트 형식으로 포맷팅합니다."""
        context_parts = []
        
        for category_id, category in self.qa_data["categories"].items():
            context_parts.append(f"=== {category['title']} ===")
            for qa in category["qa_pairs"]:
                context_parts.append(f"Q: {qa['question']}")
                context_parts.append(f"A: {qa['answer']}\n")
        
        return "\n".join(context_parts)

qa_service = QAService() 