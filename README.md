# diorisis
Annotation scripts to generate the Diorisis Ancient Greek Corpus (https://figshare.com/articles/The_Diorisis_Ancient_Greek_Corpus/6187256).

Folder paths are to be configured in [config.ini](config.ini). [TreeTaggerData.zip](TreeTaggerData.zip) and [grkFrm.py.zip](grkFrm.py.zip) need to be extracted into the root folder. TreeTagger must be downloaded and installed independently from [http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/](http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/).

Pipeline:

1. **[tokenizePerseus.py](tokenizePerseus.py)**: tokenizer for [Perseus GitHub](https://github.com/PerseusDL/canonical-greekLit/tree/master/data) corpus files.
2. **[tokenizeConverted.py](tokenizeConverted.py)**: tokenizer for open source corpus files from other collections than Perseus (preliminarily converted into XML files).
3. **[corporaParser.py](corporaParser.py)**: this script annotates the tokenized corpus files (available from https://figshare.com/articles/Diorisis_Corpus_-_Preprocessed_files/7229162).
4. **[TT_corpus_run_and_compare.py](TT_corpus_run_and_compare.py)**: this script runs TreeTagger on annotated corpus data and checks how many tokens with multiple lemma annotation are disambiguable. For each token, TreeTagger may select a POS represented by _n_ lemmata (probability of disambiguation: 1/_n_). In the best case scenario, TreeTagger identifies a POS represented by only one lemma; in the worst case, it will identify a POS not represented by any lemma in the annotated corpus (probability = 0 by default). The script generate statistics for each file in the corpus. Paths are configured in  [config.ini](config.ini).
5.  **[convert_corpus.py](convert_corpus.py)**: this script converts the annotated corpus (created through [corporaParser.py](corporaParser.py)) into a version in which lemmas are disambiguated with TreeTagger (stored in the folder specified under `final_corpus` in [config.ini](config.ini)).
