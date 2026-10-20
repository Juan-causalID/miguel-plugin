---
name: Hernán-Hsu-Healy 2019 taxonomy with verified AI/ML exemplars
description: PubMed-verified AI/ML papers mapped to descriptive/predictive/counterfactual data science tasks per Hernán, Hsu, Healy 2019 (Chance 32(1):42-49)
type: reference
---

Hernán MA, Hsu J, Healy B. A Second Chance to Get Causal Inference Right: A Classification of Data Science Tasks. Chance 2019;32(1):42-49. DOI: 10.1080/09332480.2019.1579578.

Three tasks: description (features of joint distribution), prediction (Y from X under observed distribution), counterfactual prediction (Y under interventions). The first two are non-causal in the formal sense; the third requires identification assumptions on top of any learning machinery.

PubMed-verified examples Juan uses in talks:

DESCRIPTIVE
- Do RKG, Lupton K, Causa Andrieu PI, et al. Patterns of Metastatic Disease in Patients with Cancer Derived from Natural Language Processing of Structured CT Radiology Reports over a 10-year Period. Radiology 2021;301:115-122. PMID 34342503, DOI 10.1148/radiol.2021210043.
- Chen RJ, Ding T, Lu MY, et al. Towards a general-purpose foundation model for computational pathology. Nat Med 2024;30:850-862. PMID 38504018, DOI 10.1038/s41591-024-02857-3. (UNI model.)
- Rajkomar A, Oren E, Chen K, et al. Scalable and accurate deep learning with electronic health records. NPJ Digit Med 2018;1:18. PMID 31304302, DOI 10.1038/s41746-018-0029-1. (Borderline descriptive/predictive: used for prediction but the embedding step is descriptive.)

PREDICTIVE
- Gulshan V, Peng L, Coram M, et al. Development and Validation of a Deep Learning Algorithm for Detection of Diabetic Retinopathy in Retinal Fundus Photographs. JAMA 2016;316:2402-2410. PMID 27898976, DOI 10.1001/jama.2016.17216.
- Esteva A, Kuprel B, Novoa RA, et al. Dermatologist-level classification of skin cancer with deep neural networks. Nature 2017;542:115-118. PMID 28117445, DOI 10.1038/nature21056.
- Attia ZI, Kapa S, Lopez-Jimenez F, et al. Screening for cardiac contractile dysfunction using an artificial intelligence-enabled electrocardiogram. Nat Med 2019;25:70-74. PMID 30617318, DOI 10.1038/s41591-018-0240-2.

COUNTERFACTUAL
- Inoue K, Athey S, Baicker K. Heterogeneous effects of Medicaid coverage on cardiovascular risk factors: secondary analysis of randomized controlled trial. BMJ 2024;386:e079377. PMID 39313257, DOI 10.1136/bmj-2024-079377. (Causal forest applied to Oregon Health Insurance Experiment to estimate CATE.)
- Dickerman BA, García-Albéniz X, Logan RW, et al. Avoidable flaws in observational analyses: an application to statins and cancer. Nat Med 2019;25:1601-1606. PMID 31591592, DOI 10.1038/s41591-019-0597-x. (Target trial emulation; pure methodological causal example, not ML-heavy.)
- Adams R, Henry KE, Sridharan A, et al. Prospective, multi-site study of patient outcomes after implementation of the TREWS machine learning-based early warning system for sepsis. Nat Med 2022;28:1455-1460. PMID 35864252, DOI 10.1038/s41591-022-01894-0. (Hybrid: ML risk score (predictive) deployed and then its causal effect on treatment timing evaluated; pair with companion paper PMID 35864251 by Henry KE et al.)

