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

## LTScore as a library

One can also use this package as a python library:

```py
from ltscore import get_score, get_mistakes

# get the scores
df["scores"] = df.apply(lambda row: get_score(row["text"], language=row["language"]), axis=1)
# returns a list of mistakes for each text
df["mistakes"] = df.apply(lambda row: get_mistakes(row["text"], language=row["language"]), axis=1)
```


