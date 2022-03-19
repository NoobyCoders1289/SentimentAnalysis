
import yake


def get_keywords(text):

    # default extraction
    # kw_extractor = yake.KeywordExtractor()
    # keywords = kw_extractor.extract_keywords(text)

    # for kw in keywords:
    #     print(kw)

    # special extraction
    language = "en"
    max_ngram_size = 3
    deduplication_thresold = 0.9
    deduplication_algo = 'seqm'
    windowSize = 1
    numOfKeywords = 20

    custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_thresold,
                                                dedupFunc=deduplication_algo, windowsSize=windowSize, top=numOfKeywords, features=None)
    keywords = custom_kw_extractor.extract_keywords(text)

    key_words = []
    for kw in keywords:
        key_words.append(kw[0])
    return key_words


sample_posts = df.clean_text[30:41]

sent_corpus = []
for posts in sample_posts:
    post_kw = simple_extractor.extract_keywords(posts)

    sent = ''
    for word, number in post_kw:
        sent += word+" "
    sent_corpus.append(sent)
