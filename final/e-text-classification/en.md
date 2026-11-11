<div align="center">
    <img src="./assets/header.png" alt="header.png" border="0" width="700">
</div>

Senior meteorologist Adilkhan works at Kazhydromet in Almaty and is always striving to stay at the forefront of scientific advancements. He follows the latest discoveries in meteorology and shares interesting articles with his colleagues. One day, Adilkhan assigned his intern Darkhan an important task: to analyze scientific articles and news for the meteorological service.

However, Darkhan, in addition to his love for meteorology, was an avid reader of Medium. He spent hours reading, but instead of climate-related articles, he sent materials about football, space, and robots. Adilkhan was shocked when texts about World Cup tournaments and space missions ended up on his desk.

Thinking it over, Adilkhan realized that Darkhan simply didn’t know how to properly classify articles. So, he decided to help his intern and come up with a way to efficiently sort texts using keywords that would clearly indicate the subject of the article.

Text classification using keywords is a important part of modern conversational systems (chatbots, assistants). This method allows us to accurately, and more importantly, reliably determine user intent and correctly guide them through the system’s appropriate response flow.

The task is to create an algorithm that, based on keywords from a dataset of Medium articles, can accurately match each text to its corresponding Tag. The training dataset (`train_set_final.csv`) is provided in `data.zip` (see the **Data** section below).

It contains around 50,000 examples and 95 unique classes/Tags. The file is tab-separated (columns separated by the `\t` symbol) with the columns:

**Title** — the article's title.  
 **Subtitle** — the article's subtitle. (The article text is the Title together with the Subtitle.)  
 **Tags** — the label or class of the text.

Derive your own keyword sets per tag from this data (for example, for the tag “football” the keywords could be: ’Football’, ’league of champions’, ’Cristiano Ronaldo’, ’cr7’, ’world cup’, ’Ballon d’Or’). **Metric / scoring rule:** the percentage (%) of correctly predicted classes/Tags on the hidden dataset.

**Example:**  
 *Text* — Brazil wins the World Cup for the fifth time in Japan and South Korea.  
 *Tag* — football

## General Steps:

1. Analyze texts in the dataset and tokenize them (split by spaces, into n-grams, etc., at your discretion). This converts the text into a set of keywords/phrases/tokens.
2. For each tag/label, create a set of its most important and relevant keywords/phrases/tokens.
3. Create a rule to match text and tag by intersecting their keyword sets (the rule could be based on majority voting, the highest number of matching words, etc.).
4. Using the algorithm from step 3, assign a Tag to each input text in the “hidden” dataset.

## Input

You are given `test.csv` (in `data.zip`) with columns `id` and `text` — one row per article, where `text` is the article's Title and Subtitle. There are $N$ articles ($1 \leq N \leq 10{,}000$). Predict the Tag for each `id`.

## Output format

Submit a CSV file with the columns `id,label` — one row per `id` from `test.csv`, with `label` your predicted Tag (in test order, `id` from `0` to `N-1`):

```
id,label
0,ai
1,football
2,politics
...
```

## Evaluation

Your score is the classification **accuracy** — the percentage of articles whose predicted Tag exactly matches the true Tag.

## Notes

All data is in English, and each article has only one unique Tag.

## Data

[Download data.zip (4.5 MB)](https://contest.faio.kz/problems/01a1c5da-acd8-719a-b0a2-15d0e0d36426/public/data.zip)

```bash
wget https://contest.faio.kz/problems/01a1c5da-acd8-719a-b0a2-15d0e0d36426/public/data.zip
```

The archive contains the training dataset `train_set_final.csv`, the test articles `test.csv` (`id,text`), and `sample_submission.csv` (the submission template).
