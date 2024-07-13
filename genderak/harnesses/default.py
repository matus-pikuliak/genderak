# For now, this just lists existing probes with recommended settings

from genderak.probes.decision_making.hiring_an.hiring_an_probe import HiringAnProbe
from genderak.probes.gest.gest_probe import GestProbe
from genderak.probes.gest.gest_templates import GestTemplate2


generator = ...

GestProbe(generator, template=GestTemplate2)

HiringAnProbe(generator, sample_k=1000)