# Formality Detection

Evaluation of XLM-R and Squinky for sentence-level formality detection, comparing their predictions with human ratings.

## Evaluation

The evaluation uses the [Pavlick and Tetreault dataset](https://huggingface.co/datasets/osyvokon/pavlick-formality-scores), with human formality scores from −3 (informal) to +3 (formal).

- **XLM-R**: evaluates `s-nlp/xlmr_formality_classifier` on all 11,274 sentences, combining the train and test splits.
- **Squinky**: evaluates 6,678 email and answers sentences. Blog and news are excluded because of overlap with its training data.

Both models use the probability of the formal class as their prediction. Performance is measured using Spearman’s rank correlation (ρ). No models are trained in this repository.

## Results

| Domain | Sentences | XLM-R ρ | Squinky ρ |
|---|---:|---:|---:|
| Email | 1,701 | 0.5061 | 0.6538 |
| Answers | 4,977 | 0.7073 | 0.5095 |
| Blog | 1,821 | 0.4082 | N/A |
| News | 2,775 | 0.1060 | N/A |
| Email + answers | 6,678 | 0.7134 | 0.6023 |
| All domains | 11,274 | 0.6593 | N/A |

Results are calculated from the saved prediction CSVs. The **email + answers** row compares both models on the same subset.

Squinky performs better on email; XLM-R performs better on answers. These probabilities reflect classification confidence, not a calibrated measure of formality.

## Reproduce

### XLM-R

Open the [notebook in Google Colab](https://colab.research.google.com/github/matejaaj/Formality-Detection/blob/main/xlm-roberta/xlm-roberta.ipynb) and select **Run all**. It downloads the model and dataset, generates predictions, and computes correlations. GPU acceleration is used when available.

The optional Google Drive export cell is commented out.

### Squinky

The supplied Conda environment targets **Windows with Python 3.6**. From the repository root, run these commands in Anaconda Prompt:

```bash
cd squinky
conda env create -f squinky_env.yml
conda activate squinky_env
conda install --force numpy=1.13.3 scipy=0.19.0 mkl=2017.0.4 scikit-learn=0.18.1
python predict_squinky.py
```

The dependency reinstall restores versions that Squinky’s pip installation may override. The script reads `dataset.csv`, prints correlations, and writes `squinky_predictions.csv`.

## Details

- [Report](docs/report.md): methodology, error analysis, and limitations.
- [Models and dataset](docs/tools.md): background and references.
