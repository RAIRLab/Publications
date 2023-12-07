To add new sections for future years...
  Copy the LaTeX code given below into the body of main.tex
  Create <year>.bib, add citations in order you want them to appear
  Run "make" in the publication_list directory
```tex
  \begin{refsection}[<year>.bib]
    \nocite{*}
    \printbibliography[title=<year>, heading=bibliography]
  \end{refsection}
```