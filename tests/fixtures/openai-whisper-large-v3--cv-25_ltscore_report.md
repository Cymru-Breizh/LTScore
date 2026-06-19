# LTScore Report: openai-whisper-large-v3--cv-25.0-2026-03-09-br.jsonl (Breton)

# Part 1: Visualization

![LTScore Distribution](tests/fixtures/openai-whisper-large-v3--cv-25_ltscore_kde_plot.png)

# Part 2: Descriptive Statistics

- Segments:

  - Total number: **3492**

  - Average length: **6.37 tokens**

- Scores:

  - Average: **3.97 mistakes found per 100 tokens**

  - Median: **0.00**

  - Standard Deviation of LTScore: **9.34**

# Part 3: Mistake Categories Analysis

## 3.1 Overview

The table below shows the frequency of each mistake category across the segments in the file.

| Mistake Category | Count | Percentage |
| --- | --- | --- |
| RUMM_KEMMADUR | 364 | 10.42% |
| RUMM_GER_MELL | 283 | 8.10% |
| RUMM_A_BEP_SEURT | 99 | 2.84% |
| RUMM_BARRENNIG_STAGAN | 32 | 0.92% |
| CASING | 14 | 0.40% |
| RUMM_VERB | 11 | 0.32% |
| MISC | 6 | 0.17% |
| RUMM_RANNIG_VERB | 5 | 0.14% |
| RUMM_NIVER | 1 | 0.03% |
## 3.2 Details

The following sections provide examples of the most and least grammatical sentences for each mistake category that appears in more than 1% of the segments, along with their respective LTScore and reference sentence if available.

### 3.2.1 RUMM_KEMMADUR

- Least grammatical sentence containing this category of mistake:
  - LTScore: 100.00
  - Segment: *Pen.*
  - Reference: *pemp*

- Most grammatical sentence containing this category of mistake:
  - LTScore: 5.26
  - Segment: *E vez ya denno diwar-benn an digresko an ink reiz rat bihan apoeus e vez ar reazite merr anez.*
  - Reference: *Evezhiadennou dwb an digreskoù ha n'int ket reizh rak bihan ha pouezus evit ar re a zegemer anezho.*

### 3.2.2 RUMM_GER_MELL

- Least grammatical sentence containing this category of mistake:
  - LTScore: 66.67
  - Segment: *Un an zu.*
  - Reference: *unan zu.*

- Most grammatical sentence containing this category of mistake:
  - LTScore: 5.00
  - Segment: *Eo chezhepañ eo bet strez ken an ko d'an diad-lab o rat a o, evit ar meret a reiz t'roul.*
  - Reference: *E Japan eo bet strizh-kenañ kod an dilhad-labour atav, evit ar merc’hed dreist-holl.*

### 3.2.3 RUMM_A_BEP_SEURT

- Least grammatical sentence containing this category of mistake:
  - LTScore: 40.00
  - Segment: *Blazo eo eo c'hom !*
  - Reference: *Plasoù a chom !*

- Most grammatical sentence containing this category of mistake:
  - LTScore: 5.26
  - Segment: *Ar pepet eo eo eo mont war internet a klask t'eo tout-rout ivez war benn a l'err di bavet.*
  - Reference: *Ar pep aesañ eo mont war internet ha klask titouroù diwar-benn al lec’h dibabet.*

## 3.3 Quartile-based Analyses

Here we sample random segments from the quartiles of two distributions. First, from the length of  the segments (equal-sized chunks), second from the LTScores (value-range cutoffs). 

### 3.3.1 Segments Length Quartiles

This can show errors in the error flagging process. Note that the quartiles are based on equal-sized chunks.

- **Q1 (shortest segments): 873 segments**
  - LTScore: 0.00
  - Segment length: 3 tokens
  - Segment: *Da c'hidokea.*
  - Reference: *Dalc'hit ho ker.*
  - Mistake categories: none

- **Q2 (shorter than the average): 873 segments**
  - LTScore: 0.00
  - Segment length: 5 tokens
  - Segment: *Tormez-vous an abaden !*
  - Reference: *Tomm e vo an abadenn.*
  - Mistake categories: none

- **Q3 (longer than the average): 873 segments**
  - LTScore: 0.00
  - Segment length: 6 tokens
  - Segment: *E gele e rao nour.*
  - Reference: *Digeriñ a ra an nor.*
  - Mistake categories: none

- **Q4 (longest segments): 873 segments**
  - LTScore: 0.00
  - Segment length: 9 tokens
  - Segment: *Peou an deus lec'h e dioc'h ne oa-kemaet.*
  - Reference: *Piv en deus lavaret deoc'h ne oa ket mat ?*
  - Mistake categories: none

### 3.3.2 LTScore Quartiles

This can show what typical segments look like at each level of grammaticality. Note that the quartiles are based on value-range cutoffs (bands of equal width but different sizes) some quartiles may be empty due to the distribution of scores.

- **Q1 (most grammatical): 2779 segments**
  - LTScore: 0.00
  - Segment: *E plet azevet eo ar maezeg e gomz e soaznek.*
  - Reference: *Pelec'h e vefe ur mezeg a gomzfe saozneg ?*
  - Mistake categories: none

- **Q4 (least grammatical): 713 segments**
  - LTScore: 16.67
  - Segment: *ur reioc'hvank e kraez ur ratrez.*
  - Reference: *Ar re yaouank e-kreiz ar raktres !*
  - Mistake categories: CASING

