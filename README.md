# LTScore

Cysill wrapper to score Welsh texts' grammaticality. As it connects to the Cysill API, ensure to have a working internet connexion before using it.

## Installation:
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
ltscore -l br "Kalz a tud a zo amañ!"
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

## LTScore as a library

One can also use this package as a python library:

```py
from ltscore import get_score, get_mistakes

# get the scores
df["scores"] = df.apply(lambda row: get_score(row["text"], language=row["language"]), axis=1)
# returns a list of mistakes for each text
df["mistakes"] = df.apply(lambda row: get_mistakes(row["text"], language=row["language"]), axis=1)
```


