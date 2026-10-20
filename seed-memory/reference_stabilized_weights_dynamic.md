---
name: Stabilized weights for dynamic regimes (What If, ch 21)
description: What If book explicitly says deterministic dynamic regimes cannot use stabilized IP weights; only static or random dynamic regimes can
type: reference
---

Hernan and Robins, *Causal Inference: What If* (21nov25 PDF), Technical Point 21.2 ("IP weighting for dynamic treatment strategies"), p. 284:

Verbatim quote: "Unlike for static strategies, E[Y I(A_K = A^g_K) SW_A] / E[I(A_K = A^g_K) SW_A] does not equal the g-formula because the numerator of SW_A depends on A. Hence stabilized weights cannot be used with dynamic strategies. For a random dynamic strategy f^int, the g-formula is equal to E[Y * prod f^int(A_k|A_{k-1},L_k) / f(A_k|A_{k-1},L_k)]."

Implication:
- Deterministic dynamic regime g (e.g., "treat with vancomycin until deterioration"): use UNSTABILIZED weights W_A = 1/prod f(A_k | A_{k-1}, L_k), restricted to followers I(A_K = A^g_K). Stabilized SW_A is NOT valid because its numerator f(A_k | A_{k-1}) depends on A.
- Random dynamic regime f^int: a stabilized form IS valid, with numerator = f^int(A_k | A_{k-1}, L_k), the regime's own assignment density.
- Static regime: standard SW_A with marginal numerator f(A_k | A_{k-1}) is valid (ch 12 / ch 21).

The "partly-conditional" numerator f(A_k | A_{k-1}, L*_k) where L*_k is the regime-defining covariate (Robins/Hernan/Brumback 2000 Epidemiology 11:550-560; Hernan/Brumback/Robins 2000 JASA) is NOT presented in *What If* as a stabilization for deterministic dynamic regimes. The book frames the choice as: unstabilized for deterministic dynamic, or stabilized using f^int for random dynamic. The partly-conditional construction in the 2000 papers applies to specific MSM-type estimands and is a methods-paper extension, not book content.

For per-protocol IPCW under a dynamic regime: the book (ch 22.5, p. 319-320) endorses censoring at deviation + g-methods adjustment, but does not give the explicit "numerator conditions only on regime-defining covariate" formula for IPCW; that level of detail is in the 2000 methods papers, not the textbook.

> Edition note (added 2026-10-20): What If quotes in this file were recorded without an edition stamp. Canonical copy for re-verification: the Zotero collection PDF (`~/Zotero/storage/ZNZQPZFC/`, 2025 edition); newest local file is `~/Documents/What if book/hernanrobins_WhatIf_21nov25.pdf`. Technical Point and Fine Point numbering can shift between editions. Re-check the quote and stamp the edition before reusing it.
