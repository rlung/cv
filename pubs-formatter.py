import bibtexparser
import calendar


cal_dict = {abbr.lower(): f"{num:02d}" for num, abbr in enumerate(calendar.month_abbr)}

# Open bibtex and parse data
with open('pubs.bib') as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file)

pubs = bib_database.entries

# Format publications
pubs_date = []
pubs_formatted = []
for pub in pubs:
    # Format authors
    authors = pub['author']
    authors_formatted = []
    for author in authors.split(' and '):
        names = author.split(', ')
        full_name = f'{names[0]} {"".join(c for c in names[1] if c.isupper())}'
        if full_name == 'Ung RL':
            full_name = f"\\textbf{{{full_name}}}"
        authors_formatted.append(full_name)
    authors = ', '.join(authors_formatted)

    # Format title
    title = pub['title'][1:-1]
    if title[-1] == '.':
        title = title[:-1]
    
    # Remaining properties
    year = pub['year']
    journal = pub['journal']
    
    # Add publication
    pubs_date.append(year + cal_dict[pub.get('month', '')])
    pubs_formatted.append(
        f"{authors} ({year}). {title}. \\textbf{{\\textit{{{journal}}}}}."
    )
sort_ix = sorted(range(len(pubs_date)), key=lambda x: pubs_date[x])[::-1]
pubs_formatted = [pubs_formatted[i] for i in sort_ix]

# Create file
with open('pubs-auto.tex', 'w') as pub_file:
    def new_item(text):
        pub_file.write(f"  \\item {text}\n")

    pub_file.write('\\begin{etaremune}\n')
    for entry in pubs_formatted:
        new_item(entry)
    pub_file.write('\\end{etaremune}\n')