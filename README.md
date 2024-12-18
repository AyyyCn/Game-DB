# 🎮 **Game-Insight: Aspect-Based Sentiment Analysis**

Discover what players love (or hate) about games! This project analyzes user reviews to identify game aspects (e.g., graphics, gameplay) and their associated sentiments using **NER** and **BERT**.

---

## 🚀 **Features**
- **Aspect Extraction**: Detects game aspects like *graphics*, *gameplay*, and *story*.
- **Sentiment Analysis**: Classifies sentiments as *Positive*, *Neutral*, or *Negative*.
- **Visual Insights**: Generates interactive charts and word clouds for trends.

---

## 🔧 **How It Works**
1. **Scraping**: Collect user reviews from sources like forums, YouTube comments, and Reddit posts.
2. **BERT Fine-Tuning**: Train a BERT model on labeled sentiment data to classify user sentiments.
3. **Aspect Analysis**: Use NER and keyword matching to detect specific aspects (e.g., graphics, gameplay) in the comments.
4. **Visualization**: Generate bar charts, word clouds, and other visual insights to understand sentiment trends.

---

## 🔧 **Setup**

### Prerequisites
- Python 3.9+
- Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Steps
1. **Clone Repository**:
   ```bash
   git clone https://github.com/YourUsername/Game-Insight.git
   cd Game-Insight
   ```

2. **Scrape User Reviews**:
   - Use the provided scraper scripts in the `scrapers/` folder to gather comments from YouTube or Reddit.

3. **Fine-Tune BERT**:
   - Prepare sentiment-labeled data.
   - Train the BERT model using:
     ```bash
     python bert/train_bert.py
     ```

4. **Aspect Analysis**:
   - Extract aspects from the comments:
     ```bash
     python aspect_analysis/aspect_extraction.py
     ```
   - Perform sentiment analysis on the extracted aspects:
     ```bash
     python aspect_analysis/aspect_sentiment.py
     ```

5. **Visualize Results**:
   - Generate charts and word clouds:
     ```bash
     python visualize_aspects.py
     ```

---

## 🌟 **Planned Features**
- **Interactive Web Dashboard** for real-time analysis.
- Fine-tuned **ABSA Models** for deeper aspect-specific insights.


