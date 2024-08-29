# genderak - Evaluation suite for gender biases in LLMs


`genderak` evaluates all kinds of gender biases in modern LLMs. The main goal is
to create a hollistic view of various harms related to gender. `genderak`
aggregates many `Probe`s based on the existing works, but is also contains some
novel ideas.

## Implemented probes

### Affective computing

These probes study how the models handle tasks related to affective computing,
i.e., working with emotional state of the user and emotionality in the text.

- `Isear` - We ask the model to act like a gendered persona and describe its
emotion in certain situation. If the model assigns different emotionality
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

### Health

These probes study LLM use-cases in healthcare

- `Dreaddit` measure _outcome disparity_ for stress classification. Texts from
the Dreaddit dataset are augmented with explicit gender indicators. We then
study difference in FNR and FPR. [[Trucan 2019]](https://arxiv.org/pdf/1911.00133) [[Wang 2024]](https://arxiv.org/pdf/2406.12033)

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

- We created a list of probes that measure different types of gender-biased behavior. The design document that leads the development of the probes is [available here](https://www.evernote.com/shard/s439/client/snv?isnewsnv=true&noteGuid=b8bd701f-dca3-1afd-d309-e6d6f2bcd327&noteKey=S6fCbSsOG6YPtsjiMm4JyvsI7x4aR74e-CYDnYgtid7dvH51Y4zN4m5geg&sn=https%3A%2F%2Fwww.evernote.com%2Fshard%2Fs439%2Fsh%2Fb8bd701f-dca3-1afd-d309-e6d6f2bcd327%2FS6fCbSsOG6YPtsjiMm4JyvsI7x4aR74e-CYDnYgtid7dvH51Y4zN4m5geg&title=Probe%2Bdesign)
- Each probe should have a metric that can be directly tied to a specific harm.
- The analysis of the results should be based on simple rules. Analyzing outputs with ML models is not recommended.
- If possible, non-binary genders should be considered.

