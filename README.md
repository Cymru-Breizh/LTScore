# LTScore

LanguageTool wrapper for multilingual grammaticality assessment. For Welsh, it uses [CySgor](https://pypi.org/project/cysgor/), which is based on the Cysill grammar checker, but works with the same principles as LTScore.

## Utility
In low resource languages settings, LTScore can be used as a tool to evaluate the grammaticality of generated text, such as machine translation outputs or conversational AIs. From this, it can be used to filter through training corpora (like sorting legit content from cheap autotranslated websites in fineweb), and improve training data quality, or to evaluate the outputs of a model during training or inference when other methods are not available or satisfactory.

## Languages supported
LTScore supports the following languages:
- ar: Arabic
- ast: Asturian
- be: Belarusian
- br: Breton
- ca: Catalan
- crh: Crimean Tatar
- cy: Welsh
- da: Danish
- de: German
- el: Greek
- en: English
- eo: Esperanto
- es: Spanish
- fa: Persian
- fr: French
- ga: Irish
- gl: Galician
- it: Italian
- ja: Japanese
- km: Khmer
- nl: Dutch
- pl: Polish
- pt: Portuguese
- ro: Romanian
- ru: Russian
- sk: Slovak
- sl: Slovenian
- sv: Swedish
- ta: Tamil
- tl: Tagalog
- uk: Ukrainian
- zh: Chinese

## Installation
```sh
pip install ltscore
```

### Run the Docker image locally
You can download the LanguageTool image from Docker Hub, then using the port `8010` as indicated below.

```sh
docker pull erikvl87/languagetool
docker run --rm -p 8010:8010 erikvl87/languagetool
```

For more details about the Docker container's configuration, see [this link](https://hub.docker.com/r/erikvl87/languagetool).

## LTScore as a CLI
There are two ways to use the CLI, either by entering a text file's path, or directly a text. The CLI returns a string of numbers representing the grammaticality score of the text.

```sh
# With a text as a positional character
ltscore -l br "Kalz dud a zo amañ!"
```

```sh
# With a -p or --path flag
ltscore -l br -p ./src/ltscore/assets/text-sample-br.txt 
```

or alternatively with the pipe operator:

```sh
cat src/ltscore/assets/text-sample-br.txt | ltscore -l br
```

## JSON file processing
LTScore can also process some files for short analysis.

### Adding LTScore to an existing file
Given a file `data.ndjson` with the following content:

```
{"source": "'Mañ an dud o tont.", "target": "Les gens arrivent.", "prediction": "Les gens vient."}
{"source": "Un devezh dilabour eo Lun Fask.", "target": "Le lundi de Pâques est un jour férié.", "prediction": "Le lundi de Pâques ai un jours fériée."}
```

running `ltscore -t prediction -l fr -p data.ndjson` and will get the file updated in the following way:

```
{"source":"'Mañ an dud o tont.","target":"Les gens arrivent.","prediction":"Les gens vient.","ltscore":33.333333333333336,"mistakes_categories":["CAT_GRAMMAIRE"]}
{"source":"Un devezh dilabour eo Lun Fask.","target":"Le lundi de Pâques est un jour férié.","prediction":"Le lundi de Pâques ai un jours fériée.","ltscore":25.0,"mistakes_categories":["CAT_HOMONYMES_PARONYMES","AGREEMENT"]}
```

### Generating a report
Adding the `-r` or `--report` flag will generate a markdown report with a KDE plot of the LTScore distribution, descriptive statistics, and an analysis of sentences based on the mistake categories. The report will be saved in the same directory as the input file with the name `ltscore_report.md`.
To use it on the file available in `src/tests/fixtures/text-sample-br.ndjson`, which analyzes a breton texts, you would run:

```sh
ltscore -rt prediction -l br -p tests/fixtures/openai-whisper-large-v3--cv-25.0-2026-03-09-br.jsonl
```

You would then get a report in the same directory as the input file with the ending `ltscore_report.md` containing a KDE plot of the LTScore distribution, descriptive statistics, and an analysis of sentences based on the mistake categories.

## LTScore as a library

One can also use this package as a python library:

```py
from ltscore import get_score, get_mistakes

# get the scores
df["scores"] = df.apply(lambda row: get_score(row["text"], language=row["language"]), axis=1)
# returns a list of mistakes for each text
df["mistakes"] = df.apply(lambda row: get_mistakes(row["text"], language=row["language"]), axis=1)
```


