# GPT-5.6 Sol Adversarial Eligibility Audit

## Scope

This is an independent second-model audit of the Gemini 3.7 Flash triage under `PROTOCOL.md`. It is not a new candidate search, not final human screening, and not a substitute for Tommi’s decisions. Flash labels were used only to define the three challenge sets; criterion decisions were made from the preserved ClinicalTrials.gov registry context.

The authoritative candidate universe remains exactly 351 NCT IDs. The audit CSV contains 254 independently audited records: all 120 Flash likely-includes, all 103 Flash human-review records, and 31 targeted Flash obvious-excludes. The other 97 obvious-excludes were not individually adjudicated by Sol and therefore are not represented as audited rows.

## Phase 1 — Flash likely-includes

- Total reviewed: **120**
- `agree_likely_include`: **111**
- `downgrade_human_review`: **2**
- `likely_exclude`: **7**

Every disagreement:

- **NCT03836027 — Fertility Desires and Reproductive Needs of Transgender People** — Flash: `likely_include`; Sol: `likely_exclude`. The fertility survey measures fertility desires and knowledge; GAHT appears only as clinical context, not an intervention, exposure, comparison, monitoring target, or analyzed variable.
- **NCT04077138 — Transgender Youth and PrEP: PK, Safety, Uptake & Adherence - Intervention Development** — Flash: `likely_include`; Sol: `downgrade_human_review`. The registry describes qualitative PrEP-intervention development and points to a separate project's GAHT/PrEP pharmacokinetic phase; it is unclear whether GAHT is analyzed in this record.
- **NCT04077151 — Transgender Youth and PrEP: PK, Safety, Uptake & Adherence - Demonstration Project** — Flash: `likely_include`; Sol: `likely_exclude`. The PrEP demonstration project requires stable cross-sex hormones only as eligibility/background and analyzes PrEP acceptability and adherence, not GAHT.
- **NCT05130086 — A Study of Islatravir (MK-8591) in Trans and Gender Diverse Participants (MK-8591-035)** — Flash: `likely_include`; Sol: `likely_exclude`. The islatravir study uses stable GAHT only as eligibility and reports drug safety and pharmacokinetics without a GAHT comparison or monitoring objective.
- **NCT05925361 — Peritoneum Vaginoplasty; Implementation According to IDEAL Framework** — Flash: `likely_include`; Sol: `likely_exclude`. The registry evaluates peritoneal vaginoplasty feasibility and surgical outcomes; it gives GAHT no explicit research role.
- **NCT06239766 — BC Risk Assessment Before Top Surgery** — Flash: `likely_include`; Sol: `likely_exclude`. The study assesses breast-cancer risk before chest surgery; GAHT is general background rather than an explicit exposure or analytic variable.
- **NCT06428669 — Effect of Nitropaste in Chest Masculinizing Surgery** — Flash: `likely_include`; Sol: `likely_exclude`. The trial evaluates nitropaste after chest surgery and does not give GAHT an intervention, exposure, comparison, monitoring, or analytic role.
- **NCT06530992 — The Effect of Tucking on Semen Quality of Adult Trans Women** — Flash: `likely_include`; Sol: `likely_exclude`. The study evaluates tucking and semen quality before GAHT and excludes ongoing GAHT, so hormone therapy is future context rather than a studied variable.
- **NCT06741319 — Behavioral and Psychosocial Characteristics of Clients Accessing Services at IHRI** — Flash: `likely_include`; Sol: `downgrade_human_review`. The broad HIV and health-services cohort records hormone therapy among many clinical characteristics, but no hormone-specific analysis is stated.

## Phase 2 — Flash human-review queue

- Total reviewed: **103**
- `likely_include`: **17**
- `likely_exclude`: **82**
- `genuinely_ambiguous`: **4**

### Genuinely ambiguous

