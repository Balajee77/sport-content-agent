
## 🚀 Live Demo

SportsPulse AI is deployed on Streamlit Community Cloud.

**Live App:** https://sportspulse-ai.streamlit.app/


# SportsPulse AI 🏆

AI-Powered Sports Engagement Content Agent for generating fact-grounded, multi-format Instagram sports content.

## Project Overview

SportsPulse AI helps sports content creators generate fresh and engaging interactive content for Instagram.

The system supports multiple engagement formats instead of relying only on MCQs. It combines fresh web information, historical vector retrieval, LLM generation, schema validation, duplicate prevention, and Instagram-ready formatting.

## Supported Sports

- Cricket
- Football
- Tennis
- Badminton
- Basketball

## Supported Content Types

### 1. Multiple Choice Question
- Exactly 4 options
- One correct answer
- Short explanation
- Source citation

### 2. True / False
- Factual statement
- Boolean answer
- Short explanation
- Source citation

### 3. This-or-That Poll
- Exactly 2 options
- Opinion-based
- No factual correct answer
- Not fact-checked by design

### 4. Fill in the Blank
- Sentence containing a blank
- Exactly 4 options
- One correct answer
- Short explanation

### 5. Guess the Number
- Numeric target
- Accepted tolerance range
- Short explanation
- Source citation

## Core Features

- Sport selection
- Easy, Medium and Hard difficulty levels
- Generate batches of 4 or 5 items
- Mixed content types in one batch
- Individual item regeneration
- Full batch regeneration
- Fresh sports information through Tavily web search
- Stable and historical knowledge retrieval using ChromaDB
- Gemini-powered content generation
- Type-specific prompt templates
- Pydantic schema validation
- Duplicate-content prevention
- Source citations
- Web / ChromaDB / Opinion grounding indicators
- Instagram Story, Feed and Reel Caption formatting

## Architecture

```text
User
  ↓
Streamlit Dashboard
  ↓
Content Agent
  ↓
Hybrid Retrieval Layer
  ├── Tavily Web Search
  │      Recent / changing facts
  │
  └── ChromaDB
         Stable / historical facts
  ↓
Grounded Context
  ↓
Type-Specific Prompt
  ↓
Gemini LLM
  ↓
Pydantic Schema Validation
  ↓
Duplicate Detection
  ↓
Instagram Surface Formatter
  ↓
Final Content + Source Citation
