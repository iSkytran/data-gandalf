# Data Gandalf Documentation

There are three manuals that come with Data Gandalf. A developer guide, installation guide, and a user manual. The guides are written in markdown, but the PDF and Word documents can be generated from markdown files using [Pandoc](https://pandoc.org/). The style of the outputted PDF documents can be customized using [LaTeX](https://www.latex-project.org/) in the [style.tex](style.tex) file.

Assuming Pandoc and its dependencies are installed the following command can be used to generate PDFs:

```sh
pandoc --listings -H listings.tex <input_file_path>.md -o <output_file_path>.pdf
```

Similarly, for Word files:

```sh
pandoc --listings -H listings.tex <input_file_path>.md -o <output_file_path>.docx
```
