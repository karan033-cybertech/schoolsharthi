# PYQ Analysis System Guide

Complete guide for the PYQ Analysis System that detects repeated questions, finds important chapters, predicts weightage, and generates mock tests.

## Features

### 1. Repeated Questions Detection
Identifies questions that appear across multiple years using pattern matching and keyword analysis.

**Endpoint:** `GET /api/pyq-analysis/repeated-questions`

**Parameters:**
- `exam_type` (required): boards, neet, jee_main, jee_advanced
- `subject` (optional): physics, chemistry, biology, mathematics
- `years` (optional): Comma-separated years, e.g., "2020,2021,2022"

**Response:**
```json
{
  "total_pyqs": 150,
  "repeated_patterns": {
    "pattern_key": {
      "count": 5,
      "years": [2020, 2021, 2022, 2023],
      "occurrences": [...],
      "frequency": "5/150 years"
    }
  },
  "repetition_rate": 12.5
}
```

### 2. Important Chapters Analysis
Finds chapters that appear most frequently in PYQs.

**Endpoint:** `GET /api/pyq-analysis/important-chapters`

**Response:**
```json
{
  "total_pyqs": 150,
  "important_chapters": [
    {
      "chapter": "Electromagnetic Induction",
      "frequency": 25,
      "importance_score": 16.67,
      "years_appeared": [2020, 2021, 2022, 2023],
      "appearance_rate": "25/150 PYQs"
    }
  ],
  "top_10_chapters": [...]
}
```

### 3. Weightage Prediction
Predicts topic weightage based on historical trends.

**Endpoint:** `GET /api/pyq-analysis/weightage-prediction`

**Response:**
```json
{
  "years_analyzed": [2020, 2021, 2022, 2023],
  "topic_predictions": {
    "mechanics": {
      "current_weightage": 25.5,
      "predicted_weightage": 26.2,
      "trend": "increasing",
      "history": [...]
    }
  },
  "high_weightage_topics": ["mechanics", "optics", "electricity"]
}
```

### 4. Mock Test Generation
Generates mock tests based on PYQ patterns and weightage.

**Endpoint:** `POST /api/pyq-analysis/mock-test`

**Request:**
```json
{
  "exam_type": "neet",
  "subject": "physics",
  "num_questions": 30,
  "difficulty": "mixed"
}
```

**Response:**
```json
{
  "exam_type": "neet",
  "subject": "physics",
  "total_questions": 30,
  "questions": [
    {
      "type": "high_weightage",
      "topic": "mechanics",
      "reference_pyqs": [...]
    }
  ],
  "distribution": {
    "high_weightage": 18,
    "important_chapters": 9,
    "random": 3
  }
}
```

### 5. Full Analysis
Get complete analysis in one request.

**Endpoint:** `GET /api/pyq-analysis/full-analysis`

## Usage Examples

### Python Script
```python
from app.services.pyq_analyzer import PYQAnalyzer
from app.models import ExamType, Subject
from app.database import SessionLocal

db = SessionLocal()
analyzer = PYQAnalyzer(db)

# Detect repeated questions
repeated = analyzer.detect_repeated_questions(
    ExamType.NEET,
    Subject.PHYSICS,
    years=[2020, 2021, 2022, 2023]
)

# Find important chapters
chapters = analyzer.find_important_chapters(
    ExamType.NEET,
    Subject.PHYSICS
)

# Predict weightage
weightage = analyzer.predict_weightage(
    ExamType.NEET,
    Subject.PHYSICS
)

# Generate mock test
mock_test = analyzer.generate_mock_test(
    ExamType.NEET,
    Subject.PHYSICS,
    num_questions=30
)
```

### API Calls
```bash
# Get repeated questions
curl -X GET "https://api.schoolsharthi.com/api/pyq-analysis/repeated-questions?exam_type=neet&subject=physics&years=2020,2021,2022" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Generate mock test
curl -X POST "https://api.schoolsharthi.com/api/pyq-analysis/mock-test" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "exam_type": "neet",
    "subject": "physics",
    "num_questions": 30
  }'
```

## Algorithm Details

### Pattern Detection
1. Extract keywords from PYQ titles
2. Create pattern keys from top keywords
3. Group PYQs by pattern
4. Identify patterns appearing multiple times

### Chapter Extraction
1. Use regex patterns to identify chapter names
2. Match against common curriculum chapters
3. Calculate frequency and importance scores

### Weightage Prediction
1. Analyze PYQs by year
2. Calculate topic distribution per year
3. Identify trends (increasing/decreasing)
4. Predict future weightage using trend analysis

### Mock Test Generation
1. 60% questions from high-weightage topics
2. 30% questions from important chapters
3. 10% random questions for variety
4. Reference original PYQs for each question

## Frontend Integration

Add to `frontend/lib/api.ts`:
```typescript
export const pyqAnalysisAPI = {
  getRepeatedQuestions: (params: { exam_type: string; subject?: string; years?: string }) =>
    api.get('/api/pyq-analysis/repeated-questions', { params }),
  getImportantChapters: (params: { exam_type: string; subject?: string; years?: string }) =>
    api.get('/api/pyq-analysis/important-chapters', { params }),
  getWeightagePrediction: (params: { exam_type: string; subject?: string; years?: string }) =>
    api.get('/api/pyq-analysis/weightage-prediction', { params }),
  generateMockTest: (data: { exam_type: string; subject?: string; num_questions: number }) =>
    api.post('/api/pyq-analysis/mock-test', data),
  getFullAnalysis: (params: { exam_type: string; subject?: string; years?: string }) =>
    api.get('/api/pyq-analysis/full-analysis', { params }),
}
```

## Performance Considerations

- Analysis is performed on-demand (can be cached)
- For large datasets, consider background jobs
- Use Redis caching for frequent queries
- Implement pagination for large result sets

## Future Enhancements

- Machine learning for better pattern detection
- NLP for question similarity
- Advanced topic modeling
- Personalized mock tests based on weak areas
- Export mock tests as PDF
- Integration with question banks
