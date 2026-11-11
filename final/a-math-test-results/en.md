A math test was conducted in a class of 30 students. The results were distributed as follows:

- The average score (arithmetic mean) of the test was 75.
- The median test score is 78.
- The standard deviation of the scores is 5.

Later, two more students were added to the results, each of whom received 90 points. Based on the new information, answer the following questions:

1. What is the new average score? Enter a number with an accuracy of two decimal places.
2. After adding two students, the median test score remained 78. The teacher announced that any student whose score exceeds the median by the amount of the new standard deviation will receive special praise. Darkhan, who initially received 78 points, wants to receive this praise. He is allowed to retake the test once to improve his score. What is the minimum score Darkhan should get on retake in order to receive praise? Enter an integer.

The standard deviation is a measure of the spread of data relative to its mean. It shows how much, on average, the elements of a dataset deviate from the mean value.

$$\sigma = \sqrt{\frac{1}{N} \sum_{i=1}^N (x_i - \mu)^2}$$

- $\sigma$ — the standard deviation, a measure of the spread of data relative to its mean.
- $N$ — the total number of elements in the dataset.
- $x_i$ — the $i$-th element of the dataset.
- $\mu$ — the mean of the dataset.

The median is the value that divides an ordered dataset into two equal halves: half of the values are less than or equal to the median, and the other half are greater than or equal to it.

## Output format

Submit a **CSV file** with the header `mean,min_score` and a **single data row**: the new mean (to two decimal places) and Darkhan's minimum retake score (an integer), for example:

```
mean,min_score
75.94,85
```

Scoring is all-or-nothing: you receive the full score only if **both** values are correct — the mean within a small tolerance and the minimum score exactly.
