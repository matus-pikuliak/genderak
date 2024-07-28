# For now, this just lists existing probes with recommended settings

from genderak.probes.creative.gest_creative.gest_creative_probe import GestCreativeProbe
from genderak.probes.creative.inventories.inventories_probe import InventoriesProbe
from genderak.probes.creative.jobs_lum.jobs_lum_probe import JobsLumProbe
from genderak.probes.decision_making.discrimination_tamkin.discrimination_tamkin_probe import DiscriminationTamkinProbe
from genderak.probes.decision_making.hiring_an.hiring_an_probe import HiringAnProbe
from genderak.probes.decision_making.hiring_bloomberg.hiring_bloomberg_probe import HiringBloombergProbe
from genderak.probes.health.dreaddit.dreaddit_probe import DreadditProbe
from genderak.probes.opinion.direct.direct_probe import DirectProbe
from genderak.probes.opinion.gest.gest_probe import GestProbe
from genderak.probes.opinion.gest.gest_templates import GestTemplate2


generator = ...

probes = [

    # ===
    # CREATIVE
    # ===

    # Do models use stereotypes when they are prompted to write about jobs?
    # https://arxiv.org/pdf/2402.12649
    (JobsLumProbe(generator, template=JobsLumProbe.templates[2]), ["correlation"]),


    # Do models use stereotypes when they are prompted to write characters
    # based on stereotypical first-person statements (e.g., "I am emotional").
    # Note: Recommended max_token >= 300
    # https://arxiv.org/abs/2311.18711
    (GestCreativeProbe(generator, template=GestCreativeProbe.templates[0]), ["stereotype_rate"]),


    # Do models use stereotypes when they are prompted to write characters
    # based on stereotypical attributes (e.g., emotional).
    # Note: Recommended max_token >= 300
    # This is an original work, but the attributes are based on existing
    # inventories extacted from various gender-studies papers.
    (InventoriesProbe(generator, template=InventoriesProbe.templates[0]), ["correlation"]),

    # ===
    # MEASURING OPINIONS
    # ===

    # How much do models agree with gender-role stereotypes
    # https://arxiv.org/abs/2311.18711
    (GestProbe(generator, template=GestTemplate2), ["stereotype_rate"]),

    # Does the model agree with stereotypical statements about genders?
    # https://aclanthology.org/2020.acl-main.486.pdf
    # https://arxiv.org/pdf/2311.18711 
    (DirectProbe(generator), ["stereotype_rate"], ["sbic_fail_rate", "gest_fail_rate"]),

    # ===
    # DECISION MAKING
    # ===

    # How much do models prefer male candidates for hiring
    # How much do models hire according to gender roles
    # https://arxiv.org/pdf/2406.10486
    (HiringAnProbe(generator, sample_k=5000), ["average_acceptance_rate_difference", "average_correlation_difference"]),

    # How often do models select male resume from a pile
    # https://www.bloomberg.com/graphics/2024-openai-gpt-hiring-racial-discrimination/
    (HiringBloombergProbe(generator), ['software_engineer_masc_rate', 'hr_specialist_masc_rate', 'retail_masc_rate', 'financial_analyst_masc_rate'])

    # Yes/No decisions making in various situations (e.g., giving loans) for
    # different genders
    # https://arxiv.org/pdf/2312.03689
    (DiscriminationTamkinProbe(generator), ["female_success_rate", "male_success_rate", "nonbinary_success_rate"]),

    # ===
    # HEALTH
    # ===

    # Error disparity when the model detects "stress" in texts. Author's gender
    # is explicitly mentioned in the prompt
    # Dreaddit dataset: https://arxiv.org/abs/1911.00133
    # LLM evaluation: https://arxiv.org/abs/2406.12033
    (DreadditProbe(generator), ["max_diff_tpr", "max_diff_tnr"]),

]

