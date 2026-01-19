# AI Features Documentation

## Overview

SchoolSharthi now includes comprehensive AI-powered features designed specifically for Indian students, with bilingual support (Hindi + English) and practical, motivational guidance.

## AI Study Assistant Features

### 1. Chapter-wise Doubt Solver
**Endpoint:** `POST /api/ai/doubt`

Solve academic doubts with step-by-step explanations in Hindi + English mix.

**Features:**
- Understands context from subject, class, and chapter
- Provides bilingual explanations (Hinglish)
- Step-by-step solutions
- Encouraging and motivational tone

**Request:**
```json
{
  "question": "What is Newton's first law?",
  "subject": "physics",
  "class_level": "11",
  "chapter": "Laws of Motion"
}
```

### 2. Important Questions Generator
**Endpoint:** `POST /api/ai/important-questions`

Generate important exam questions for any chapter.

**Features:**
- Generates conceptual, numerical, and application-based questions
- Based on Indian board exam patterns
- Includes frequently asked topics
- Bilingual format

**Request:**
```json
{
  "subject": "physics",
  "class_level": "12",
  "chapter": "Electromagnetic Induction",
  "count": 10
}
```

### 3. PYQ Pattern Analyzer
**Endpoint:** `POST /api/ai/pyq-patterns`

Analyze Previous Year Questions to find repeated patterns and important topics.

**Features:**
- Identifies frequently asked topics
- Shows question type distribution
- Chapter-wise weightage analysis
- Practical preparation tips

**Request:**
```json
{
  "exam_type": "neet",
  "subject": "physics",
  "year_range": "2019-2023"
}
```

### 4. Step-by-Step Solution Generator
**Endpoint:** `POST /api/ai/step-by-step`

Get detailed step-by-step solutions for any problem.

**Features:**
- Clear step-by-step breakdown
- Explains why each step is taken
- Includes formula/concept used
- Verification and checking

**Request:**
```json
{
  "problem": "A car accelerates from rest to 60 km/h in 10 seconds. Find its acceleration.",
  "subject": "physics"
}
```

## AI Career Counselor Features

### Guidance Types

#### 1. Stream Selection (10th के बाद)
**Type:** `stream_selection`

Helps students choose between Science, Commerce, and Arts streams after 10th.

**Focus Areas:**
- Career options for each stream
- Skills required
- Job opportunities
- Government schemes

#### 2. Career Roadmap (12th के बाद)
**Type:** `career_roadmap_12th`

Provides roadmap after 12th for different streams.

**Focus Areas:**
- Degree vs Diploma vs Skill courses
- Government vs Private colleges
- Scholarships and financial aid
- Career growth paths

#### 3. NEET/JEE Strategy
**Type:** `neet_jee_strategy`

Preparation strategy for medical and engineering entrance exams.

**Focus Areas:**
- Study schedule and time management
- Important topics and weightage
- Free resources and coaching
- Alternative paths if not selected

#### 4. Government Exams
**Type:** `govt_exams`

Guidance for government job exams.

**Focus Areas:**
- Popular exams (SSC, Railway, Banking)
- Eligibility and age limits
- Preparation strategy
- Free study materials

#### 5. Skill-Based Careers
**Type:** `skill_based`

Guidance for skill-based careers and vocational courses.

**Focus Areas:**
- ITI and vocational courses
- Short-term courses with job prospects
- Local employment opportunities
- Government skill development schemes

**Endpoint:** `POST /api/career/query`

**Request:**
```json
{
  "query": "मुझे 10th के बाद कौन सा stream choose करना चाहिए?",
  "guidance_type": "stream_selection"
}
```

## Language Support

All AI responses are provided in **Hindi + English mix (Hinglish)** to make them accessible to Indian students, especially those from rural areas.

## Key Features

1. **Bilingual Support**: All explanations in Hindi + English
2. **Rural-Friendly**: Simple language, practical advice
3. **Motivational**: Encouraging tone throughout
4. **Context-Aware**: Understands Indian education system
5. **Practical**: Real-world examples and actionable advice

## Frontend Pages

1. **`/ai-doubt`**: Chapter-wise doubt solver
2. **`/ai-assistant`**: 
   - Important Questions Generator
   - PYQ Pattern Analyzer
   - Step-by-Step Solution Generator
3. **`/career`**: Career guidance with type selection

## Configuration

To enable full AI features, configure OpenAI API key in `.env`:

```env
OPENAI_API_KEY=your-openai-api-key
```

If not configured, the system will return helpful placeholder responses.

## Usage Examples

### Solve a Doubt
```javascript
const response = await aiAPI.askDoubt({
  question: "What is the difference between speed and velocity?",
  subject: "physics",
  class_level: "11",
  chapter: "Motion in a Straight Line"
})
```

### Generate Important Questions
```javascript
const response = await aiAPI.generateImportantQuestions({
  subject: "chemistry",
  class_level: "12",
  chapter: "Organic Chemistry",
  count: 15
})
```

### Get Career Guidance
```javascript
const response = await careerAPI.askQuery({
  query: "12th Science के बाद मेरे options क्या हैं?",
  guidance_type: "career_roadmap_12th"
})
```

## Response Format

All AI responses are formatted with:
- Clear headings and sections
- Step-by-step explanations
- Key points highlighted
- Motivational messages
- Practical tips

## Best Practices

1. **Be Specific**: Provide subject, class, and chapter when available
2. **Use Guidance Types**: Select appropriate guidance type for better results
3. **Ask Clear Questions**: More specific questions get better answers
4. **Review History**: Check previous queries for reference

## Future Enhancements

- Voice input support
- Image-based problem solving
- Personalized learning paths
- Progress tracking
- Offline mode support
