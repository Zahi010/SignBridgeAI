# SignBridge AI — Phase 5.6: Academic Evaluation Engine & Statistical Metrics

**Author:** Academic Research Statistician & Computational Linguist  
**Milestone:** Phase 5 — ISL Community Review, Expert Validation & Academic Evaluation Framework  
**Project:** SignBridge AI (`E:\SignBridgeAi`)  

---

## 1. Overview of Academic Evaluation Engine

To support peer-reviewed academic publication and clinical ISL validation, SignBridge AI includes a dedicated statistical engine (`backend/app/services/academic_metrics_service.py`). 

The engine implements established metrics for inter-rater reliability, inter-annotator agreement, sample size gating, and confidence intervals. Crucially, the engine **refuses to synthesize or hallucinate statistical values when sample sizes are zero or insufficient**.

---

## 2. Statistical Metrics Formulations

### 2.1 Cohen's Kappa ($\kappa$)
Used for evaluating inter-rater agreement between pairs of independent expert reviewers across discrete recommendation categories (`accept`, `reject`, `needs_revision`, `inconclusive`):

$$\kappa = \frac{P_o - P_e}{1 - P_e}$$

Where:
- $P_o$: Observed proportion of pairwise agreements across all evaluated signs:
  $$P_o = \frac{\sum \text{agreed pairs}}{\text{total pairs}}$$
- $P_e$: Expected proportion of agreement by chance, computed from marginal category frequencies:
  $$P_e = \sum_{k} \left(\frac{n_k}{N}\right)^2$$

Interpretation Scale (Landis & Koch):
- $\kappa < 0.20$: Slight agreement
- $0.21 - 0.40$: Fair agreement
- $0.41 - 0.60$: Moderate agreement
- $0.61 - 0.80$: Substantial agreement
- $0.81 - 1.00$: Almost perfect agreement

### 2.2 Criterion-Level Agreement Percentage
For each of the 12 phonological criteria (Handshape, Orientation, Movement, Location, etc.):

$$\text{Agreement}_c = \left(\frac{\text{Concordant Pairs}_c}{\text{Total Pairs}_c}\right) \times 100\%$$

Enables identification of specific phonological dimensions that produce high divergence (e.g. thumb opposition in complex handshapes).

### 2.3 Wilson Score 95% Confidence Interval
For the proportion of accepted signs ($\hat{p} = \frac{x}{n}$):

$$CI_{95} = \frac{\hat{p} + \frac{z^2}{2n} \pm z \sqrt{\frac{\hat{p}(1-\hat{p})}{n} + \frac{z^2}{4n^2}}}{1 + \frac{z^2}{n}}$$

Where $z = 1.96$. Unlike the normal approximation, the Wilson score interval maintains proper coverage even for small sample sizes and extreme proportions near $0$ or $1$.

---

## 3. Sample Size Sufficiency Categorization

SignBridge AI explicitly distinguishes four sample size tiers in the API output:

| Category | Sample Size ($N$) | Academic Validity Status | System Behavior |
| :--- | :---: | :--- | :--- |
| **`NO_DATA`** | $N = 0$ | No evaluations recorded | Returns `None` for $\kappa$; displays zero-fabrication notice. |
| **`INSUFFICIENT_SAMPLE_SIZE`** | $1 \le N < 5$ | Exploratory pilot only | Warns that sample size is statistically underpowered for publication. |
| **`PRELIMINARY_RESULTS`** | $5 \le N < 30$ | Initial trend indicator | Computes preliminary $\kappa$ and agreement; notes cohort expansion needed. |
| **`COMPLETED_EVALUATION`** | $N \ge 30$ | Scholarly publication ready | Full confidence intervals and inter-rater reliability certified. |

---

## 4. API Response Structure (`GET /api/v1/validation/academic-metrics`)

```json
{
  "sample_size_category": "PRELIMINARY_RESULTS",
  "total_signs_reviewed": 5,
  "total_verified_reviewers": 2,
  "total_evaluations": 5,
  "cohens_kappa": 0.625,
  "fleiss_kappa": 0.625,
  "average_inter_reviewer_agreement_percent": 84.2,
  "disagreement_frequency_percent": 20.0,
  "critical_error_count": 1,
  "criterion_statistics": [
    {
      "criterion_name": "handshape",
      "total_evaluations": 5,
      "agreement_percentage": 80.0,
      "pass_rate": 80.0,
      "major_error_rate": 20.0
    }
  ],
  "confidence_interval_95": {
    "lower": 23.1,
    "upper": 82.5
  },
  "academic_disclaimer": "Preliminary validation cohort (N=5 evaluations). Results indicate initial trends but require expansion to N>=30 across diverse Deaf regional cohorts for definitive publication."
}
```

