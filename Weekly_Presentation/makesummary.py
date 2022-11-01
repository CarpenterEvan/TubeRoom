from pylatex import Document, Section, MdFramed, Itemize, Enumerate, Command, NoEscape

if __name__ == '__main__':
	doc = Document(documentclass="beamer")
	with doc.create(MdFramed()):
		doc.append("text")
		

doc.generate_pdf('full', clean_tex=False)
