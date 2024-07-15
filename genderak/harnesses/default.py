# For now, this just lists existing probes with recommended settings

from genderak.probes.decision_making.discrimination_tamkin.discrimination_tamkin_probe import DiscriminationTamkinProbe
from genderak.probes.decision_making.hiring_an.hiring_an_probe import HiringAnProbe
from genderak.probes.decision_making.hiring_bloomberg.hiring_bloomberg_probe import HiringBloombergProbe
from genderak.probes.gest.gest_probe import GestProbe
from genderak.probes.gest.gest_templates import GestTemplate2


generator = ...

probes = [
    # How much do models agree with gender-role stereotypes
    # https://arxiv.org/abs/2311.18711
    (GestProbe(generator, template=GestTemplate2), ["stereotype_rate"]),

    # How much do models prefer male candidates for hiring
    # How much do models hire according to gender roles
    # https://arxiv.org/pdf/2406.10486
    (HiringAnProbe(generator, sample_k=5000),["average_acceptance_rate_difference", "average_correlation_difference"]),

    # How often do models select male resume from a pile
    # https://www.bloomberg.com/graphics/2024-openai-gpt-hiring-racial-discrimination/
    (HiringBloombergProbe(generator), ['software_engineer_masc_rate', 'hr_specialist_masc_rate', 'retail_masc_rate', 'financial_analyst_masc_rate'])

    # Yes/No decisions making in various situations (e.g., giving loans) for different genders
    # https://arxiv.org/pdf/2312.03689
    (DiscriminationTamkinProbe(generator) ["female_success_rate", "male_success_rate", "nonbinary_success_rate"]),
]

