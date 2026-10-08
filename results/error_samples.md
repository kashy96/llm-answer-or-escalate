# Confident errors for manual review

Highest-confidence wrong answers per model and condition. Read each one and note
why it went wrong (see the categories in the README).

## gemini-flash / closed_book

- **20538207**: Should temperature be monitorized during kidney allograft preservation?
  - label `no`, model `yes` at 100% confidence
  - category: plausible prior
- **19578820**: Are opioid dependence and methadone maintenance treatment (MMT) documented in the medical record?
  - label `maybe`, model `yes` at 100% confidence
  - category: maybe confusion
- **9044116**: Biliary atresia: should all patients undergo a portoenterostomy?
  - label `no`, model `yes` at 95% confidence
  - category: plausible prior
- **19198736**: Is being small for gestational age a risk factor for retinopathy of prematurity?
  - label `no`, model `yes` at 95% confidence
  - category: plausible prior
- **21789019**: Do elderly cancer patients have different care needs compared with younger ones?
  - label `no`, model `yes` at 95% confidence
  - category: plausible prior
- **25394614**: Does timing of initial surfactant treatment make a difference in rates of chronic lung disease or mortality in premature infants?
  - label `maybe`, model `yes` at 95% confidence
  - category: maybe confusion
- **18784527**: Can mandibular depiction be improved by changing the thickness of double-oblique computed tomography images?
  - label `no`, model `yes` at 95% confidence
  - category: plausible prior
- **12626177**: Can the Internet be used to improve sexual health awareness in web-wise young people?
  - label `maybe`, model `yes` at 95% confidence
  - category: label disagreement
- **23356465**: Uniformity of evidence-based treatments in practice?
  - label `yes`, model `no` at 95% confidence
  - category: label disagreement
- **16564683**: Is there any interest to perform ultrasonography in boys with undescended testis?
  - label `no`, model `yes` at 95% confidence
  - category: plausible prior

## gemini-flash / gold_context

- **19694846**: Does self-efficacy mediate the relationship between transformational leadership behaviours and healthcare workers' sleep quality?
  - label `maybe`, model `no` at 100% confidence
  - category: label disagreement
- **16735905**: Does the severity of obstructive sleep apnea predict patients requiring high continuous positive airway pressure?
  - label `maybe`, model `yes` at 100% confidence
  - category: maybe confusion
- **17578985**: Parasacral sciatic nerve block: does the elicited motor response predict the success rate?
  - label `maybe`, model `yes` at 100% confidence
  - category: label disagreement
- **26864326**: Predicting admission at triage: are nurses better than a simple objective score?
  - label `yes`, model `no` at 95% confidence
  - category: label disagreement
- **22211919**: Actinobaculum schaalii, a cause of urinary tract infections in children?
  - label `maybe`, model `yes` at 95% confidence
  - category: maybe confusion
- **17565137**: Out of the smokescreen II: will an advertisement targeting the tobacco industry affect young people's perception of smoking in movies and their intention to smoke?
  - label `yes`, model `maybe` at 90% confidence
  - category: maybe confusion
- **23356465**: Uniformity of evidence-based treatments in practice?
  - label `yes`, model `no` at 90% confidence
  - category: label disagreement
- **22617083**: Does age moderate the effect of personality disorder on coping style in psychiatric inpatients?
  - label `yes`, model `no` at 90% confidence
  - category: misread evidence
- **15787677**: Does aerobic fitness influence microvascular function in healthy adults at risk of developing Type 2 diabetes?
  - label `maybe`, model `yes` at 90% confidence
  - category: maybe confusion
- **24591144**: Are the elderly with oropharyngeal carcinoma undertreated?
  - label `maybe`, model `yes` at 90% confidence
  - category: maybe confusion

## gemini-flash / retrieved

- **19694846**: Does self-efficacy mediate the relationship between transformational leadership behaviours and healthcare workers' sleep quality?
  - label `maybe`, model `no` at 100% confidence
  - category: label disagreement
- **23356465**: Uniformity of evidence-based treatments in practice?
  - label `yes`, model `no` at 95% confidence
  - category: label disagreement
- **22211919**: Actinobaculum schaalii, a cause of urinary tract infections in children?
  - label `maybe`, model `yes` at 95% confidence
  - category: maybe confusion
- **17578985**: Parasacral sciatic nerve block: does the elicited motor response predict the success rate?
  - label `maybe`, model `yes` at 95% confidence
  - category: label disagreement
- **22617083**: Does age moderate the effect of personality disorder on coping style in psychiatric inpatients?
  - label `yes`, model `no` at 90% confidence
  - category: misread evidence
- **18784527**: Can mandibular depiction be improved by changing the thickness of double-oblique computed tomography images?
  - label `no`, model `yes` at 90% confidence
  - category: misread evidence
- **21789019**: Do elderly cancer patients have different care needs compared with younger ones?
  - label `no`, model `yes` at 90% confidence
  - category: misread evidence
- **20538207**: Should temperature be monitorized during kidney allograft preservation?
  - label `no`, model `yes` at 90% confidence
  - category: misread evidence
- **19712912**: Has the 80-hour workweek improved surgical resident education in New England?
  - label `no`, model `maybe` at 90% confidence
  - category: maybe confusion
- **28011794**: Can Ambu self-inflating bag and Neopuff infant resuscitator provide adequate and safe manual inflations for infants up to 10 kg weight?
  - label `maybe`, model `no` at 90% confidence
  - category: maybe confusion

## qwen2.5-3b / closed_book

