# PlagiarismDetection

Scans all text files in a given directory and compares each one to all others as to find the pairs that are more likely to have copied / plagiariazed text.

Utilizes the [TF-IDF](https://en.wikipedia.org/wiki/Tf%E2%80%93idf) algorithm to handle comparisons between files somewhat intelligently.

Automatically ignores binary / empty files. By default only looks for .txt documents, but can be told to scan all file types anyway.

Used via console, program parameters are determined at runtime and saved to a dedicated settings file. Test files are included in the "Tests" folder.
