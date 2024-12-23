# Kortex - Prompt Workflow Evaluation System
Design Documentation v1.0

## Overview
Kortex is a system designed to create, manage, and evaluate prompt workflows for Large Language Models (LLMs). It enables systematic prompt engineering through version control, test cases, and automated evaluation.

## Core Features
1. Prompt Workflow Management
   - Create and modify prompt workflows
   - Support for multiple prompts in sequence
   - Input/Output mapping using regex
   - Version control for workflows

2. Test Case Management
   - Define test cases with input data
   - Custom evaluation prompts per test case
   - Track test results across workflow versions

3. OpenRouter Integration
   - Support for multiple LLM models
   - Configurable model parameters
   - Flexible API integration

4. Evaluation System
   - Automated evaluation using LLMs
   - Score extraction using regex
   - Performance comparison across versions

## Technical Architecture

### Database Schema

```sql
-- Workflows
CREATE TABLE workflows (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    description TEXT,
    created_at TIMESTAMP
);

-- Prompts
CREATE TABLE prompts (
    id SERIAL PRIMARY KEY,
    workflow_id INTEGER REFERENCES workflows(id),
    sequence_order INTEGER,
    prompt_text TEXT,
    input_mapping JSONB,  -- Stores regex patterns for input extraction
    output_mapping JSONB  -- Stores regex patterns for output extraction
);

-- Test Cases
CREATE TABLE test_cases (
    id SERIAL PRIMARY KEY,
    workflow_id INTEGER REFERENCES workflows(id),
    name VARCHAR(255),
    input_data TEXT,      -- The test input
    evaluation_prompt TEXT, -- Prompt used to evaluate the output
    expected_score_regex TEXT, -- Regex to extract score from evaluation
    created_at TIMESTAMP
);

-- Test Results
CREATE TABLE test_results (
    id SERIAL PRIMARY KEY,
    test_case_id INTEGER REFERENCES test_cases(id),
    workflow_version INTEGER, -- To track workflow changes
    configuration_id INTEGER REFERENCES configurations(id),
    workflow_output TEXT,    -- Output from the workflow
    evaluation_output TEXT,  -- Raw output from evaluation
    score FLOAT,            -- Extracted score
    created_at TIMESTAMP
);

-- Configurations
CREATE TABLE configurations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    model_name VARCHAR(255),
    temperature FLOAT,
    max_tokens INTEGER,
    other_params JSONB
);

-- Workflow Versions
CREATE TABLE workflow_versions (
    id SERIAL PRIMARY KEY,
    workflow_id INTEGER REFERENCES workflows(id),
    version INTEGER,
    prompts_snapshot JSONB, -- Store the complete prompt workflow at this version
    created_at TIMESTAMP
);
```

### Core Components

#### 1. Workflow Manager
```python
class WorkflowManager:
    def create_workflow(name, description)
    def add_prompt(workflow_id, prompt_text, sequence_order, input_mapping, output_mapping)
    def update_prompt(prompt_id, prompt_text, input_mapping, output_mapping)
    def create_version(workflow_id)  # Creates a new version when prompts are modified
```

#### 2. Test Case Manager
```python
class TestCaseManager:
    def create_test_case(workflow_id, name, input_data, evaluation_prompt, expected_score_regex)
    def run_test_case(test_case_id, configuration_id)
    def run_all_test_cases(workflow_id, configuration_id)
```

#### 3. Evaluation System
```python
class EvaluationSystem:
    def evaluate_workflow_output(workflow_output, evaluation_prompt, configuration)
    def extract_score(evaluation_output, score_regex)
    def compare_versions(workflow_id, test_case_ids=[])
```

#### 4. Performance Tracker
```python
class PerformanceTracker:
    def get_version_performance(workflow_id, version)
    def get_trend_analysis(workflow_id)
    def get_test_case_history(test_case_id)
```

## Usage Example

```python
# Create a workflow
workflow_id = workflow_manager.create_workflow(
    name="Customer Support Response",
    description="Generate helpful customer support responses"
)

# Add prompts to workflow
prompt_id = workflow_manager.add_prompt(
    workflow_id=workflow_id,
    prompt_text="Given the customer inquiry: {{input}}, generate a helpful response",
    sequence_order=1,
    input_mapping={"input": ".*"},
    output_mapping={"response": "Response: (.*)"}
)

# Create test case
test_case_id = test_case_manager.create_test_case(
    workflow_id=workflow_id,
    name="Refund Request",
    input_data="I haven't received my refund yet. It's been 2 weeks.",
    evaluation_prompt="""
    Rate the following customer service response on a scale of 1-10:
    {{workflow_output}}
    
    Consider:
    1. Professionalism
    2. Helpfulness
    3. Clarity
    
    Provide the rating in format: RATING: X/10
    """,
    expected_score_regex="RATING: (\d+)/10"
)

# Run tests
test_results = test_case_manager.run_all_test_cases(
    workflow_id=workflow_id,
    configuration_id=config_id
)
```

## Technology Stack
- Backend: FastAPI (Python)
- Database: PostgreSQL
- ORM: SQLAlchemy
- API Client: OpenRouter API
- Frontend: Streamlit

## Project Structure
```
kortex/
├── backend/
│   ├── api/
│   ├── models/
│   ├── services/
│   │   ├── workflow_engine.py
│   │   ├── openrouter_client.py
│   │   └── evaluator.py
│   └── database/
├── frontend/
│   ├── pages/
│   └── components/
└── tests/
```

## Key Benefits
1. Version Control: Track changes in prompt workflows
2. Systematic Testing: Maintain test cases and track performance
3. Performance History: Monitor how changes affect output quality
4. Flexible Evaluation: Custom evaluation prompts per test case
5. Automated Regression Testing: Ensure changes don't decrease quality

## Future Enhancements
1. Support for more LLM providers
2. Advanced visualization of performance metrics
3. Collaborative features for team-based prompt engineering
4. Export/Import functionality for workflows and test cases
5. API documentation and SDK for programmatic access

