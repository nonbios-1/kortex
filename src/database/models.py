from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .config import Base

class PromptWorkflow(Base):
    __tablename__ = "prompt_workflows"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    prompt_template = Column(String, nullable=False)
    parameters = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    evaluations = relationship("PromptEvaluation", back_populates="workflow")

class PromptEvaluation(Base):
    __tablename__ = "prompt_evaluations"

    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(Integer, ForeignKey("prompt_workflows.id"))
    input_data = Column(JSON)
    output_data = Column(JSON)
    metrics = Column(JSON)
    score = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    workflow = relationship("PromptWorkflow", back_populates="evaluations")

class TestSuite(Base):
    __tablename__ = "test_suites"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    workflow_id = Column(Integer, ForeignKey("prompt_workflows.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    workflow = relationship("PromptWorkflow", backref="test_suites")
    test_cases = relationship("TestCase", back_populates="test_suite")

class TestCase(Base):
    __tablename__ = "test_cases"

    id = Column(Integer, primary_key=True, index=True)
    test_suite_id = Column(Integer, ForeignKey("test_suites.id"))
    input_data = Column(JSON, nullable=False)
    expected_output = Column(JSON)
    metadata = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    test_suite = relationship("TestSuite", back_populates="test_cases")
    results = relationship("TestResult", back_populates="test_case")

class TestResult(Base):
    __tablename__ = "test_results"

    id = Column(Integer, primary_key=True, index=True)
    test_case_id = Column(Integer, ForeignKey("test_cases.id"))
    actual_output = Column(JSON)
    is_passed = Column(Boolean, nullable=False)
    error_message = Column(String)
    execution_time = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    test_case = relationship("TestCase", back_populates="results")