PREDICTIVE 2024+
- Gustafsson S, Ribeiro AH, Gedon D, et al. A deep learning ECG model for identification and localization of occlusion myocardial infarction. Nat Commun 2026;17(1):4336. PMID 42129209, DOI 10.1038/s41467-026-73023-1. (Deep-learning ECG on 540,372 emergency ECGs with cath outcomes; locates culprit lesion across 3 coronary branches; pure P(Y|X).)
- He S, Nie Y, Wang H, et al. Towards generalizable AI in medicine via Generalist-Specialist Collaboration. Nat Biomed Eng 2026 May 1. PMID 42067582, DOI 10.1038/s41551-026-01653-3. (MedDr foundation model + lightweight specialists across 32 medical imaging datasets; foundation-model exemplar.)
- Wu F, Xue Y, Yuhas PT, Gao XR. AUBADE-syn: a novel deep learning ensemble method for glaucoma detection using synthetic fundus images on imbalanced datasets. NPJ Digit Med 2026 May 14. PMID 42135460, DOI 10.1038/s41746-026-02752-w. (Diffusion-based synthetic augmentation + ensemble; EyePACS AUROC 0.992.)
- Wang C, Gao M, Ye J, et al. Interpretable machine learning model integrating MRI-derived paraspinal muscle parameters for predicting new vertebral compression fractures after vertebral augmentation. Eur Radiol 2026 May 15. PMID 42141290, DOI 10.1007/s00330-026-12632-2. (Random forest + MRI muscle parameters; external-validation AUC 0.837.)

COUNTERFACTUAL 2024+
- Young JC, Dahabreh IJ, James S, Erlinge D, Fröbert O, Berglund A, Rylance R, Hernán MA, Matthews AA. Extending inferences from a randomized trial to trial-eligible and treatment-candidate target populations: examples of generalizability and transportability. Epidemiology 2026 May 4. PMID 42081803, DOI 10.1097/EDE.0000000000001994. (Transportability of VALIDATE-SWEDEHEART bivalirudin vs heparin to trial-eligible and treatment-candidate Swedish registry populations.)
- Bulbulia JA, Davis DE, Park C, Rice KG, Troughton G, Van Tongeren DR, Sibley CG. Target trial emulation shows that supported causal effects of religious attendance on well-being are selective. Evol Hum Sci 2026;8:e16. PMID 42058103, DOI 10.1017/ehs.2026.10043. (Sequentially doubly robust + cross-validated ML nuisance learners; stochastic interventions because deterministic "make everyone attend" fails positivity.)
- Kim K, Kim J, Kennedy EH. Causal K-Means Clustering. J R Stat Soc Series B Stat Methodol 2026 Apr 27:qkag068. PMID 42064907, DOI 10.1093/jrsssb/qkag068. (Methodology: clusters unknown counterfactual functions; DML-based bias-corrected estimator with sqrt(n) rates; applied to chronic low back pain mobile self-management.)
- Zehra A, Deng Y, Swarna KS, Herrin J, Polley EC, Neumiller JJ, Galindo RJ, Umpierrez GE, Ross JS, Brito JP, Montori VM, Borah BJ, Maron BA, Mickelson MM, McCoy RG. Comparative Effectiveness of Individual Sodium Glucose Transporter 2 Inhibitors on Cardiovascular Outcomes in Type 2 Diabetes With Moderate Cardiovascular Risk: Emulation of a Target Trial. J Am Heart Assoc 2026;14:e046238. PMID 42132163, DOI 10.1161/JAHA.125.046238. (Three-way head-to-head comparative effectiveness; n=137,232; standard propensity-score weighting rather than heavy ML, but a clean active-comparator TTE; caveat: estimand is not strongly ML-flavored.)

Notes:
- Komorowski "AI Clinician" sepsis paper (PMID 30349085, Nat Med 2018;24:1716-1720) is sometimes invoked as counterfactual but is methodologically off-label policy evaluation with off-policy RL; raises strong concerns from causal inference perspective (Gottesman et al. critiques). Flag if Juan asks.
- The Attia ECG paper is predictive but has spawned counterfactual follow-ups (EAGLE trial NCT04000750) that would be examples of moving prediction toward intervention.
