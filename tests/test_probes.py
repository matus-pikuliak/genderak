from genderak.generators.random_generator import RandomGenerator
from genderak.probes.affective.isear.isear_probe import IsearProbe
from genderak.probes.creative.gest_creative.gest_creative_probe import \
    GestCreativeProbe
from genderak.probes.creative.inventories.inventories_probe import \
    InventoriesProbe
from genderak.probes.creative.jobs_lum.jobs_lum_probe import JobsLumProbe
from genderak.probes.decision_making.discrimination_tamkin.discrimination_tamkin_probe import \
    DiscriminationTamkinProbe
from genderak.probes.decision_making.hiring_an.hiring_an_probe import \
    HiringAnProbe
from genderak.probes.decision_making.hiring_bloomberg.hiring_bloomberg_probe import \
    HiringBloombergProbe
from genderak.probes.health.dreaddit.dreaddit_probe import DreadditProbe
from genderak.probes.opinion.bbq.bbq_probe import BbqProbe
from genderak.probes.opinion.direct.direct_probe import DirectProbe
from genderak.probes.opinion.gest.gest_probe import GestProbe
from genderak.probes.opinion.gest.gest_templates import GestTemplate1


def test_isear():
    probe = IsearProbe()
    generator = RandomGenerator(probe.emotions)
    probe.run(generator)
    print(probe.__class__, probe.metrics, end="\n\n")
    assert abs(probe.metrics["max_diff"]) < 0.03


def test_gest_creative():
    generator = RandomGenerator(["she", "he", "..."])
    probe = GestCreativeProbe(
        template=GestCreativeProbe.templates[0], num_repetitions=10
    )
    probe.run(generator)
    print(probe.__class__, probe.metrics, end="\n\n")
    assert abs(probe.metrics["stereotype_rate"]) < 0.03
    assert abs(probe.metrics["masculine_rate"] - 1 / 2) < 0.03


def test_inventories():
    generator = RandomGenerator(["she", "he", "..."])
    probe = InventoriesProbe(
        template=InventoriesProbe.templates[0], num_repetitions=100
    )
    probe.run(generator)
    print(probe.__class__, probe.metrics, end="\n\n")
    assert abs(probe.metrics["correlation"]) < 0.05
    assert abs(probe.metrics["masculine_rate"] - 1 / 2) < 0.03


def test_jobs_lum():
    generator = RandomGenerator(["she", "he", "..."])
    probe = JobsLumProbe(template=JobsLumProbe.templates[0], num_repetitions=100)
    probe.run(generator)
    print(probe.__class__, probe.metrics, end="\n\n")
    assert abs(probe.metrics["correlation"]) < 0.03
    assert abs(probe.metrics["masculine_rate"] - 1 / 2) < 0.03


def test_discrimination_tamkin():
    generator = RandomGenerator(["yes", "no", "..."])
    probe = DiscriminationTamkinProbe()
    probe.run(generator)
    print(probe.__class__, probe.metrics, end="\n\n")
    assert abs(probe.metrics["female_success_rate"] - 1 / 2) < 0.03
    assert abs(probe.metrics["male_success_rate"] - 1 / 2) < 0.03
    assert abs(probe.metrics["nonbinary_success_rate"] - 1 / 2) < 0.03


def test_hiring_an():
    generator = RandomGenerator(
        ["regret to inform you", "you have been selected", "..."]
    )
    probe = HiringAnProbe(sample_k=20_000)
    probe.run(generator)
    print(probe.__class__, probe.metrics, end="\n\n")
    assert abs(probe.metrics["average_acceptance_rate_difference"]) < 0.03
    assert abs(probe.metrics["average_correlation_difference"]) < 0.03


def test_hiring_bloomberg():
    generator = RandomGenerator(["A", "B", "..."])
    probe = HiringBloombergProbe()
    probe.names = {
        "MALE": {"ASIAN": ["A", "A", "A", "A"]},
        "FEMALE": {"ASIAN": ["B", "B", "B", "B"]},
    }
    probe.races = ["ASIAN"]
    probe.run(generator)
    print(probe.__class__, probe.metrics, end="\n\n")
    assert abs(probe.metrics["software_engineer_asian_masc_rate"] - 0.5) < 0.03


def test_dreaddit():
    generator = RandomGenerator(["yes", "no", "..."])
    probe = DreadditProbe(num_repetitions=5)
    probe.run(generator)
    print(probe.__class__, probe.metrics, end="\n\n")
    assert abs(probe.metrics["max_diff_tpr"]) < 0.03
    assert abs(probe.metrics["max_diff_tnr"]) < 0.03


def test_bbq():
    generator = RandomGenerator(["(a)", "(b)", "(c)", "..."])
    probe = BbqProbe()
    probe.run(generator)
    print(probe.__class__, probe.metrics, end="\n\n")
    assert abs(probe.metrics["stereotypical_rate"] - 1 / 3) < 0.03
    assert abs(probe.metrics["logical_rate"] - 1 / 3) < 0.03


def test_direct():
    generator = RandomGenerator(["yes", "no", "..."])
    probe = DirectProbe(num_repetitions=10)
    probe.run(generator)
    print(probe.__class__, probe.metrics, end="\n\n")
    assert abs(probe.metrics["sbic_fail_rate"] - 1 / 2) < 0.03


def test_gest():
    generator = RandomGenerator(["(a)", "(b)", "(c)", "..."])
    probe = GestProbe(template=GestTemplate1)
    probe.run(generator)
    print(probe.__class__, probe.metrics, end="\n\n")
    assert abs(probe.metrics["stereotype_rate"]) < 0.03
    assert abs(probe.metrics["frequency_male_option"] - 1 / 4) < 0.03
