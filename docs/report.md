### Introduction

The goal of this project was to evaluate how well different models can detect sentence-level formality, by comparing their outputs to human-rated formality scores.

### Approach

Since the Pavlick and Tetrault dataset has continous formality scores, and both models I used output either binary labels or proabibilities, I used Spearman's rank correlation to compare the model predictions with human-annotated scores. This metric focuses on the relative ranking of values rather than exact numbers.

The XLM-R notebook combines the Hugging Face train and test splits (11,274 rows). The Squinky script filters the local dataset to email and answers (6,678 rows), excluding blog and news. Neither evaluation script trains a model.

For the xlmr_formality_classifier, I used the softmax probabilty assigned to the "formal" class as the model's prediction. This gives a continuous value between 0 and 1, which is more suitable for comparing against the continuous human formality scores in the dataset.

For Squinky, the model provides probabilty scores for both classes. I used raw probability of the "formal" class directly, instead of mapping it to a binary label. Squinky was not evaluated on blogs and news since that part of dataset was included in the model's training.

### Results - Spearman's Correlation

| **Domain**  | **XLM-R ρ** | **Squinky ρ** |
| ----------- | ----------- | ------------- |
| **Email**   | 0.5061      | 0.6538        |
| **Answers** | 0.7073      | 0.5095        |
| **Blog**    | 0.4082      | –             |
| **News**    | 0.1060      | –             |
| **Email + answers (6,678 rows)** | 0.7134 | 0.6023 |
| **All domains (11,274 rows)** | 0.6593 | – |

Results are computed from the saved prediction CSVs. The email + answers row compares both models on the same subset; the XLM-R notebook itself reports all domains and each domain separately.

Despite its simplicity, Squinky generalized well to unseen domains when using raw probability scores. XLM-R's correlation was lowest on news. These results alone do not establish the cause; evaluation uses continuous probabilities rather than binary predictions.

Overall, both models were able to capture sentence-level formality to a reasonable degree.

### Error Analysis

One common and obvious pattern was the difficulty both models had with classifying neutral sentences. For example, the sentence "A clean desk is a sign of a cluttered desk drawer." has a humar-rated score of 0.0, but both models assigned it a proabilities of being formal (Squinky: 0.91 and XLMR: 0.99).

Another issue appears with informal sentences, like "west indies for sure would win!!!", which recieved a human score of -3.0. Both models predicted very low formal probabilities (Squinky: 0.02, xlmr: 0.002), which is technically correct. However the same range of low values also appear for neutral sentences, making it hard to tell apart sentences that are slightly informal (or neutral) from those that are extremely informal. This is expected, since both models are trained to classify formality, not to measure how formal or how informal something is along a continuous scale.

### Challenges encountered

A significant portion of time was spent finding suitable models and datasets for evaluation. Many publicly available models were trained on the same datasets I planned to use for testing, including Pavlic and Tetrault corpus, which made it difficult to avoid data leakage and ensure a fair evaluation.

Setting up Squinky also came with challenges. The codebase depends on Python 3.6 and several outdated libraries, which required extra effort to get working in a modern environment.

Lastly, my initial evaluation approach involved converting model outputs to binary predictions (e.g -1 for informal and 1 for formal) before computing Spearman's correlation. This led to poor results due to the lack of granularity. Switching to using the raw probabilities from each model significantly improved the correlation scores and provided a more accurate reflection of how well the models captured relative formality.

### Final thoughts

While sentence-level formality prediction has its limitations in real-world applications like writing assistants — where formality is often relative, contextual, and varies across an entire document — it can still be a valuable baseline. When used thoughtfully, such predictions can help identify tone inconsistencies, guide adaptive suggestions, or contribute to a larger pipeline when aggregated across multiple sentences or combined with document-level cues.
