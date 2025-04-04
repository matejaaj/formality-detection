### Dataset

For evaluation, I used the dataset from Pavlick and Tetreault (2016) [1]. The evaluation combines the Hugging Face train and test splits: 11,274 English sentences from four domains (2,775 news, 1,821 blog, 1,701 email, and 4,977 answers). XLM-R uses all 11,274 rows; Squinky uses only the 6,678 email and answers rows. Content origins can be found at the [link](https://huggingface.co/datasets/osyvokon/pavlick-formality-scores#contents).

The news and blog sentences are originally from Lahiri (2015) [2], while email and forum answers are introduced in Pavlick and Tetreault dataset. I used cleaned-up version from Hugging Face.

Each sentence has a formality score on a continuous scale from -3 (very informal) to +3 (very formal), based on the average rating from 5 human anotators.

### Models

#### s-nlp/xlmr_formality_classifier

This model is based on XLM-RoBERTa, a multilingual transformer, and was introduced by Dementieva et al. (2023) [3]. It was trained on the X-FORMAL dataset (English, French, Italian, and Portuguese sentences), and classifies sentences to formal or informal.

#### Squinky Formality Classifier

The Squinky was introduced in Lahiri’s 2015 paper. It uses logistic regression, based on features like punctuation, sentence length etc. It was trained on the SQUINKY! corpus, which contains over 7k sentences rated on formality, informativeness, and implicature.

In this project, I only tested Squinky on the email and forum answers domains from the Pavlick and Tetreault dataset — these weren’t part of the original training data for Squinky (which was just blogs and news), so it’s a solid test to see if the model can generalize to new types of writing.

### Evaluation Metric

I used Spearman’s rank correlation. It checks how well the model's classification of sentences aligns with the human rankings, even if the model outputs are binary (formal or informal) or probability scores instead of continuous values. This metric is pretty standard for tasks like this — for example, Babakov et al. (2023) [4] reported Spearman value of 0.76 on the test split of the same dataset I used.

### References

[1] E. Pavlick and J. Tetreault, “An empirical analysis of formality in online communication,” _Transactions of the Association for Computational Linguistics_, vol. 4, pp. 61–74, 2016.

[2] S. Lahiri, “SQUINKY! A corpus of sentence-level formality, informativeness, and implicature,” _arXiv preprint arXiv:1506.02306_, 2015.

[3] D. Dementieva, N. Babakov, and A. Panchenko, “Detecting text formality: A study of text classification approaches,” in _Proceedings of the 14th International Conference on Recent Advances in Natural Language Processing (RANLP)_, Varna, Bulgaria, Sep. 2023, pp. 274–284.

[4] N. Babakov, D. Dale, I. Gusev, I. Krotova, and A. Panchenko, “Don’t lose the message while paraphrasing: A study on content preserving style transfer,” in _Natural Language Processing and Information Systems_, E. Métais, F. Meziane, V. Sugumaran, W. Manning, and S. Reiff-Marganiec, Eds. Cham: Springer, 2023, pp. 47–61.
