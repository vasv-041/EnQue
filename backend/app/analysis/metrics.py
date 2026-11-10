"""Deterministic metrics calculation engine using Pandas.
Implements the exact formulas defined in PRD Section 5.2.
"""

from typing import List, Dict, Any, Optional
import pandas as pd
import numpy as np

def calculate_post_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates:
    - Engagement Rate = (Likes + Comments + Shares + Saves) / Reach * 100
    - Save Rate = Saves / Reach * 100
    - Share Rate = Shares / Reach * 100
    - Comment Rate = Comments / Reach * 100
    Safely handles zero reach and missing metrics.
    """
    metrics_df = df.copy()

    # Ensure required columns exist with numeric conversion
    for col in ["reach", "impressions", "likes", "comments", "shares", "saves", "clicks"]:
        if col not in metrics_df.columns:
            metrics_df[col] = 0.0
        else:
            metrics_df[col] = pd.to_numeric(metrics_df[col], errors="coerce").fillna(0.0)

    # Safe division helper
    reach = metrics_df["reach"].replace(0, np.nan)
    total_engagements = metrics_df["likes"] + metrics_df["comments"] + metrics_df["shares"] + metrics_df["saves"]

    metrics_df["engagement_rate"] = (total_engagements / reach * 100).fillna(0.0).round(2)
    metrics_df["save_rate"] = (metrics_df["saves"] / reach * 100).fillna(0.0).round(2)
    metrics_df["share_rate"] = (metrics_df["shares"] / reach * 100).fillna(0.0).round(2)
    metrics_df["comment_rate"] = (metrics_df["comments"] / reach * 100).fillna(0.0).round(2)

    return metrics_df

def calculate_reach_growth(current_reach: float, previous_reach: float) -> float:
    """Reach Growth = (Current Reach - Previous Reach) / Previous Reach * 100"""
    if not previous_reach or previous_reach <= 0:
        return 0.0
    return round(((current_reach - previous_reach) / previous_reach) * 100, 2)

def summarize_content_performance(posts_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyzes content performance by format, topic, and overall metrics.
    Identifies top and underperforming content.
    """
    if posts_df.empty:
        return {
            "total_posts": 0,
            "avg_engagement_rate": 0.0,
            "top_performing_posts": [],
            "underperforming_posts": [],
            "performance_by_format": {},
            "performance_by_topic": {},
        }

    df = calculate_post_metrics(posts_df)
    
    # Sort by engagement rate
    sorted_df = df.sort_values(by="engagement_rate", ascending=False)
    
    # Top 5 and bottom 5
    top_posts = sorted_df.head(5).to_dict(orient="records")
    underperforming = sorted_df.tail(5).to_dict(orient="records")
    
    # Format grouping
    format_group = {}
    if "content_type" in df.columns:
        format_agg = df.groupby("content_type").agg(
            post_count=("id" if "id" in df.columns else "caption", "count"),
            avg_reach=("reach", "mean"),
            avg_engagement_rate=("engagement_rate", "mean"),
            avg_save_rate=("save_rate", "mean"),
            avg_share_rate=("share_rate", "mean")
        ).round(2)
        format_group = format_agg.to_dict(orient="index")

    # Topic grouping
    topic_group = {}
    if "topic" in df.columns:
        topic_agg = df.groupby("topic").agg(
            post_count=("id" if "id" in df.columns else "caption", "count"),
            avg_engagement_rate=("engagement_rate", "mean"),
            avg_reach=("reach", "mean")
        ).round(2)
        topic_group = topic_agg.to_dict(orient="index")

    return {
        "total_posts": len(df),
        "avg_engagement_rate": round(float(df["engagement_rate"].mean()), 2),
        "avg_save_rate": round(float(df["save_rate"].mean()), 2),
        "avg_share_rate": round(float(df["share_rate"].mean()), 2),
        "top_performing_posts": top_posts,
        "underperforming_posts": underperforming,
        "performance_by_format": format_group,
        "performance_by_topic": topic_group,
    }

