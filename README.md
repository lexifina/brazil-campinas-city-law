# Campinas (city): law history in git

Part of [lexifina/global-law](https://github.com/lexifina/global-law), one git history for every country's law: this is the law of Campinas, São Paulo, Brazil, which global-law reads at `brazil/sao-paulo/campinas/acts/`.

The municipal law of the Município de Campinas, São Paulo (Brazil) as a git history: one file per Artigo, one paragraph per line, so `git blame`, `git log` and `git diff` work line by line. The text is Portuguese, the only official language.

It follows the shared design of [lexifina/global-law](https://github.com/lexifina/global-law).

## What this repository holds

| Folder | Act | Versions |
| --- | --- | ---: |
| `lei-organica/` | Lei Orgânica do Município de Campinas, de 30 de março de 1990 | 1 (text in force as compiled) |
| `lei-*/`, `lc-*/` | Municipal laws (Leis and Leis Complementares), newest first | one each, as enacted (364) |

**The Lei Orgânica.** The Lei Orgânica is given only as the Câmara's compiled edition ("Atualizada até a Emenda nº 55, de 6 de maio de 2025"), from the PDF its SAPL holds, dated 6 May 2025 and committed as the publisher's text (the oldest version available). The text as promulgated on 30 March 1990 and the wordings the amendments replaced are not reconstructed.

**Municipal laws, newest first.** Each law the Câmara's SAPL lists with a PDF that has a text layer of its own, as enacted, credited to itself. Laws are added in parts, working back in time; later amendments by other laws are not worked into earlier laws. Scans and laws that take effect on another day than their publication are left out.

State law is in [brazil-sao-paulo-law](https://github.com/lexifina/brazil-sao-paulo-law); federal law is in [brazil-law](https://github.com/lexifina/brazil-law).

## Source

[Câmara Municipal de Campinas, SAPL](https://sapl.campinas.sp.leg.br/norma/1), published by the Câmara Municipal de Campinas. Each version names the page it was taken from and that page's sha256, in `data/versions.json`.

## Dates

The Lei Orgânica is given as the Câmara's compiled edition "Atualizada até a Emenda nº 55, de 6 de maio de 2025", dated 6 May 2025 (the day of that Emenda) and committed as the publisher's text; the text as promulgated on 30 March 1990 and the earlier wordings are not reconstructed. Each law is dated by the publication date SAPL records for it (else by its own date), and only laws whose own vigência clause says they take effect on their publication (or signature) are taken in (Decreto-Lei 4.657/1942, art. 1, would otherwise give 45 days). Commits are at noon in Campinas.

## How it is built

Lexifina reads the sources listed here and records each act's dated versions, and the laws that made each change, in one corpus file. `tools/build.py` writes this repository from that file, and the same corpus always gives the same commit hashes; `REPRODUCE.md` gives the details and the checks. A model (Claude) wrote Lexifina's code; it wrote no legal text, and no model runs when the history is built.

The PDF is read line by line: the letterhead and footer on every page, page numbers, the table of contents before the preamble and the signatures after "Sala de Sessões, em 30 de Março de 1990." are left out. The edition's notes in parentheses ("(Nova redação dada pela Emenda nº ...)", "(Acrescido pela Emenda nº ...)", "(Revogado pela ...)") are left out of the text, and each provision the edition marks "(Declarado inconstitucional pela ADIn nº ...)" is left out whole. Lines are joined into paragraphs (a new paragraph at a provision label, a heading line, or after a line ending in ".", ";" or ":"). One file per Art.; the transitional provisions, numbered from 1 again, are adt-*. Each law's PDF is read from its heading to the closing line that ends in its date (signatures after it are left out); lines repeated at the top or bottom of two or more pages and page numbers are left out; lines are joined into paragraphs, one file per Art.

## How it is checked

Every version is read back from git on the day it took effect (`tools/check_repo.py`) and must match the corpus; an independent letters-and-digits comparison of every version against the source page must show no difference. Results are in `REPRODUCE.md`.

## What "author" means

The author of each commit is the law that made the text, or, for a consolidated text, the publisher, with an e-mail address that cannot exist; the committer is always Lexifina.

## Limits

The record is SAPL's: a version is only as exact as the Câmara's text for it. Only the newest laws are in so far; older ones follow in later parts. The text is not the official version: only the Diário Oficial do Município is authoritative.

## Licence

See [LICENSE](LICENSE): Brazilian law texts are not protected by copyright (Lei 9.610/1998, art. 8, IV). Fonte: Câmara Municipal de Campinas, SAPL, Câmara Municipal de Campinas.
