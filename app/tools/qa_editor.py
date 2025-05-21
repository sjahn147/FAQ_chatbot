import sys
import json
from pathlib import Path
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QTreeWidget, QTreeWidgetItem, QPushButton, 
                            QTextEdit, QLabel, QMessageBox, QInputDialog, QLineEdit,
                            QSplitter, QFrame, QStatusBar)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon

class QAEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Q&A 편집기")
        self.setGeometry(100, 100, 1400, 900)
        
        # 데이터 파일 경로
        self.data_file = Path("app/core/qa_data.json")
        self.load_data()
        
        # 현재 선택된 항목 추적
        self.current_category_id = None
        self.current_qa_index = None
        
        # 메인 위젯 설정
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        
        # 스플리터 생성
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)
        
        # 왼쪽 패널 (카테고리 트리)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        # 카테고리 트리
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["카테고리/질문"])
        self.tree.setFont(QFont("맑은 고딕", 10))
        self.tree.setAlternatingRowColors(True)
        self.tree.setStyleSheet("""
            QTreeWidget {
                border: 1px solid #cccccc;
                border-radius: 4px;
            }
            QTreeWidget::item {
                padding: 4px;
            }
            QTreeWidget::item:selected {
                background-color: #e0e0e0;
            }
        """)
        self.tree.itemClicked.connect(self.on_item_clicked)
        left_layout.addWidget(self.tree)
        
        # 카테고리 관리 버튼
        category_buttons = QHBoxLayout()
        self.add_category_btn = QPushButton("카테고리 추가")
        self.add_category_btn.setMinimumWidth(120)
        self.add_category_btn.setStyleSheet("""
            QPushButton {
                padding: 8px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.delete_category_btn = QPushButton("카테고리 삭제")
        self.delete_category_btn.setMinimumWidth(120)
        self.delete_category_btn.setStyleSheet("""
            QPushButton {
                padding: 8px;
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        self.add_category_btn.clicked.connect(self.add_category)
        self.delete_category_btn.clicked.connect(self.delete_category)
        category_buttons.addWidget(self.add_category_btn)
        category_buttons.addWidget(self.delete_category_btn)
        category_buttons.addStretch()  # 오른쪽 여백 추가
        left_layout.addLayout(category_buttons)
        
        # 오른쪽 패널 (Q&A 편집)
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(10, 0, 10, 0)
        
        # 현재 선택된 항목 표시
        self.current_item_label = QLabel("선택된 항목: 없음")
        self.current_item_label.setStyleSheet("""
            QLabel {
                color: #666666;
                font-size: 12px;
                padding: 5px;
            }
        """)
        right_layout.addWidget(self.current_item_label)
        
        # 구분선
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        right_layout.addWidget(line)
        
        # 질문 편집
        question_label = QLabel("질문:")
        question_label.setFont(QFont("맑은 고딕", 11, QFont.Weight.Bold))
        self.question_edit = QTextEdit()
        self.question_edit.setFont(QFont("맑은 고딕", 10))
        self.question_edit.setMaximumHeight(100)
        self.question_edit.setStyleSheet("""
            QTextEdit {
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 5px;
            }
        """)
        right_layout.addWidget(question_label)
        right_layout.addWidget(self.question_edit)
        
        # 답변 편집
        answer_label = QLabel("답변:")
        answer_label.setFont(QFont("맑은 고딕", 11, QFont.Weight.Bold))
        self.answer_edit = QTextEdit()
        self.answer_edit.setFont(QFont("맑은 고딕", 10))
        self.answer_edit.setStyleSheet("""
            QTextEdit {
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 5px;
            }
        """)
        right_layout.addWidget(answer_label)
        right_layout.addWidget(self.answer_edit)
        
        # Q&A 관리 버튼
        qa_buttons = QHBoxLayout()
        
        # Q&A 추가 버튼
        self.add_qa_btn = QPushButton("새 Q&A 추가")
        self.add_qa_btn.setMinimumWidth(120)
        self.add_qa_btn.setStyleSheet("""
            QPushButton {
                padding: 8px;
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        
        # 저장 버튼
        self.save_btn = QPushButton("편집 내용 저장")
        self.save_btn.setMinimumWidth(120)
        self.save_btn.setStyleSheet("""
            QPushButton {
                padding: 8px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        
        # Q&A 삭제 버튼
        self.delete_qa_btn = QPushButton("Q&A 삭제")
        self.delete_qa_btn.setMinimumWidth(120)
        self.delete_qa_btn.setStyleSheet("""
            QPushButton {
                padding: 8px;
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        
        # 버튼 이벤트 연결
        self.add_qa_btn.clicked.connect(self.add_qa)
        self.save_btn.clicked.connect(self.save_qa)
        self.delete_qa_btn.clicked.connect(self.delete_qa)
        
        # 버튼을 레이아웃에 추가
        qa_buttons.addWidget(self.add_qa_btn)
        qa_buttons.addWidget(self.save_btn)
        qa_buttons.addWidget(self.delete_qa_btn)
        qa_buttons.addStretch()  # 오른쪽 여백 추가
        
        # 초기 버튼 상태 설정
        self.save_btn.setEnabled(False)
        self.delete_qa_btn.setEnabled(False)
        
        # 레이아웃에 버튼 그룹 추가
        right_layout.addLayout(qa_buttons)
        
        # 스플리터에 패널 추가
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([400, 1000])  # 초기 크기 설정
        
        # 상태 표시줄 추가
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("준비")
        
        self.populate_tree()
        
    def load_data(self):
        """JSON 파일에서 데이터 로드"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = {"categories": {}}
            
    def save_data(self):
        """데이터를 JSON 파일에 저장"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)
        self.statusBar.showMessage("저장 완료", 3000)
            
    def populate_tree(self):
        """트리 위젯에 데이터 표시"""
        # 현재 선택된 항목과 확장 상태 저장
        expanded_items = []
        for i in range(self.tree.topLevelItemCount()):
            item = self.tree.topLevelItem(i)
            if item.isExpanded():
                expanded_items.append(item.text(0))
        
        # 현재 선택된 항목 저장
        current_item = self.tree.currentItem()
        current_category = current_item.parent().text(0) if current_item and current_item.parent() else None
        current_question = current_item.text(0) if current_item else None
        
        # 트리 업데이트
        self.tree.clear()
        for category_id, category in self.data["categories"].items():
            category_item = QTreeWidgetItem([category["title"]])
            category_item.setData(0, Qt.ItemDataRole.UserRole, category_id)
            category_item.setFont(0, QFont("맑은 고딕", 10, QFont.Weight.Bold))
            self.tree.addTopLevelItem(category_item)
            
            for qa in category["qa_pairs"]:
                qa_item = QTreeWidgetItem([qa["question"]])
                qa_item.setData(0, Qt.ItemDataRole.UserRole, qa)
                category_item.addChild(qa_item)
        
        # 이전 확장 상태 복원
        for i in range(self.tree.topLevelItemCount()):
            item = self.tree.topLevelItem(i)
            if item.text(0) in expanded_items:
                item.setExpanded(True)
        
        # 이전 선택 상태 복원
        if current_category and current_question:
            for i in range(self.tree.topLevelItemCount()):
                category_item = self.tree.topLevelItem(i)
                if category_item.text(0) == current_category:
                    for j in range(category_item.childCount()):
                        qa_item = category_item.child(j)
                        if qa_item.text(0) == current_question:
                            self.tree.setCurrentItem(qa_item)
                            break
                    break
                
    def on_item_clicked(self, item, column):
        """트리 아이템 클릭 시 처리"""
        if item.parent():  # Q&A 항목
            qa_data = item.data(0, Qt.ItemDataRole.UserRole)
            if qa_data:  # Q&A 데이터가 있는 경우에만 처리
                self.question_edit.setText(qa_data["question"])
                self.answer_edit.setText(qa_data["answer"])
                self.current_item_label.setText(f"선택된 항목: {item.parent().text(0)} > {qa_data['question']}")
                self.statusBar.showMessage("Q&A 편집 모드")
                
                # 현재 선택된 항목 저장
                self.current_category_id = item.parent().data(0, Qt.ItemDataRole.UserRole)
                self.current_qa_index = item.parent().indexOfChild(item)
                
                # Q&A 편집 버튼 활성화
                self.save_btn.setEnabled(True)
                self.delete_qa_btn.setEnabled(True)
        else:  # 카테고리 항목
            self.question_edit.clear()
            self.answer_edit.clear()
            self.current_item_label.setText(f"선택된 항목: {item.text(0)}")
            self.statusBar.showMessage("카테고리 선택됨")
            
            # 현재 선택된 항목 저장
            self.current_category_id = item.data(0, Qt.ItemDataRole.UserRole)
            self.current_qa_index = None
            
            # Q&A 편집 버튼 비활성화
            self.save_btn.setEnabled(False)
            self.delete_qa_btn.setEnabled(False)
            
    def add_category(self):
        """새 카테고리 추가"""
        title, ok = QInputDialog.getText(self, "카테고리 추가", "카테고리 제목:")
        if ok and title:
            category_id = title.lower().replace(" ", "_")
            self.data["categories"][category_id] = {
                "title": title,
                "qa_pairs": []
            }
            self.save_data()
            self.populate_tree()
            self.statusBar.showMessage(f"카테고리 '{title}' 추가됨", 3000)
            
    def delete_category(self):
        """선택된 카테고리 삭제"""
        current = self.tree.currentItem()
        if current and not current.parent():
            category_name = current.text(0)  # 삭제 전에 카테고리 이름 저장
            reply = QMessageBox.question(self, "확인", 
                                       f"정말로 카테고리 '{category_name}'를 삭제하시겠습니까?",
                                       QMessageBox.StandardButton.Yes | 
                                       QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                category_id = current.data(0, Qt.ItemDataRole.UserRole)
                del self.data["categories"][category_id]
                self.save_data()
                self.populate_tree()
                self.statusBar.showMessage(f"카테고리 '{category_name}' 삭제됨", 3000)
                # 편집 영역 초기화
                self.question_edit.clear()
                self.answer_edit.clear()
                self.current_item_label.setText("선택된 항목: 없음")
                
    def add_qa(self):
        """새 Q&A 추가"""
        current = self.tree.currentItem()
        if current and not current.parent():
            category_id = current.data(0, Qt.ItemDataRole.UserRole)
            category_title = current.text(0)  # 카테고리 제목 저장
            
            new_qa = {
                "question": "",
                "answer": ""
            }
            self.data["categories"][category_id]["qa_pairs"].append(new_qa)
            self.save_data()
            self.populate_tree()
            
            # 새로 추가된 Q&A 선택
            for i in range(self.tree.topLevelItemCount()):
                category_item = self.tree.topLevelItem(i)
                if category_item.text(0) == category_title:
                    last_qa_item = category_item.child(category_item.childCount() - 1)
                    if last_qa_item:
                        self.tree.setCurrentItem(last_qa_item)
                        self.on_item_clicked(last_qa_item, 0)
                    break
            
            self.statusBar.showMessage(f"카테고리 '{category_title}'에 새 Q&A 추가됨", 3000)
            
    def save_qa(self):
        """현재 Q&A 저장"""
        current = self.tree.currentItem()
        if current and current.parent():
            category_item = current.parent()
            category_id = category_item.data(0, Qt.ItemDataRole.UserRole)
            category_title = category_item.text(0)  # 카테고리 제목 저장
            qa_index = category_item.indexOfChild(current)
            
            question = self.question_edit.toPlainText().strip()
            answer = self.answer_edit.toPlainText().strip()
            
            if not question or not answer:
                QMessageBox.warning(self, "경고", "질문과 답변을 모두 입력해주세요.")
                return
            
            self.data["categories"][category_id]["qa_pairs"][qa_index] = {
                "question": question,
                "answer": answer
            }
            self.save_data()
            self.populate_tree()
            
            # 저장된 Q&A 다시 선택
            for i in range(self.tree.topLevelItemCount()):
                category_item = self.tree.topLevelItem(i)
                if category_item.text(0) == category_title:
                    if qa_index < category_item.childCount():
                        qa_item = category_item.child(qa_index)
                        self.tree.setCurrentItem(qa_item)
                        self.on_item_clicked(qa_item, 0)
                    break
            
            self.statusBar.showMessage("Q&A 저장 완료", 3000)
            
    def delete_qa(self):
        """선택된 Q&A 삭제"""
        current = self.tree.currentItem()
        if current and current.parent():
            category_item = current.parent()
            category_id = category_item.data(0, Qt.ItemDataRole.UserRole)
            category_title = category_item.text(0)  # 카테고리 제목 저장
            
            reply = QMessageBox.question(self, "확인", 
                                       f"정말로 이 Q&A를 삭제하시겠습니까?\n\n질문: {current.text(0)}",
                                       QMessageBox.StandardButton.Yes | 
                                       QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                qa_index = category_item.indexOfChild(current)
                del self.data["categories"][category_id]["qa_pairs"][qa_index]
                self.save_data()
                self.populate_tree()
                
                # 카테고리 선택
                for i in range(self.tree.topLevelItemCount()):
                    category_item = self.tree.topLevelItem(i)
                    if category_item.text(0) == category_title:
                        self.tree.setCurrentItem(category_item)
                        self.on_item_clicked(category_item, 0)
                        break
                
                self.statusBar.showMessage("Q&A 삭제 완료", 3000)

def main():
    app = QApplication(sys.argv)
    window = QAEditor()
    window.show()
    sys.exit(app.exec()) 