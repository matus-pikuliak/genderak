# genderak - Evaluation suite for gender biases in LLMs


`genderak` is an evaluation suite that comprehensively benchmarks gender biases
in large language models (LLMs). `genderak` aims to identify unfair behavior
with respect to the gender of the user or the gender of people mentioned
in the processed texts. `genderak` consists of many `Probes`, each focused on
different use case, domain, bias, and so on. `genderak` mostly aggregates
existing methodologies, but it also contains original and novel ideas.

## Installation

You can install the package from this repository:

```
pip install git+https://github.com/matus-pikuliak/genderak
```

## Usage

`genderak` can be used to evaluate an arbitrary text generator, i.e., anything
that is able to call `generate(input: str) -> str` method.

### Probes
The basic use case is to evaluate a `generator` with a single probe:

```python
# GestCreative asks model to write a character profile based on a stereotypical
# prompt. Then it analyzes the genders of the generated characters.
from genderak.generators.random_generator import RandomGenerator
from genderak.probes.creative.gest_creative.gest_creative_probe import GestCreativeProbe


generator = RandomGenerator(["He was a punk", "She did ballet"])
probe = GestCreative(template=GestCreativeProbe.templates[0], num_repetitions=10)
probe.run(generator)

>> {
>>      "masculine_rate": 0.5007705894713239,
>>      "stereotype_rate": -0.002398816752873345,
>>      ...
>> }
```

Each probe returns a set of appropriate scores that need to be interpreted. In
this case, the main score is `stereotype_rate` which is close to zero, as we are
randomly generated either a male-coded or a female-coded text.

### Harnesses

To run a comprehensive evaluation, probes are organized into predefined sets
called `harnesses`. A harness returns only the pre-defined metrics that are
deemed important for an experiment. Currently, there is only one harness in the
repository, the `DefaultHarness`:

```python
from genderak.harnesses.default import DefaultHarness

harness = DefaultHarness(calculate_cis=True)
harness.run(generator)

>>> {
>>>     'GestCreativeProbe': {'stereotype_rate': 0.00224880192056498},
>>>     'InventoriesProbe': {'correlation': 0.012060006315442866},
>>>     ...
>>> }
```

## Probes

### Affective computing

These probes study how the models handle tasks related to affective computing,
i.e., working with the emotional state of the user and emotionality in the text.

- `Dreaddit` measure _outcome disparity_ for stress classification. Texts from
the Dreaddit dataset are augmented with explicit gender indicators. We then
study difference in FNR and FPR. [[Trucan 2019]](https://arxiv.org/pdf/1911.00133) [[Wang 2024]](https://arxiv.org/pdf/2406.12033)

- `Isear` - We ask the model to act like a gendered persona and describe its
emotion in certain situations. If the model assigns different emotionality
to certain genders, it is a sign of stereotyping. [[Plaza-del-Arco 2024]](https://arxiv.org/pdf/2403.03121)

### Creative writing

These probes study how the models use stereotypes when they are
prompted to do creative writing.

- `GestCreative` - We ask the model to write a character profile based on a
stereotypical statement (e.g., "I am emotional"). We study whether the gender
of the character matches the stereotypical gender (in this case female). [[Pikuliak 2023]](https://arxiv.org/abs/2311.18711)

- `Inventories` - We ask the model to write a character profile based on a
stereotypical attribute (e.g., emotional). We study whether the gender of the
character matches the stereotypical gender (in this case female). The
inventories are based on social science literature. See `resources/gender_inventories/README.md`
for sources.

- `JobsLum` - We ask the model to write a character profile based on a job. We
study whether the gender of the character matches the stereotypical gender
(E.g., are _nurses_ female). [[Lum 2024]](https://arxiv.org/pdf/2402.12649)

### Decision making

These probes study whether the models discriminate against certain genders
when they are prompted to make a decision about typical life situations.

- `DiscriminationTamkin` is a set of prompts from various life situations
(e.g., hiring, mortgage, publishing) when the model is asked to make a binary
final decision about a person. We study whether the gender changes the result. [[Tamkin 2023]](https://arxiv.org/pdf/2312.03689)

- `HiringAn` is about accepting or refusing job candidates. We study whether
the (gender-coded) name of the candidate changes the result. The jobs are also
gender-coded. [[An 2024]](https://arxiv.org/pdf/2406.10486)

- `HiringBloomberg` is about selecting a resume from a set of similar resumes.
We study whether the model systematically selects male or female resumes as the
top-1 resume. [[Bloomberg]](https://www.bloomberg.com/graphics/2024-openai-gpt-hiring-racial-discrimination/)

### Measuring opinions

These probes study what are the opinions of the models when asked.

- `BBQ` is a dataset of questions that can be solved either logically or
stereotypically. The probe measure how much stereotypical reasoning is used.
[[Parrish 2021]](https://arxiv.org/pdf/2110.08193)

- `Direct` is a set of gender stereotypes (e.g., _women are emotional_) and we 
ask the model whether it agrees or disagrees wit them. [[Sap 2020]](https://aclanthology.org/2020.acl-main.486.pdf) [[Pikuliak 2023]](https://arxiv.org/abs/2311.18711)

- `Gest` is a set of stereotypical statements in the first person, and we ask
the model what gender it assigns to these statements. [[Pikuliak 2023]](https://arxiv.org/abs/2311.18711)


## Design philosophy

- We want to cover as many possibilities of using LLMs as possible.
- Data and methodological _quality_ are of utmost importance. Each data source
is manually evaluated and judged.
- Each probe measures a behavior that can be considered _harmful_ in one way
or another.
- The analysis of the results should be _trustworthy_. Analyzing texts with ML
models is not done until proven reliable enough.
- If possible, non-binary genders should be included.

## Probe design

### Probe anatomy

```                                                                
 ┌─────────┐     ┌─────────────┐     ┌──────────┐     ┌───────────┐ 
 │  Probe  ├─────┤  ProbeItem  ├─────│  Prompt  │─────│  Attempt  │ 
 └─────────┘    *└─────────────┘    *└──────────┘    *└───────────┘ 
```

- Each `Probe` is designed to measure a single well defined behavior of the
evaluated `generator`, e.g., _how does a generator order gender-coded CVs_. The
result of running a probe is a _metric_.
- Each `Probe` measures the behavior by running many `Prompts`. `Prompts` are
specific text inputs that are being fed into the evaluated `generator`.
- Logically related `Prompts` are grouped in `ProbeItems`, e.g., if we have a
multiple-choice question, we might wish to reorder the choices to tackle order
bias that might be present in a model. A single `ProbeItem` would then contain
all the possible reorderings as `Prompts`.
- After we run the generation process, each `Prompt` is populated with one or
more `Attempts`. `Attempts` are the generations being generated by the
`generator` for given `Prompts`.

### Probe lifecycle

Running a probe consists of four phases, as seen in the `Probe.run` method:

1. **Prompt Creation**. The probe is populated with `ProbeItems` and `Prompts`.
All the texts that will be fed into the generator are prepared at this stage,
along with appropriate metadata.
2. **Attempt Generation**. The generator is used to process the `Prompts` and
the generate texts are stored in `Attempts`.
3. **Attempt Evaluation**. The generated texts in `Attempts` are evaluated with
appropriate evaluators. The evaluation is an assessment of the evaluated text,
e.g., was a correct letter selected for a multiple-choice question?
4. **Metric Calculation**. The evaluations in `Attempts` are aggregated to
calculate a final set of metrics for the `Probe`.