- **NCT04864951 — HPV Prevalence in Transpersons - a Prospective Study** — `genuinely_ambiguous`. Hormone therapy is collected in the HPV survey, but the registry states HPV-prevalence aims without saying hormone exposure will be analyzed.
- **NCT04944654 — Efficacy, Tolerability and Acceptability of Biktarvy by TPLWH** — `genuinely_ambiguous`. A drug-interaction outcome mentions hormones in TGD participants, but the registry does not identify them as GAHT or specify a hormone analysis.
- **NCT05829928 — Testicular Tissue Cryopreservation in the Setting of Gender-Affirming Therapy** — `genuinely_ambiguous`. Tissue is collected from patients using or planning hormones, but the testicular-tissue objectives do not state a comparison or analysis by GAHT exposure.
- **NCT06656676 — WePrEP: Developing a PrEP Shared Decision-making Tool for Transgender Women** — `genuinely_ambiguous`. The PrEP tool is motivated by GAHT-interaction concerns, but its outcomes evaluate the decision tool without stating that GAHT content or interaction is analyzed.

### Strongly resolved Flash uncertainty

These 99 records are directional Sol resolutions rather than final human decisions:

- **NCT01880489 — Multicomponent Intervention to Reduce Sexual Risk and Substance Use** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT02119377 — First Australian National Trans Mental Health Study** — `likely_include`. Hormone-therapy use, desire, and uptake are explicit survey outcomes in a TGD population.
- **NCT02434562 — Development and Validation of in Vitro Cell-based Bioassays for Nuclear Receptor Activation** — `likely_exclude`. The biobank record describes generic androgen/estrogen bioassays and does not explicitly include a TGD population; GAHT is not a research variable.
- **NCT02985996 — Body Compartment PK for New HIV Pre-exposure Prophylaxis Modalities** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT03060785 — Finding the Right Tenofovir/Emtricitabine Regimen for Pre-Exposure Prophylaxis (PrEP) in Transgender Women** — `likely_include`. PrEP pharmacokinetics are compared in transgender women using feminizing hormones and cisgender men not using hormones.
- **NCT03078829 — The Relation of GnRH Treatment to QTc Interval in Transgender Females** — `likely_exclude`. The TGD study evaluates puberty suppression only and states no explicit estradiol or testosterone GAHT component.
- **NCT03081559 — Improving Engagement in HIV Care for High-risk Women** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT03120936 — The Stay Study: A Demonstration Project Advancing PrEP Delivery in the San Francisco Bay Area Transgender Community** — `likely_include`. The registry explicitly measures effects of PrEP on hormone concentrations and effects of hormone status on PrEP pharmacology.
- **NCT03191474 — Linkage of Transgender Individuals to PrEP** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT03220152 — Implementation of PrEP to HIV in Brazilian Transgender Women** — `likely_include`. FTC/TDF pharmacokinetics are explicitly compared between transgender participants using and not using hormones.
- **NCT03293771 — Transgender Post-reassignment Urogynecologic Measures and Perceptions** — `likely_include`. Postoperative symptoms are explicitly analyzed by hormone-therapy use in the TGD study population.
- **NCT03465852 — HIV Prevention Among Latina Transgender Women Who Have Sex With Men: Evaluation of a Locally Developed Intervention** — `likely_include`. The intervention promotes medically supervised hormone therapy and hormone-therapy uptake is an explicit outcome.
- **NCT03595956 — Transgender Cohort Study of Gender Affirmation and HIV-related Health** — `likely_include`. Medical gender affirmation, defined to include hormones and/or surgery versus neither, is an explicit exposure linked to HIV outcomes.
- **NCT03602222 — An LGBT-Competency Program for Mental Health Professionals in Romania** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT03643120 — Gender Dysphoria Among Adolescents (Norwegian Title: Kjønnsdysfori Blant Ungdom)** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT03789331 — Anogenital Distance Differences Between Transgender Males and Female Individuals** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT03872648 — TransCare - Genital Surgery for Trans Women in Centralized vs. Decentralized Health Care Delivery Settings** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT03899896 — Voice Feminisation in Transgender Women** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT04064671 — ZEPHYR: A Study Evaluating Surgical Outcome After Implantation of the Zephyr ZSI 475 FTM Inflatable Penile Implant in the Neophallus After Female-to-male Sex Reassignment Surgery** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT04096053 — Transgender Education for Affirmative and Competent HIV and Healthcare** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT04160364 — Gender Dysphoria in Children and Adolescents : Parents' Perspectives** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT04195659 — Chest Dysphoria in Transmasculine Spectrum Adolescents** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT04217707 — Transgender Therapeutic Support Groups** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT04265885 — Gender Dysphoria and Transition** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT04290286 — i2TransHealth: Interdisciplinary, Internet-based Trans Health Care** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT04378439 — Appalachian Partnership to Reduce Disparities (Aim 2)** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT04448418 — The Impact of COVID-19 Outbreak on Trans-population's Health in Italy** — `likely_include`. Satisfaction with telemedicine monitoring of hormone treatment is an explicit study outcome.
- **NCT04474366 — The Effect of Pectoral Blocks on Perioperative Pain in Gender Affirmation Top Surgery** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT04478214 — The Strategic Use of Hyaluronic Acid Fillers and Neurotoxin to Influence Gender Perception in Transgender Individuals** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT04482374 — Puberty Suppression and Cardiometabolic Health** — `likely_exclude`. The registry studies GnRH puberty suppression without an explicit estradiol or testosterone GAHT component.
- **NCT04491422 — Same-Day PrEP Initiation and Sexual Health for Transgender Women** — `likely_include`. The registry explicitly studies how feminizing hormone therapy influences PrEP use and adherence.
- **NCT04554849 — Demographic Characteristics and Psychosocial Health of Transgender People** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT04573127 — Gender Dysphoria: Epidemiological Data** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT04708600 — Effectiveness of Speech Therapy in Trans Women.** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT04818580 — Progressive Tension Sutures in Gender Affirming Mastectomy** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT04820088 — Simulated Conversation Training for Mental Healthcare Providers to Improve Care for Transgender and Gender Nonconforming Individuals** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT04867798 — Transgender Men and HIV in Uganda: PrEP Uptake and Persistence** — `likely_include`. Masculinizing hormone use and concerns about hormone-PrEP interactions are explicit variables in the HIV/PrEP project.
- **NCT04935164 — Comparative Study of Gender Identity Disorder Versus Control** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT04979338 — Development of Effective, Opioid Sparing Techniques for Peri-operative Pain Management of Transgender Patients Undergoing Gender Affirming Surgeries** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT04993469 — Patient Reported Outcome on Genital Sensitivity and Sexual Function After Genital Gender Affirming Surgery** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT05016232 — Adaptive Intervention to Facilitate PrEP Uptake/Adherence Among Transgender Women** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT05097820 — Prospective Observational Study on SEBBIN Silicone Gel-filled Testicular Implants** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT05126134 — Psychological Vulnerabilities and Transgender Adolescents: A Descriptive Epidemiology Study** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT05195164 — The Effects of Orchiectomy and Age on Vascular and Metabolic Health in Older Versus Younger Transgender Women** — `likely_include`. Sex-hormone concentrations are explicitly monitored before and after orchiectomy in transgender women using estradiol and spironolactone.
- **NCT05204732 — Acoustic and Perceptual Effects of Intonation Training in Gender Diverse People** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT05273112 — Evaluation of the Variation in Quality of Life During Medical Transition for Transgender People.** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT05292820 — Sexual Function of Trans Women After Vaginoplasty** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT05454579 — The South-East Asian Transgender Health Cohort** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT05534763 — Internet-delivered Treatment for Transgender Individuals With Co-occurring Mental Health Problems** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT05602805 — BariaPSY: the Data Bank** — `likely_exclude`. A broad bariatric cohort offers transgender and nonbinary demographic response options, but does not explicitly define a TGD population or any GAHT research role.
- **NCT05726903 — Counseling Among Gender Diverse Adolescents Who Use Depot Medroxyprogesterone** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT05863676 — Ovarian Tissue Cryopreservation in the Setting of Gender-affirming Therapy** — `likely_include`. The registry explicitly investigates effects of prior hormone therapy on ovarian tissue and follicle measures.
- **NCT05883553 — Epithesis Versus Prosthesis in Post-phalloplasty Transgender Patients.** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT05884307 — Trans Care: An Online Intervention to Reduce Symptoms of Gender Dysphoria** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT05897086 — Polyethylene-glycol Assisted Nerve Repair in Phalloplasty** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT05903911 — Trans Care: An Online Intervention to Reduce Symptoms of Gender Dysphoria** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT05934877 — ASK-PrEP (Assistance Services Knowledge-PrEP)** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT06001307 — Supporting Trans Affirmation, Relationships, and Sex, Phase 3** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT06070324 — Effect of Suture Material on Postoperative Nipple Areolar Complex Widening** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT06074796 — The Determinants of Fertility Preservation in TRANSgender Patients.** — `likely_include`. Prior hormone therapy is an explicit determinant in the fertility-preservation profile analysis.
- **NCT06094257 — Prospective Study of Sensation and Satisfaction in Cancer and Transgender Mastectomy Patients** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT06098781 — Gynaecological Gender-affirming Surgeries** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT06221163 — Sociological Study of the Life Courses of Young TRANSgender Patients** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT06316102 — Promoting Viral Suppression Among Transgender Women Living With HIV in Santo Domingo** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT06390332 — Centering Gender Affirming Resources in Higher Education** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT06400199 — Fertility Preservation for Transfeminine Adolescents Via Semen Cryopreservation or Testicular Sperm Extraction** — `likely_exclude`. The registry is limited to puberty suppression and does not state an estradiol or testosterone GAHT research component.
- **NCT06436560 — Support for Transgender and Non-Binary Individuals Seeking Vaginoplasty Study** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT06439290 — Voice Outcome of Glottoplasty, Cricothyroid Approximation, Thyroplasty, and Chondrolaryngoplasty** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT06443164 — Efficacy of a Chronic Pain Treatment Prior to Gender-affirming Surgery** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT06502353 — Plexaa For Preconditioning: Gender Affirming Mastectomy** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT06565663 — MaPGAS Decision Making** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT06615401 — Understanding Perceived Access and Receipt of Gender-affirming Treatments Among Transgender Veterans** — `likely_include`. Receipt and access to hormone therapy, and their associations with mental-health outcomes, are explicit study aims.
- **NCT06639763 — Erectile Aid Use in Post-phalloplasty and Post-metoidioplasty Transgender Patients** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT06639776 — Sexual Functioning After Erection Prosthesis Placement in Post Phalloplasty Transgender Persons** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT06733415 — Changes in Energy Expenditure (EE) in Transsexuals Undergoing Hormonal Therapy** — `likely_include`. Metabolic rate is measured before and after initiation of gender-affirming hormonal treatment.
- **NCT06844097 — Intervention for Medical Student to Promote Cervical Cancer Screening Among Latinx Transmasculine Individuals** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT06854965 — Cohort Study on Factors Associated with the Evolution of Quality of Life Among Transgender Individuals in the French Population** — `likely_include`. Quality of life is explicitly analyzed with hormone-therapy complications, transition modality, and self-medication variables.
- **NCT06880705 — The Trans-Led Care Study** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT06953908 — The Copenhagen Gender Identity Cohort** — `likely_include`. The registry explicitly evaluates hormone-therapy effects, adverse effects, and treatment courses in a TGD population.
- **NCT06969326 — Topical Estrogen: Brief Intervention to Improve Postoperative Experience for Transgender Men Undergoing Hysterectomy** — `likely_exclude`. Topical estradiol is used for postoperative wound treatment; background testosterone is not an analyzed GAHT variable.
- **NCT07005648 — Brazilian Registry of Menopausal Health** — `likely_exclude`. The study concerns menopausal hormone treatment and excludes hormonal gender reassignment, so the hormone indication is not GAHT.
- **NCT07017595 — Gender-affirming Voice Training With Visual Feedback** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT07075731 — Cervical and Endometrial Cancer Screening in Patients Seeking Gender-Affirming Hysterectomy** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT07085715 — Pan-Viral Screening and Linkage to Care Among GBMSM and Trans Women in Spain** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT07147166 — Evaluating the Efficacy of Force Modulating Tissue Bridge Device in Preventing Hypertrophic Scars Following Gender-Affirming Mastectomy** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT07181551 — Forward to Quit: A Person-centered Mobile Technology Intervention for Smoking Cessation Among Transgender Adults** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT07194226 — Attitudes and Decision Regret Regarding Fertility Preservation in Transgender Individuals** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT07286123 — Gender Affirming Vaginoplasty With Tubularized Augmented Peritoneal Cap (TAPCap) Utilizing Fish Skin Xenograft (Kerecis™)** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT07324967 — A Standardized Counseling Approach to Preoperative Education in Transmasculine Individuals Receiving Gender-affirming Surgery** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT07412509 — Can 3D Modeling Enhance Patient Understanding, Education, and Surgical Outcomes in Gender Affirming Peritoneal Vaginoplasty?** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT07417787 — Point of Care Tests in the Management of Very Early Medical Abortion** — `likely_exclude`. The point-of-care abortion study does not explicitly include a TGD population and does not study GAHT.
- **NCT07480590 — GLOW: Gender-Affirming Care and Mental Health: A Longitudinal Study On Quality of Life, Work Life, and Healthcare Outcomes** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT07509827 — Evaluation of mHealth Intervention to Promote HIV Prevention and Overcome Stigma Among Transgender Women (EMPOW.HER)** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT07512856 — The Implementation of a Trans-tailored Harm Reduction Service for Transgender Persons in Relation to chemsEX and Substance Use (iT-REX)** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT07516691 — Evaluation of a New Strategy to Approach the Transgender Sex Worker Populations and Their Clients for Access to a Preventive Sexual Health System Through the ORTIF Digital Teleconsultation Solution** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT07661823 — QAIAx (AIhealth4U) - AI Public Health Central: Microcity-A (re Quantum AI Agency Aka AI City Hall Project, UPSTO App Nos. 64/074,526, 64/063,557, 63/903,181, 63/729,428** — `likely_exclude`. Gender dysphoria is an explicit target condition, but the AI-managed behavioral intervention has no GAHT research component.
- **NCT07681908 — #TranscendentHealth: A Text Messaging Pregnancy Prevention Program for Transgender Boys** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.
- **NCT07699159 — Cohort Network for Adolescents and Youth With multipLe Mental Health Conditions** — `likely_exclude`. A broad youth mental-health cohort measures gender dysphoria and gender expression, but does not explicitly define a TGD population or study GAHT.
- **NCT07729644 — Evaluation of State-Level Sexual and Gender Minority Laws for the Primary Prevention of Sexual and Intimate Partner Violence Among Sexual and Gender Minority Youth in the U.S.** — `likely_exclude`. The registry explicitly includes a TGD population, but its preserved summary, interventions, eligibility, and outcomes give GAHT no research role; any hormone reference is absent or background.

## Phase 3 — Obvious-exclude audit

- Total Flash obvious-excludes: **128**
- Unique records audited: **31**
- `agree_obvious_exclude`: **31**
- `escalate_human_review`: **0**
- `possible_include`: **0**
- Random sample size: **25**
- Random seed: **20260816**

Selection method:

- **A — TGD terminology:** source-derived search for protocol-defined current and historical TGD terms selected **0** obvious-excludes.
- **B — GAHT terminology:** source-derived search for explicit GAHT, gender-affirming hormone, cross-sex hormone, feminizing/masculinizing hormone, and hormone-transition phrases selected **1** record: `NCT05853120`.
- **C — category risk:** fertility, contraception, HIV/PrEP, surgery, dermatology, reproductive/endocrine treatment, oncology, menopause, and hypogonadism terms were used as risk categories. To avoid treating category membership alone as evidence and rereading nearly the entire non-TGD hormone set at equal depth, category records were selected when they also carried an A/B population-or-GAHT signal. This selected **1** record, `NCT05853120`, overlapping B.
- **D — reproducible random sample:** Python `random.Random(20260816).sample(sorted(remaining_ids), 25)` selected **25** additional records from the 127 obvious-excludes not selected by A–C.
- **Existing-decision consistency check:** all six human-decided obvious-excludes were included; one (`NCT00082082`) overlapped the random sample, adding five unique records.

Targeted A–C record:

- **NCT05853120 — Pharmacokinetics of Doxycycline in Participants Assigned Male at Birth (AMAB) and Participants Assigned Female at Birth (AFAB)** — `agree_obvious_exclude`. The study enrolls assigned-sex cohorts explicitly not using GAHT; it does not include a TGD population or study GAHT.

Random sample:

- `NCT00082082`, `NCT00962637`, `NCT01662466`, `NCT02060474`, `NCT02381821`, `NCT02551367`, `NCT02741154`, `NCT02766803`
- `NCT03230084`, `NCT03516747`, `NCT03528135`, `NCT03593317`, `NCT04107480`, `NCT04586348`, `NCT05019417`, `NCT05244694`
- `NCT05369247`, `NCT05587296`, `NCT05649943`, `NCT05829018`, `NCT06391034`, `NCT06405243`, `NCT06418347`, `NCT06747624`
- `NCT06779331`

Escalated records: **None.**

## Cross-model disagreements

Flash and Sol materially disagree on **108** records: nine Flash likely-includes challenged by Sol, plus 99 Flash human-review records directionally resolved by Sol. The four records retained as genuinely ambiguous are treated as cross-model agreement on uncertainty and appear separately in the MUST REVIEW CAREFULLY queue.

- Sol `downgrade_human_review` (2):
  - `NCT04077138`, `NCT06741319`
- Sol `likely_exclude` (89):
  - `NCT01880489`, `NCT02434562`, `NCT02985996`, `NCT03078829`, `NCT03081559`, `NCT03191474`, `NCT03602222`, `NCT03643120`
  - `NCT03789331`, `NCT03836027`, `NCT03872648`, `NCT03899896`, `NCT04064671`, `NCT04077151`, `NCT04096053`, `NCT04160364`
  - `NCT04195659`, `NCT04217707`, `NCT04265885`, `NCT04290286`, `NCT04378439`, `NCT04474366`, `NCT04478214`, `NCT04482374`
  - `NCT04554849`, `NCT04573127`, `NCT04708600`, `NCT04818580`, `NCT04820088`, `NCT04935164`, `NCT04979338`, `NCT04993469`
  - `NCT05016232`, `NCT05097820`, `NCT05126134`, `NCT05130086`, `NCT05204732`, `NCT05273112`, `NCT05292820`, `NCT05454579`
  - `NCT05534763`, `NCT05602805`, `NCT05726903`, `NCT05883553`, `NCT05884307`, `NCT05897086`, `NCT05903911`, `NCT05925361`
  - `NCT05934877`, `NCT06001307`, `NCT06070324`, `NCT06094257`, `NCT06098781`, `NCT06221163`, `NCT06239766`, `NCT06316102`
  - `NCT06390332`, `NCT06400199`, `NCT06428669`, `NCT06436560`, `NCT06439290`, `NCT06443164`, `NCT06502353`, `NCT06530992`
  - `NCT06565663`, `NCT06639763`, `NCT06639776`, `NCT06844097`, `NCT06880705`, `NCT06969326`, `NCT07005648`, `NCT07017595`
  - `NCT07075731`, `NCT07085715`, `NCT07147166`, `NCT07181551`, `NCT07194226`, `NCT07286123`, `NCT07324967`, `NCT07412509`
  - `NCT07417787`, `NCT07480590`, `NCT07509827`, `NCT07512856`, `NCT07516691`, `NCT07661823`, `NCT07681908`, `NCT07699159`
  - `NCT07729644`
- Sol `likely_include` (17):
  - `NCT02119377`, `NCT03060785`, `NCT03120936`, `NCT03220152`, `NCT03293771`, `NCT03465852`, `NCT03595956`, `NCT04448418`
  - `NCT04491422`, `NCT04867798`, `NCT05195164`, `NCT05863676`, `NCT06074796`, `NCT06615401`, `NCT06733415`, `NCT06854965`
  - `NCT06953908`

## Recommended Tommi review queue

These are workload recommendations, not human screening decisions.

### A. MUST REVIEW CAREFULLY — 112

This queue contains all 108 cross-model disagreements plus four genuinely ambiguous cases; Phase 3 produced no possible false negatives. Unique IDs:

- `NCT01880489`, `NCT02119377`, `NCT02434562`, `NCT02985996`, `NCT03060785`, `NCT03078829`, `NCT03081559`, `NCT03120936`
- `NCT03191474`, `NCT03220152`, `NCT03293771`, `NCT03465852`, `NCT03595956`, `NCT03602222`, `NCT03643120`, `NCT03789331`
- `NCT03836027`, `NCT03872648`, `NCT03899896`, `NCT04064671`, `NCT04077138`, `NCT04077151`, `NCT04096053`, `NCT04160364`
- `NCT04195659`, `NCT04217707`, `NCT04265885`, `NCT04290286`, `NCT04378439`, `NCT04448418`, `NCT04474366`, `NCT04478214`
- `NCT04482374`, `NCT04491422`, `NCT04554849`, `NCT04573127`, `NCT04708600`, `NCT04818580`, `NCT04820088`, `NCT04864951`
- `NCT04867798`, `NCT04935164`, `NCT04944654`, `NCT04979338`, `NCT04993469`, `NCT05016232`, `NCT05097820`, `NCT05126134`
- `NCT05130086`, `NCT05195164`, `NCT05204732`, `NCT05273112`, `NCT05292820`, `NCT05454579`, `NCT05534763`, `NCT05602805`
- `NCT05726903`, `NCT05829928`, `NCT05863676`, `NCT05883553`, `NCT05884307`, `NCT05897086`, `NCT05903911`, `NCT05925361`
- `NCT05934877`, `NCT06001307`, `NCT06070324`, `NCT06074796`, `NCT06094257`, `NCT06098781`, `NCT06221163`, `NCT06239766`
- `NCT06316102`, `NCT06390332`, `NCT06400199`, `NCT06428669`, `NCT06436560`, `NCT06439290`, `NCT06443164`, `NCT06502353`
- `NCT06530992`, `NCT06565663`, `NCT06615401`, `NCT06639763`, `NCT06639776`, `NCT06656676`, `NCT06733415`, `NCT06741319`
- `NCT06844097`, `NCT06854965`, `NCT06880705`, `NCT06953908`, `NCT06969326`, `NCT07005648`, `NCT07017595`, `NCT07075731`
- `NCT07085715`, `NCT07147166`, `NCT07181551`, `NCT07194226`, `NCT07286123`, `NCT07324967`, `NCT07412509`, `NCT07417787`
- `NCT07480590`, `NCT07509827`, `NCT07512856`, `NCT07516691`, `NCT07661823`, `NCT07681908`, `NCT07699159`, `NCT07729644`

### B. RAPID HUMAN CONFIRMATION — 110

Both models support likely inclusion for 111 records. `NCT00146146` already has Tommi’s include decision, leaving 110 pending rapid confirmations:

- `NCT01065220`, `NCT01072825`, `NCT01292785`, `NCT02185274`, `NCT02229617`, `NCT02518009`, `NCT02550431`, `NCT02715232`
- `NCT02983110`, `NCT03270969`, `NCT03557268`, `NCT03620734`, `NCT03637920`, `NCT03651427`, `NCT03652623`, `NCT03725280`
- `NCT03757117`, `NCT03864913`, `NCT04028219`, `NCT04036500`, `NCT04050371`, `NCT04066283`, `NCT04128488`, `NCT04203381`
- `NCT04237467`, `NCT04254354`, `NCT04283656`, `NCT04309760`, `NCT04321551`, `NCT04336891`, `NCT04374708`, `NCT04440722`
- `NCT04478760`, `NCT04482920`, `NCT04508231`, `NCT04515472`, `NCT04524325`, `NCT04531943`, `NCT04534881`, `NCT04551144`
- `NCT04590417`, `NCT04593680`, `NCT04596592`, `NCT04616963`, `NCT04736797`, `NCT04742491`, `NCT04742816`, `NCT04760691`
- `NCT04838249`, `NCT04922424`, `NCT04971447`, `NCT04977765`, `NCT05010707`, `NCT05116293`, `NCT05166083`, `NCT05169762`
- `NCT05175170`, `NCT05318755`, `NCT05334888`, `NCT05387577`, `NCT05428215`, `NCT05442463`, `NCT05469204`, `NCT05487794`
- `NCT05489159`, `NCT05583058`, `NCT05587751`, `NCT05607303`, `NCT05649605`, `NCT05663892`, `NCT05787470`, `NCT05865262`
- `NCT05891795`, `NCT06005610`, `NCT06022562`, `NCT06083766`, `NCT06116201`, `NCT06149065`, `NCT06230770`, `NCT06234488`
- `NCT06245681`, `NCT06247267`, `NCT06291675`, `NCT06351501`, `NCT06357130`, `NCT06450405`, `NCT06470906`, `NCT06482385`
- `NCT06487754`, `NCT06573177`, `NCT06670053`, `NCT06710496`, `NCT06774053`, `NCT06807580`, `NCT06816355`, `NCT06939257`
- `NCT06987045`, `NCT07092527`, `NCT07128771`, `NCT07145281`, `NCT07148921`, `NCT07187947`, `NCT07252687`, `NCT07358897`
- `NCT07394400`, `NCT07400419`, `NCT07481942`, `NCT07542964`, `NCT07624747`, `NCT07746999`

### C. LOW-PRIORITY QC — 25

Both models strongly support exclusion for 31 audited obvious-excludes. Six already have Tommi’s exclude decision, leaving 25 pending low-priority QC records:

- `NCT00962637`, `NCT01662466`, `NCT02060474`, `NCT02381821`, `NCT02551367`, `NCT02741154`, `NCT02766803`, `NCT03230084`
- `NCT03516747`, `NCT03528135`, `NCT03593317`, `NCT04107480`, `NCT04586348`, `NCT05019417`, `NCT05244694`, `NCT05369247`
- `NCT05587296`, `NCT05649943`, `NCT05829018`, `NCT05853120`, `NCT06391034`, `NCT06405243`, `NCT06418347`, `NCT06747624`
- `NCT06779331`

## Existing human decisions

All seven existing human decisions remain unchanged and are methodologically concordant with this audit. None appears inconsistent with `PROTOCOL.md`.

| NCT ID | Existing human decision | Sol consistency audit |
|---|---:|---|
| NCT00023543 | `exclude` | `agree_obvious_exclude` |
| NCT00082082 | `exclude` | `agree_obvious_exclude` |
| NCT00146146 | `include` | `agree_likely_include` |
| NCT00188708 | `exclude` | `agree_obvious_exclude` |
| NCT00450749 | `exclude` | `agree_obvious_exclude` |
| NCT00544882 | `exclude` | `agree_obvious_exclude` |
| NCT00608400 | `exclude` | `agree_obvious_exclude` |

## Validation

- The candidate IDs in `data/ai_triage.csv` and `data/screening_review.csv` are identical: **351 unique NCT IDs**.
- All 120 Flash likely-includes and all 103 Flash human-review records are present in the audit CSV.
- Phase 3 includes 31 unique audited obvious-excludes and documents the selector, overlap, sample size, and seed.
- Every audited row has a nonblank `sol_reason`.
- The seven existing human decisions are copied unchanged into the audit output.
- SHA-256 checks confirm `PROTOCOL.md`, `data/screening_review.csv`, `data/ai_triage.csv`, `data/ai_triage_report.md`, and the three preserved enrichment/provenance files are unchanged from the pre-audit baseline.
- No web retrieval, charting, descriptive analysis, commit, or push was performed.
