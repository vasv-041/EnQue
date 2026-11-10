"""Synthetic Demo Dataset Generator for GlowUp Skincare.
Generates realistic CSV datasets for Posts, Campaigns, and Audience Comments
using standard Python (csv and datetime) without requiring external dependencies.
"""

import os
import csv
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEMO_DIR = os.path.join(BASE_DIR, "datasets", "demo")
os.makedirs(DEMO_DIR, exist_ok=True)

def generate_demo_dataset():
    start_date = datetime(2025, 1, 10)
    
    # 1. Campaigns
    campaigns_file = os.path.join(DEMO_DIR, "campaigns.csv")
    campaigns = [
        {"campaign_id": "CMP_101", "campaign_name": "New Year Glow Routine", "objective": "Brand Awareness", "target_audience": "Gen-Z & Millennials", "budget": 5000},
        {"campaign_id": "CMP_102", "campaign_name": "Barrier Repair Deep Dive", "objective": "Engagement & Saves", "target_audience": "Skincare Enthusiasts with Sensitive Skin", "budget": 7500},
        {"campaign_id": "CMP_103", "campaign_name": "Ingredient Truths: Niacinamide & Zinc", "objective": "Audience Education", "target_audience": "Acne & Texture Concerns", "budget": 6000}
    ]
    with open(campaigns_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["campaign_id", "campaign_name", "objective", "target_audience", "budget"])
        writer.writeheader()
        writer.writerows(campaigns)

    # 2. Posts (30 records showing two distinct periods)
    posts_file = os.path.join(DEMO_DIR, "posts.csv")
    posts = [
        # Period 1: Routine & Aesthetics
        ("P_01", "instagram", start_date, "Kickstart your morning glow with our 3-step cleanser! ✨ Drop a 💕 if you love a minimalist routine.", "carousel", "morning routine", 4500, 6200, 310, 42, 18, 95, 25, "CMP_101"),
        ("P_02", "instagram", start_date + timedelta(days=2), "Hydration check! 💧 Is hyaluronic acid your best friend during dry winter mornings?", "single_image", "hydration", 3800, 4900, 240, 31, 10, 45, 15, "CMP_101"),
        ("P_03", "instagram", start_date + timedelta(days=4), "Glow from within: our daily antioxidant moisturizer in action.", "reel", "product spotlight", 8900, 14200, 780, 85, 92, 340, 80, "CMP_101"),
        ("P_04", "instagram", start_date + timedelta(days=7), "Minimalist makeup starts with healthy skin. How do you prep your base?", "carousel", "routine prep", 4100, 5200, 260, 28, 14, 88, 20, "CMP_101"),
        ("P_05", "instagram", start_date + timedelta(days=9), "Self-care Sunday vibes with our soothing oat mask. 🧖‍♀️", "single_image", "self care", 3200, 4100, 190, 15, 8, 30, 10, "CMP_101"),
        ("P_06", "tiktok", start_date + timedelta(days=12), "POV: Applying your SPF every 2 hours like a skincare pro ☀️", "reel", "sun protection", 12500, 21000, 1450, 160, 210, 820, 140, "CMP_101"),
        ("P_07", "instagram", start_date + timedelta(days=15), "Customer spotlight: Sarah's glowing skin journey after 30 days! 🌟", "carousel", "social proof", 5200, 6800, 380, 50, 35, 140, 60, "CMP_101"),
        ("P_08", "instagram", start_date + timedelta(days=18), "Night routine essentials: Lock in moisture while you sleep 🌙", "carousel", "night routine", 4600, 5900, 320, 39, 22, 110, 30, "CMP_101"),
        ("P_09", "instagram", start_date + timedelta(days=21), "Quick poll: Oil cleanser or micellar water? Tell us in the comments! 👇", "single_image", "skincare tips", 3500, 4400, 210, 85, 12, 40, 15, "CMP_101"),
        ("P_10", "tiktok", start_date + timedelta(days=24), "3 common skincare mistakes you might still be making 🚫", "reel", "educational", 15400, 26000, 1890, 220, 340, 1450, 190, "CMP_101"),

        # Period 2: Barrier Repair & Ingredients
        ("P_11", "instagram", start_date + timedelta(days=32), "Is your skin barrier compromised? 🚨 4 warning signs you shouldn't ignore: redness, tightness, stinging.", "carousel", "barrier repair", 7800, 11200, 850, 115, 145, 920, 95, "CMP_102"),
        ("P_12", "instagram", start_date + timedelta(days=35), "Why Ceramides + Centella are non-negotiable for irritated skin. Save this guide! 📌", "carousel", "ingredient guide", 8400, 12500, 920, 140, 190, 1200, 120, "CMP_102"),
        ("P_13", "tiktok", start_date + timedelta(days=38), "Stop exfoliating every single night! Here is how to rebuild your damaged barrier in 14 days.", "reel", "barrier repair", 22000, 38000, 2800, 340, 620, 2400, 310, "CMP_102"),
        ("P_14", "instagram", start_date + timedelta(days=42), "Gentle vs harsh cleansers: The pH balance test you need to see. 🧪", "reel", "formulation science", 14500, 23000, 1600, 195, 280, 1550, 180, "CMP_102"),
        ("P_15", "instagram", start_date + timedelta(days=45), "Fragrance-free vs Natural Scents: What does sensitive skin really need?", "carousel", "ingredient safety", 6900, 9400, 640, 110, 85, 590, 75, "CMP_102"),
        ("P_16", "instagram", start_date + timedelta(days=48), "Ingredient deep-dive: Panthenol (Pro-Vitamin B5) and why your skin drinks it up.", "carousel", "ingredient guide", 7200, 10100, 710, 95, 110, 810, 85, "CMP_102"),
        ("P_17", "tiktok", start_date + timedelta(days=51), "How to use Retinol without ruining your barrier (The Sandwich Method explained) 🥪", "reel", "actives tutorial", 28000, 49000, 3900, 480, 950, 3800, 420, "CMP_102"),
        ("P_18", "instagram", start_date + timedelta(days=55), "Mythbusters: Does slugging with petrolatum clog your pores? 🧴", "carousel", "skincare myths", 9100, 13400, 980, 175, 180, 1140, 110, "CMP_102"),
        ("P_19", "instagram", start_date + timedelta(days=58), "Skin barrier rescue routine for when you accidentally over-did the AHA/BHA peel.", "carousel", "barrier repair", 8900, 12800, 940, 130, 210, 1350, 130, "CMP_102"),
        ("P_20", "instagram", start_date + timedelta(days=62), "Why we formulated without drying alcohols and artificial dyes. 🌿", "single_image", "clean formulation", 5100, 6900, 410, 65, 40, 230, 45, "CMP_102"),

        # Period 2 Continued: Actives & Acne Care
        ("P_21", "instagram", start_date + timedelta(days=68), "Is 10% Niacinamide too much? Why 2-5% is actually the clinical sweet spot. 🔬", "carousel", "ingredient safety", 11200, 16800, 1420, 240, 380, 2100, 210, "CMP_103"),
        ("P_22", "tiktok", start_date + timedelta(days=72), "Skin purging vs allergic breakout: How to tell the difference before panicking! 🚨", "reel", "educational", 31000, 56000, 4500, 620, 1200, 4900, 580, "CMP_103"),
        ("P_23", "instagram", start_date + timedelta(days=75), "Zinc PCA + Niacinamide: The duo that regulates sebum without stripping moisture.", "carousel", "acne care", 8800, 12900, 990, 145, 175, 1290, 140, "CMP_103"),
        ("P_24", "instagram", start_date + timedelta(days=78), "Full ingredient transparency: What every single % in our Barrier Elixir does.", "carousel", "transparency", 10400, 15100, 1250, 190, 260, 1820, 195, "CMP_103"),
        ("P_25", "tiktok", start_date + timedelta(days=82), "Stop combining these 3 actives in the same routine! Save this warning ⚠️", "reel", "routine tips", 24500, 43000, 3100, 390, 780, 3200, 360, "CMP_103")
    ]
    with open(posts_file, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["post_id", "platform", "post_date", "caption", "content_type", "topic", "reach", "impressions", "likes", "comments", "shares", "saves", "clicks", "campaign_id"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for p in posts:
            writer.writerow({
                "post_id": p[0], "platform": p[1], "post_date": p[2].strftime("%Y-%m-%d"),
                "caption": p[3], "content_type": p[4], "topic": p[5], "reach": p[6],
                "impressions": p[7], "likes": p[8], "comments": p[9], "shares": p[10],
                "saves": p[11], "clicks": p[12], "campaign_id": p[13]
            })

    # 3. Audience Comments (30 comments capturing audience sentiment and transition)
    comments_file = os.path.join(DEMO_DIR, "comments.csv")
    comments = [
        ("C_01", "P_01", "Love this aesthetic so much! Does it leave a white cast?", start_date + timedelta(days=1), "instagram"),
        ("C_02", "P_01", "My morning routine is incomplete without this glow cleanser 💕", start_date + timedelta(days=1), "instagram"),
        ("C_03", "P_02", "Can I use hyaluronic acid on dry skin or does it need to be damp?", start_date + timedelta(days=3), "instagram"),
        ("C_04", "P_03", "The texture is incredible, so lightweight and hydrating!", start_date + timedelta(days=5), "instagram"),
        ("C_05", "P_03", "Best moisturizer I have used all winter! Highly recommend.", start_date + timedelta(days=5), "instagram"),
        ("C_06", "P_06", "Finally an SPF that doesn't burn my sensitive eyes! Amazing.", start_date + timedelta(days=13), "tiktok"),
        ("C_07", "P_06", "Does it work well under foundation or does it pill?", start_date + timedelta(days=13), "tiktok"),
        ("C_08", "P_10", "I was definitely guilty of over-cleansing! Thank you for this.", start_date + timedelta(days=25), "tiktok"),
        ("C_09", "P_09", "Oil cleansing completely cleared my blackheads! Game changer.", start_date + timedelta(days=22), "instagram"),
        ("C_10", "P_05", "Smells so good and relaxing after a long week 🧖‍♀️", start_date + timedelta(days=10), "instagram"),
        ("C_11", "P_11", "My skin broke out so bad after using 10% AHA! Is my barrier damaged?", start_date + timedelta(days=33), "instagram"),
        ("C_12", "P_11", "Everything stung my face until I cut all actives. Saving this post!", start_date + timedelta(days=33), "instagram"),
        ("C_13", "P_12", "Centella is my holy grail for redness. Please never discontinue this!", start_date + timedelta(days=36), "instagram"),
        ("C_14", "P_12", "Can ceramides cause breakouts for fungal acne prone skin?", start_date + timedelta(days=36), "instagram"),
        ("C_15", "P_13", "I needed this so badly. My skin was burning from daily exfoliation 😭", start_date + timedelta(days=39), "tiktok"),
        ("C_16", "P_13", "The sandwich method literally saved my skin with retinol!", start_date + timedelta(days=40), "tiktok"),
        ("C_17", "P_14", "Most drugstore cleansers have a pH of 8! No wonder my skin felt stripped.", start_date + timedelta(days=43), "instagram"),
        ("C_18", "P_15", "Please keep all products fragrance free! Essential oils give me an allergic rash.", start_date + timedelta(days=46), "instagram"),
        ("C_19", "P_17", "Retinol purging was so scary for me. How long does the purging phase usually last?", start_date + timedelta(days=52), "tiktok"),
        ("C_20", "P_17", "Is it normal to get small whiteheads during the first 2 weeks?", start_date + timedelta(days=53), "tiktok"),
        ("C_21", "P_21", "YES! Finally someone addressing 10% Niacinamide toxicity. It broke me out so badly.", start_date + timedelta(days=69), "instagram"),
        ("C_22", "P_21", "I love that you guys formulated with 3% Niacinamide instead. Much gentler!", start_date + timedelta(days=70), "instagram"),
        ("C_23", "P_22", "This video cleared my confusion. Turns out I was purging, not reacting badly!", start_date + timedelta(days=73), "tiktok"),
        ("C_24", "P_22", "What if the breakout happens in areas where I never get acne?", start_date + timedelta(days=74), "tiktok"),
        ("C_25", "P_24", "This level of ingredient transparency is why GlowUp is my favorite skincare brand.", start_date + timedelta(days=79), "instagram"),
        ("C_26", "P_25", "Can I use Vitamin C in the morning and Niacinamide at night?", start_date + timedelta(days=83), "tiktok"),
        ("C_27", "P_19", "Saved this! Going to do this recovery routine tonight.", start_date + timedelta(days=59), "instagram"),
        ("C_28", "P_18", "Slugging changed my skin texture completely overnight!", start_date + timedelta(days=56), "instagram"),
        ("C_29", "P_15", "Does your packaging prevent oxidation of the active ingredients?", start_date + timedelta(days=47), "instagram"),
        ("C_30", "P_23", "Zinc PCA helped my redness so much without being drying.", start_date + timedelta(days=76), "instagram")
    ]
    with open(comments_file, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["comment_id", "post_id", "comment_text", "comment_date", "platform"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for c in comments:
            writer.writerow({
                "comment_id": c[0], "post_id": c[1], "comment_text": c[2],
                "comment_date": c[3].strftime("%Y-%m-%d"), "platform": c[4]
            })

    print(f"Demo CSV datasets successfully written to: {DEMO_DIR}")

if __name__ == "__main__":
    generate_demo_dataset()
