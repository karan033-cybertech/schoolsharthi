"""
PYQ Analysis System
Detects repeated questions, finds important chapters, predicts weightage, generates mock tests
"""
import re
from typing import List, Dict, Tuple, Optional
from collections import Counter, defaultdict
from sqlalchemy.orm import Session
from app.models import PYQ, ExamType, Subject
from app.database import get_db
import json


class PYQAnalyzer:
    """Analyze Previous Year Questions for patterns and insights"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_pyqs(self, exam_type: ExamType, subject: Optional[Subject] = None, years: Optional[List[int]] = None) -> List[PYQ]:
        """Get PYQs from database"""
        query = self.db.query(PYQ).filter(
            PYQ.exam_type == exam_type,
            PYQ.is_approved == True
        )
        
        if subject:
            query = query.filter(PYQ.subject == subject)
        
        if years:
            query = query.filter(PYQ.year.in_(years))
        
        return query.order_by(PYQ.year.desc()).all()
    
    def detect_repeated_questions(self, exam_type: ExamType, subject: Optional[Subject] = None, years: Optional[List[int]] = None) -> Dict:
        """
        Detect repeated questions across years
        Uses keyword matching and pattern recognition
        """
        pyqs = self.get_pyqs(exam_type, subject, years)
        
        # Extract keywords from titles and descriptions
        question_patterns = defaultdict(list)
        
        for pyq in pyqs:
            # Simple keyword extraction (can be enhanced with NLP)
            keywords = self._extract_keywords(pyq.title)
            key = self._create_pattern_key(keywords)
            question_patterns[key].append({
                'id': pyq.id,
                'title': pyq.title,
                'year': pyq.year,
                'subject': pyq.subject.value if pyq.subject else None
            })
        
        # Find patterns that appear multiple times
        repeated = {}
        for pattern, occurrences in question_patterns.items():
            if len(occurrences) > 1:
                repeated[pattern] = {
                    'count': len(occurrences),
                    'years': sorted([o['year'] for o in occurrences]),
                    'occurrences': occurrences,
                    'frequency': f"{len(occurrences)}/{len(pyqs)} years"
                }
        
        # Sort by frequency
        repeated_sorted = dict(sorted(repeated.items(), key=lambda x: x[1]['count'], reverse=True))
        
        return {
            'total_pyqs': len(pyqs),
            'repeated_patterns': repeated_sorted,
            'repetition_rate': len(repeated_sorted) / len(pyqs) * 100 if pyqs else 0
        }
    
    def find_important_chapters(self, exam_type: ExamType, subject: Optional[Subject] = None, years: Optional[List[int]] = None) -> Dict:
        """
        Find important chapters based on PYQ frequency
        """
        pyqs = self.get_pyqs(exam_type, subject, years)
        
        # Extract chapter information from titles
        chapter_frequency = Counter()
        chapter_years = defaultdict(set)
        
        for pyq in pyqs:
            chapters = self._extract_chapters(pyq.title)
            for chapter in chapters:
                chapter_frequency[chapter] += 1
                chapter_years[chapter].add(pyq.year)
        
        # Calculate importance score
        important_chapters = []
        total_pyqs = len(pyqs)
        
        for chapter, count in chapter_frequency.most_common():
            importance_score = (count / total_pyqs) * 100 if total_pyqs > 0 else 0
            years_appeared = sorted(list(chapter_years[chapter]))
            
            important_chapters.append({
                'chapter': chapter,
                'frequency': count,
                'importance_score': round(importance_score, 2),
                'years_appeared': years_appeared,
                'appearance_rate': f"{count}/{total_pyqs} PYQs"
            })
        
        return {
            'total_pyqs': total_pyqs,
            'important_chapters': important_chapters,
            'top_10_chapters': important_chapters[:10]
        }
    
    def predict_weightage(self, exam_type: ExamType, subject: Optional[Subject] = None, years: Optional[List[int]] = None) -> Dict:
        """
        Predict topic weightage based on historical data
        """
        pyqs = self.get_pyqs(exam_type, subject, years)
        
        if not pyqs:
            return {'error': 'No PYQs found'}
        
        # Analyze by year
        year_analysis = defaultdict(lambda: {'count': 0, 'topics': Counter()})
        
        for pyq in pyqs:
            year_analysis[pyq.year]['count'] += 1
            topics = self._extract_topics(pyq.title)
            for topic in topics:
                year_analysis[pyq.year]['topics'][topic] += 1
        
        # Calculate weightage trends
        topic_weightage = defaultdict(list)
        
        for year, data in sorted(year_analysis.items()):
            total = data['count']
            for topic, count in data['topics'].items():
                weightage = (count / total) * 100 if total > 0 else 0
                topic_weightage[topic].append({
                    'year': year,
                    'weightage': round(weightage, 2)
                })
        
        # Predict future weightage (simple average trend)
        predictions = {}
        for topic, history in topic_weightage.items():
            if len(history) >= 2:
                recent_weightage = sum([h['weightage'] for h in history[-3:]]) / min(3, len(history))
                trend = (history[-1]['weightage'] - history[0]['weightage']) / len(history) if len(history) > 1 else 0
                
                predictions[topic] = {
                    'current_weightage': history[-1]['weightage'],
                    'predicted_weightage': round(max(0, recent_weightage + trend), 2),
                    'trend': 'increasing' if trend > 0 else 'decreasing' if trend < 0 else 'stable',
                    'history': history
                }
        
        # Sort by predicted weightage
        predictions_sorted = dict(sorted(predictions.items(), key=lambda x: x[1]['predicted_weightage'], reverse=True))
        
        return {
            'years_analyzed': sorted(year_analysis.keys()),
            'topic_predictions': predictions_sorted,
            'high_weightage_topics': list(predictions_sorted.keys())[:10]
        }
    
    def generate_mock_test(self, exam_type: ExamType, subject: Optional[Subject] = None, 
                          num_questions: int = 30, difficulty: str = 'mixed') -> Dict:
        """
        Generate mock test based on PYQ patterns
        """
        pyqs = self.get_pyqs(exam_type, subject)
        
        if not pyqs:
            return {'error': 'No PYQs found'}
        
        # Get important chapters
        important_chapters = self.find_important_chapters(exam_type, subject)
        top_chapters = [ch['chapter'] for ch in important_chapters.get('top_10_chapters', [])[:5]]
        
        # Get weightage predictions
        weightage = self.predict_weightage(exam_type, subject)
        high_weightage_topics = weightage.get('high_weightage_topics', [])[:10]
        
        # Select questions based on patterns
        selected_questions = []
        
        # 60% from high weightage topics
        high_weightage_count = int(num_questions * 0.6)
        for topic in high_weightage_topics[:high_weightage_count]:
            matching_pyqs = [p for p in pyqs if topic.lower() in p.title.lower()]
            if matching_pyqs:
                selected_questions.append({
                    'type': 'high_weightage',
                    'topic': topic,
                    'reference_pyqs': [{'year': p.year, 'title': p.title} for p in matching_pyqs[:2]]
                })
        
        # 30% from important chapters
        chapter_count = int(num_questions * 0.3)
        for chapter in top_chapters[:chapter_count]:
            matching_pyqs = [p for p in pyqs if chapter.lower() in p.title.lower()]
            if matching_pyqs:
                selected_questions.append({
                    'type': 'important_chapter',
                    'chapter': chapter,
                    'reference_pyqs': [{'year': p.year, 'title': p.title} for p in matching_pyqs[:2]]
                })
        
        # 10% random
        remaining = num_questions - len(selected_questions)
        import random
        random_pyqs = random.sample(pyqs, min(remaining, len(pyqs)))
        for pyq in random_pyqs:
            selected_questions.append({
                'type': 'random',
                'reference_pyqs': [{'year': pyq.year, 'title': pyq.title}]
            })
        
        return {
            'exam_type': exam_type.value,
            'subject': subject.value if subject else 'All',
            'total_questions': len(selected_questions),
            'questions': selected_questions[:num_questions],
            'distribution': {
                'high_weightage': high_weightage_count,
                'important_chapters': chapter_count,
                'random': remaining
            },
            'based_on': {
                'total_pyqs_analyzed': len(pyqs),
                'important_chapters': top_chapters,
                'high_weightage_topics': high_weightage_topics[:5]
            }
        }
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text"""
        # Remove common words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        words = re.findall(r'\b\w+\b', text.lower())
        return [w for w in words if w not in stop_words and len(w) > 3]
    
    def _create_pattern_key(self, keywords: List[str]) -> str:
        """Create a pattern key from keywords"""
        # Use top 3 keywords as pattern
        return ' '.join(sorted(keywords[:3]))
    
    def _extract_chapters(self, text: str) -> List[str]:
        """Extract chapter names from text"""
        # Common chapter patterns
        patterns = [
            r'chapter\s+(\d+[a-z]?)',
            r'ch\.\s*(\d+)',
            r'(\w+\s+waves?)',
            r'(\w+\s+mechanics)',
            r'(\w+\s+optics)',
            r'(\w+\s+electricity)',
            r'(\w+\s+magnetism)',
        ]
        
        chapters = []
        text_lower = text.lower()
        
        for pattern in patterns:
            matches = re.findall(pattern, text_lower)
            chapters.extend(matches)
        
        # If no pattern match, try to extract from common Indian curriculum chapters
        if not chapters:
            common_chapters = [
                'motion', 'force', 'energy', 'waves', 'optics', 'electricity',
                'magnetism', 'atoms', 'nuclei', 'semiconductors', 'communication'
            ]
            for chapter in common_chapters:
                if chapter in text_lower:
                    chapters.append(chapter)
        
        return list(set(chapters)) if chapters else ['general']
    
    def _extract_topics(self, text: str) -> List[str]:
        """Extract topics from text"""
        # Common physics/chemistry/biology topics
        topics = []
        text_lower = text.lower()
        
        topic_keywords = {
            'mechanics': ['motion', 'force', 'momentum', 'energy', 'work', 'power'],
            'optics': ['light', 'lens', 'mirror', 'refraction', 'reflection'],
            'electricity': ['current', 'voltage', 'resistance', 'circuit', 'electric'],
            'magnetism': ['magnetic', 'field', 'induction', 'flux'],
            'waves': ['wave', 'frequency', 'amplitude', 'oscillation'],
            'thermodynamics': ['heat', 'temperature', 'entropy', 'thermodynamics'],
            'atoms': ['atom', 'electron', 'proton', 'nucleus'],
            'organic': ['organic', 'compound', 'reaction', 'molecule'],
            'inorganic': ['inorganic', 'element', 'periodic'],
            'biochemistry': ['biochemistry', 'enzyme', 'protein', 'dna']
        }
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                topics.append(topic)
        
        return topics if topics else ['general']


def analyze_pyqs(exam_type: ExamType, subject: Optional[Subject] = None, 
                 years: Optional[List[int]] = None, db: Session = None) -> Dict:
    """Main analysis function"""
    analyzer = PYQAnalyzer(db)
    
    return {
        'repeated_questions': analyzer.detect_repeated_questions(exam_type, subject, years),
        'important_chapters': analyzer.find_important_chapters(exam_type, subject, years),
        'weightage_prediction': analyzer.predict_weightage(exam_type, subject, years),
        'summary': {
            'exam_type': exam_type.value,
            'subject': subject.value if subject else 'All',
            'years_analyzed': years or 'All'
        }
    }
