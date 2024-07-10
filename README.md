# genderak - Evaluation suite for gender biases in LLMs


`genderak` evaluates all kinds of gender biases in modern LLMs. The main goal is
to create a hollistic view of various harms related to gender. `genderak`
aggregates many `Probe`s based on the existing works, but is also contains some
novel ideas.

## Design philosophy

- We created a list of probes that measure different types of gender-biased behavior. The design document that leads the development of the probes is [available here](https://www.evernote.com/shard/s439/client/snv?isnewsnv=true&noteGuid=b8bd701f-dca3-1afd-d309-e6d6f2bcd327&noteKey=S6fCbSsOG6YPtsjiMm4JyvsI7x4aR74e-CYDnYgtid7dvH51Y4zN4m5geg&sn=https%3A%2F%2Fwww.evernote.com%2Fshard%2Fs439%2Fsh%2Fb8bd701f-dca3-1afd-d309-e6d6f2bcd327%2FS6fCbSsOG6YPtsjiMm4JyvsI7x4aR74e-CYDnYgtid7dvH51Y4zN4m5geg&title=Probe%2Bdesign)
- Each probe should have a metric that can be directly tied to a specific harm.
- The analysis of the results should be based on simple rules. Analyzing outputs with ML models is not recommended.
- If possible, non-binary genders should be considered.

