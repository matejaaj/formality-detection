import csv
from squinky.classifier import Classifier
from scipy.stats import spearmanr

clf = Classifier()

avg_scores = []
model_preds = []
domain_data = {}

TARGET_DOMAINS = {"email", "answers"}

with open("dataset.csv", newline='', encoding="utf-8") as infile:
    reader = csv.DictReader(infile)
    output_rows = []
    for row in reader:
        domain = row["domain"]
        if domain not in TARGET_DOMAINS:
            continue  

        sentence = row["sentence"]
        avg_score = float(row["avg_score"])

        form, _, _ = clf.predict(sentence)
        pred = form["formal"]

        avg_scores.append(avg_score)
        model_preds.append(pred)

        if domain not in domain_data:
            domain_data[domain] = {"avg": [], "pred": []}
        domain_data[domain]["avg"].append(avg_score)
        domain_data[domain]["pred"].append(pred)

        output_rows.append({
            "sentence": sentence,
            "domain": domain,
            "human_score": avg_score,
            "squinky_formal_probability": pred
        })

rho, pval = spearmanr(avg_scores, model_preds)
print("\nOverall Spearman R (email + answers): {:.4f} (p = {:.4e})".format(rho, pval))

print("\nSpearman R per domain:")
for domain in sorted(domain_data):
    domain_avg = domain_data[domain]["avg"]
    domain_pred = domain_data[domain]["pred"]
    r, p = spearmanr(domain_avg, domain_pred)
    print("{:<12} → R = {:.4f} (p = {:.4e})".format(domain, r, p))


with open("squinky_predictions.csv", mode="w", encoding="utf-8", newline="") as outfile:
    fieldnames = ["sentence", "domain", "human_score", "squinky_formal_probability"]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(output_rows)

