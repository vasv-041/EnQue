"""SQLAlchemy models for EnQue backend.
Defines tables for users, brands, brand_guidelines, campaigns, posts, post_metrics, audience_comments,
documents, document_chunks, recommendations, experiments, experiment_outcomes, and analysis_runs.
"""

from .db import Base
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Float, JSON
from sqlalchemy.orm import relationship
import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    brands = relationship("Brand", back_populates="owner", cascade="all, delete-orphan")

class Brand(Base):
    __tablename__ = "brands"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    brand_name = Column(String, nullable=False)
    description = Column(Text)
    industry = Column(String)
    target_audience = Column(Text)
    objectives = Column(Text)
    brand_voice = Column(Text)
    hindsight_bank_id = Column(String, unique=True, index=True)  # Isolated memory bank per brand
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    owner = relationship("User", back_populates="brands")
    guidelines = relationship("BrandGuideline", back_populates="brand", cascade="all, delete-orphan")
    campaigns = relationship("Campaign", back_populates="brand", cascade="all, delete-orphan")
    posts = relationship("Post", back_populates="brand", cascade="all, delete-orphan")
    audience_comments = relationship("AudienceComment", back_populates="brand", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="brand", cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="brand", cascade="all, delete-orphan")
    experiments = relationship("Experiment", back_populates="brand", cascade="all, delete-orphan")
    analysis_runs = relationship("AnalysisRun", back_populates="brand", cascade="all, delete-orphan")

class BrandGuideline(Base):
    __tablename__ = "brand_guidelines"
    id = Column(Integer, primary_key=True, index=True)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=False)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=True)
    brand_voice = Column(Text)
    communication_preferences = Column(Text)
    
    brand = relationship("Brand", back_populates="guidelines")

class Campaign(Base):
    __tablename__ = "campaigns"
    id = Column(Integer, primary_key=True, index=True)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=False)
    campaign_name = Column(String, nullable=False)
    objective = Column(Text)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    target_audience = Column(Text)
    budget = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    brand = relationship("Brand", back_populates="campaigns")
    posts = relationship("Post", back_populates="campaign")

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=False)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=True)
    platform = Column(String)
    caption = Column(Text)
    content_type = Column(String)
    topic = Column(String)
    post_date = Column(DateTime)
    external_post_id = Column(String, index=True, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    brand = relationship("Brand", back_populates="posts")
    campaign = relationship("Campaign", back_populates="posts")
    metrics = relationship("PostMetric", back_populates="post", uselist=False, cascade="all, delete-orphan")
    comments = relationship("AudienceComment", back_populates="post", cascade="all, delete-orphan")

class PostMetric(Base):
    __tablename__ = "post_metrics"
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False, unique=True)
    reach = Column(Float, default=0.0)
    impressions = Column(Float, default=0.0)
    likes = Column(Float, default=0.0)
    comments = Column(Float, default=0.0)
    shares = Column(Float, default=0.0)
    saves = Column(Float, default=0.0)
    clicks = Column(Float, default=0.0)
    recorded_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    post = relationship("Post", back_populates="metrics")

class AudienceComment(Base):
    __tablename__ = "audience_comments"
    id = Column(Integer, primary_key=True, index=True)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=True)
    external_comment_id = Column(String, index=True, nullable=True)
    comment_text = Column(Text, nullable=False)
    comment_date = Column(DateTime)
    platform = Column(String)
    sentiment = Column(String, nullable=True)  # Positive, Negative, Neutral
    topic = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    brand = relationship("Brand", back_populates="audience_comments")
    post = relationship("Post", back_populates="comments")

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=False)
    file_name = Column(String, nullable=False)
    document_type = Column(String)  # brand_guidelines, campaign_report, product_info, other
    file_path = Column(String, nullable=True)
    processing_status = Column(String, default="pending")  # pending, completed, failed
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    brand = relationship("Brand", back_populates="documents")
    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")

class DocumentChunk(Base):
    __tablename__ = "document_chunks"
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=False)
    chunk_index = Column(Integer, nullable=False)
    chunk_text = Column(Text, nullable=False)
    # Note: Vector embedding column can be added or stored as JSON/array for pgvector
    embedding = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    document = relationship("Document", back_populates="chunks")

class Recommendation(Base):
    __tablename__ = "recommendations"
    id = Column(Integer, primary_key=True, index=True)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=False)
    recommendation = Column(Text, nullable=False)
    reasoning = Column(Text)
    evidence = Column(JSON)
    expected_outcome = Column(Text)
    status = Column(String, default="proposed")  # proposed, implemented, rejected
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    brand = relationship("Brand", back_populates="recommendations")
    experiments = relationship("Experiment", back_populates="recommendation")

class Experiment(Base):
    __tablename__ = "experiments"
    id = Column(Integer, primary_key=True, index=True)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=False)
    recommendation_id = Column(Integer, ForeignKey("recommendations.id"), nullable=True)
    hypothesis = Column(Text, nullable=False)
    measurement_method = Column(Text)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    status = Column(String, default="active")  # active, completed, cancelled
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    brand = relationship("Brand", back_populates="experiments")
    recommendation = relationship("Recommendation", back_populates="experiments")
    outcomes = relationship("ExperimentOutcome", back_populates="experiment", cascade="all, delete-orphan")

class ExperimentOutcome(Base):
    __tablename__ = "experiment_outcomes"
    id = Column(Integer, primary_key=True, index=True)
    experiment_id = Column(Integer, ForeignKey("experiments.id"), nullable=False)
    actual_results = Column(JSON)
    evaluation = Column(String)  # Positive, Neutral, Negative
    learning_summary = Column(Text)
    evaluated_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    experiment = relationship("Experiment", back_populates="outcomes")

class AnalysisRun(Base):
    __tablename__ = "analysis_runs"
    id = Column(Integer, primary_key=True, index=True)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=False)
    analysis_type = Column(String, nullable=False)  # audience, content, full, strategy
    execution_status = Column(String, default="running")  # running, completed, failed
    result = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    brand = relationship("Brand", back_populates="analysis_runs")
