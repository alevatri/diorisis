# diorisis
Annotation scripts to generate the Diorisis Ancient Greek Corpus (https://figshare.com/articles/The_Diorisis_Ancient_Greek_Corpus/6187256). The preprocessed files these scripts use are available at https://figshare.com/articles/Diorisis_Corpus_-_Preprocessed_files/7229162.

Folder paths are to be configured in [config.ini](config.ini). [TreeTaggerData.zip](TreeTaggerData.zip) and [grkFrm.py.zip](grkFrm.py.zip) need to be extracted into the root folder.

Pipeline:

1. **[corporaParser.py](corporaParser.py)**: this script annotates tokenized corpus files (available from https://figshare.com/articles/Diorisis_Corpus_-_Preprocessed_files/7229162).
2. **[TT_corpus_run_and_compare.py](TT_corpus_run_and_compare.py)**: runs TreeTagger on annotated corpus data and checks how many tokens with multiple lemma annotation are disambiguable. For each token, TreeTagger may select a POS represented by _n_ lemmata (probability of disambiguation: 1/_n_). In the best case scenario, TreeTagger identifies a POS represented by only one lemma; in the worst case, it will identify a POS not represented by any lemma in the annotated corpus (probability = 0 by default). The script generate statistics for each file in the corpus. Paths are configured in  [config.ini](config.ini).
3.  **[convert_corpus.py](convert_corpus.py)**: this script converts the annotated corpus (created through [corporaParser.py](corporaParser.py)) into a version in which lemmas are disambiguated with TreeTagger (stored in the folder specified under `final_corpus` in [config.ini](config.ini)).
