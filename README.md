Introduction. 

Zipf’s Law of Abbreviation states that frequently used words tend to be shorter. This principle suggests that language is optimized for efficiency, reducing the effort required for communication. Previous research, such as Bentz & Ferrer-i-Cancho (2016), has demonstrated this law across multiple languages and text genres. In this assignment, I test whether Zipf’s Law holds for song lyrics in two different languages: English and Korean. Given that Zipf’s Law has been confirmed in large linguistic datasets, I expect to observe a negative correlation between word length and frequency in both English and Korean lyrics.

Material and Methods.

To conduct this analysis, I extracted the top 100 song titles from the Billboard Hot 100 (for English) and the Melon Chart (for Korean). I used Genius API to retrieve the lyrics for a set of songs from each dataset, 25 songs for English and Korean. 

First, the lyrics were preprocessed by:

•	Removing punctuation and non-alphabetic characters.
•	Tokenizing words using NLTK’s word tokenizer.
•	Filtering out short words (less than two characters) and non-language symbols.
•	Detecting and filtering words that mix English and Korean characters.
•	Detecting and ignoring English words in Korean songs.
•	Removing some words from the Genius Website not related to the lyrics.

For each dataset, I computed:

•	Word frequency: the number of occurrences of each word.
•	Word length: the number of characters in each word.
•	Kendall’s rank correlation coefficient to measure the relationship between frequency and length.

The results were visualized using scatter plots with logarithmic frequency scales to illustrate the expected negative correlation.

Results.

English Lyrics. 

The scatter plot for English lyrics (Fig. 1) reveals a clear trend: shorter words tend to appear more frequently. The most common words, such as pronouns and conjunctions, are also among the shortest. The Kendall correlation coefficient was -0.312, supporting Zipf’s Law. 

Korean Lyrics. 

The results for Korean lyrics (Fig. 2) also show a negative correlation, but the pattern is less pronounced compared to English. The Kendall correlation coefficient was -0.180, indicating a weaker relationship between frequency and word length.

Comparison. 

While Zipf’s Law holds in both languages, the correlation is stronger in English lyrics. This discrepancy may be due to differences in morphological complexity. Korean employs more suffixes and agglutination, which may result in longer words even if they are frequent. For examples: 아름다웠던 - 아름답다 (areumdapda, beautiful) + -었- (past tense marker) + -던 (retrospective modifier), 괜찮아질까 - 괜찮다 (gwaenchanta, to be okay) + -아지다 (-ajida, to become a state) + -ㄹ까 (-kka, question suffix). 

A key difference between English and Korean is that English is an alphabet-based language, while Korean is a syllabic language. Korean words are structured in Hangul blocks, where each block represents a syllable rather than individual letters. This can make frequent Korean words appear longer when analyzed character-by-character, which may weaken the observed correlation in Zipf’s Law. Additionally, Korean’s rich morphological system, with affixes and verb conjugations, further contributes to word length differences."

Conclusion. 

This analysis supports Zipf’s Law of Abbreviation in both English and Korean lyrics, though with varying degrees of correlation. The findings align with previous research suggesting that language efficiency principles apply across genres and linguistic systems. Future studies with larger datasets and alternative tokenization approaches could provide more robust insights into the universality of Zipf’s Law.

References
Bentz, C., & Ferrer-i-Cancho, R. (2016). Zipf’s law of abbreviation as a language universal. Proceedings of the Leiden Workshop on Capturing Phylogenetic Algorithms for Linguistics. University of Tübingen.