- **24901580**: Is scintigraphy a guideline method in determining amputation levels in diabetic foot?
  - label `yes`, model `no` at 100% confidence
  - category: plausible prior
- **22453060**: Does a 4 diagram manual enable laypersons to operate the Laryngeal Mask Supreme®?
  - label `yes`, model `no` at 100% confidence
  - category: plausible prior
- **9044116**: Biliary atresia: should all patients undergo a portoenterostomy?
  - label `no`, model `maybe` at 70% confidence
  - category: maybe confusion
- **20577124**: Is leptin involved in phagocytic NADPH oxidase overactivity in obesity?
  - label `yes`, model `maybe` at 60% confidence
  - category: maybe confusion
- **25501465**: Evaluation of pediatric VCUG at an academic children's hospital: is the radiographic scout image necessary?
  - label `no`, model `maybe` at 60% confidence
  - category: maybe confusion
- **19575307**: Does glomerular hyperfiltration in pregnancy damage the kidney in women with more parities?
  - label `no`, model `maybe` at 60% confidence
  - category: maybe confusion
- **12855939**: Is ankle/arm pressure predictive for cardiovascular mortality in older patients living in nursing homes?
  - label `no`, model `maybe` at 60% confidence
  - category: maybe confusion
- **9100537**: Can nonproliferative breast disease and proliferative breast disease without atypia be distinguished by fine-needle aspiration cytology?
  - label `no`, model `maybe` at 60% confidence
  - category: maybe confusion
- **21881325**: Do preoperative statins reduce atrial fibrillation after coronary artery bypass grafting?
  - label `yes`, model `maybe` at 60% confidence
  - category: maybe confusion
- **24172579**: Does sex influence the response to intravenous thrombolysis in ischemic stroke?
  - label `yes`, model `maybe` at 60% confidence
  - category: maybe confusion

## qwen2.5-3b / gold_context

- **19694846**: Does self-efficacy mediate the relationship between transformational leadership behaviours and healthcare workers' sleep quality?
  - label `maybe`, model `no` at 100% confidence
  - category: label disagreement
- **17565137**: Out of the smokescreen II: will an advertisement targeting the tobacco industry affect young people's perception of smoking in movies and their intention to smoke?
  - label `yes`, model `no` at 100% confidence
  - category: misread evidence
- **24901580**: Is scintigraphy a guideline method in determining amputation levels in diabetic foot?
  - label `yes`, model `no` at 100% confidence
  - category: label disagreement
- **22849512**: Are neighbourhood social capital and availability of sports facilities related to sports participation among Dutch adolescents?
  - label `maybe`, model `no` at 100% confidence
  - category: maybe confusion
- **11458136**: Does managed care enable more low income persons to identify a usual source of care?
  - label `maybe`, model `no` at 95% confidence
  - category: maybe confusion
- **7547656**: Does continuous intravenous infusion of low-concentration epinephrine impair uterine blood flow in pregnant ewes?
  - label `no`, model `yes` at 95% confidence
  - category: misread evidence
- **15539888**: Is the atopy patch test with house dust mites specific for atopic dermatitis?
  - label `yes`, model `no` at 90% confidence
  - category: misread evidence
- **23149821**: Should HIV-infected patients be screened for silent myocardial ischaemia using gated myocardial perfusion SPECT?
  - label `maybe`, model `yes` at 85% confidence
  - category: maybe confusion
- **17489316**: Is tumour expression of VEGF associated with venous invasion and survival in pT3 renal cell carcinoma?
  - label `maybe`, model `yes` at 85% confidence
  - category: maybe confusion
- **16735905**: Does the severity of obstructive sleep apnea predict patients requiring high continuous positive airway pressure?
  - label `maybe`, model `yes` at 85% confidence
  - category: maybe confusion

## qwen2.5-3b / retrieved

- **17565137**: Out of the smokescreen II: will an advertisement targeting the tobacco industry affect young people's perception of smoking in movies and their intention to smoke?
  - label `yes`, model `no` at 100% confidence
  - category: misread evidence
- **17598882**: Is breast cancer prognosis inherited?
  - label `yes`, model `no` at 100% confidence
  - category: wrong evidence
- **21689015**: Can dogs prime autistic children for therapy?
  - label `yes`, model `no` at 100% confidence
  - category: wrong evidence
- **17682349**: Are there gender differences in the reasons why African Americans delay in seeking medical help for symptoms of an acute myocardial infarction?
  - label `yes`, model `no` at 100% confidence
  - category: label disagreement
- **24901580**: Is scintigraphy a guideline method in determining amputation levels in diabetic foot?
  - label `yes`, model `no` at 100% confidence
  - category: label disagreement
- **22849512**: Are neighbourhood social capital and availability of sports facilities related to sports participation among Dutch adolescents?
  - label `maybe`, model `no` at 90% confidence
  - category: maybe confusion
- **22302658**: Does limb-salvage surgery offer patients better quality of life and functional capacity than amputation?
  - label `maybe`, model `yes` at 85% confidence
  - category: maybe confusion
- **26784147**: Target Serum Urate: Do Gout Patients Know Their Goal?
  - label `no`, model `yes` at 85% confidence
  - category: misread evidence
- **19130332**: Is the zeolite hemostatic agent beneficial in reducing blood loss during arterial injury?
  - label `yes`, model `no` at 85% confidence
  - category: misread evidence
- **25394614**: Does timing of initial surfactant treatment make a difference in rates of chronic lung disease or mortality in premature infants?
  - label `maybe`, model `yes` at 85% confidence
  - category: maybe confusion
