"""
Pydantic models for structured outputs from the CrewAI agents.
"""
from typing import List, Optional
from pydantic import BaseModel, Field


class Resource(BaseModel):
    """Individual learning resource model."""
    title: str = Field(..., description="Title of the resource")
    url: str = Field(..., description="URL/link to the resource")
    description: str = Field(..., description="Brief description of the resource content")
    resource_type: str = Field(..., description="Type: video, article, or exercise")


class LearningMaterial(BaseModel):
    """Complete learning materials output."""
    topic: str = Field(..., description="Main topic covered")
    expertise_level: str = Field(..., description="Target expertise level")
    videos: List[Resource] = Field(default_factory=list, description="List of video resources")
    articles: List[Resource] = Field(default_factory=list, description="List of article resources")
    exercises: List[Resource] = Field(default_factory=list, description="List of exercise resources")
    summary: str = Field(..., description="Overall summary of the learning path")


class QuizOption(BaseModel):
    """Individual quiz option."""
    option: str = Field(..., description="Option text (A, B, C, D)")
    text: str = Field(..., description="Option content")


class QuizQuestion(BaseModel):
    """Individual quiz question with multiple choice options."""
    question: str = Field(..., description="The question text")
    options: List[QuizOption] = Field(..., description="List of 4 options (A, B, C, D)")
    correct_answer: str = Field(..., description="The correct option (A, B, C, or D)")
    explanation: str = Field(..., description="Explanation of the correct answer")
    difficulty: str = Field(..., description="Difficulty level: easy, medium, or hard")


class Quiz(BaseModel):
    """Complete quiz output."""
    topic: str = Field(..., description="Quiz topic")
    total_questions: int = Field(..., description="Total number of questions")
    questions: List[QuizQuestion] = Field(..., description="List of quiz questions")
    estimated_time_minutes: int = Field(..., description="Estimated time to complete in minutes")


class Deliverable(BaseModel):
    """Individual project deliverable."""
    name: str = Field(..., description="Deliverable name")
    description: str = Field(..., description="What needs to be delivered")


class ProjectIdea(BaseModel):
    """Individual project idea."""
    title: str = Field(..., description="Project title")
    description: str = Field(..., description="High-level project description")
    expertise_level: str = Field(..., description="Target expertise level")
    estimated_duration: str = Field(..., description="Estimated time to complete")
    key_concepts: List[str] = Field(..., description="Key concepts covered in the project")
    deliverables: List[Deliverable] = Field(..., description="List of project deliverables")
    learning_outcomes: List[str] = Field(..., description="What the user will learn")


class ProjectSuggestions(BaseModel):
    """Complete project suggestions output."""
    topic: str = Field(..., description="Main topic")
    projects: List[ProjectIdea] = Field(..., description="List of project ideas")
    total_projects: int = Field(..., description="Total number of projects suggested")
