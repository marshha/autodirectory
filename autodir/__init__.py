import os
import subprocess
import csv
import math

HEADER='''\\overfullrule=10pt
\\setlength{\\parindent}{0pt}
\\addtolength{\\oddsidemargin}{-.875in}
\\addtolength{\\evensidemargin}{-.875in}
\\addtolength{\\textwidth}{1.75in}
\\addtolength{\\topmargin}{-.875in}
\\addtolength{\\textheight}{1.75in}
\\documentclass[titlepage]{article}
\\pagestyle{empty}
\\usepackage[margin=25pt]{geometry}
\\usepackage{graphicx}
\\usepackage{float}
\\usepackage{easytable}
\\usepackage{relsize}
'''

COVERPAGE='''\\begin{{document}}
\\title{{{0} \\\\ \\smaller{{}} Last updated: \\today}}
\\date{{}}
\\maketitle
'''

TBLHEADER='''\\begin{figure}[h!]
\\center
\\begin{TAB}(c,0.5in,0.5in)[5pt,7.5in,10in]'''

TBLFOOTER='''\\end{TAB}
\\end{figure}
'''

PICENTRY='''\\includegraphics[width=1.25in,height=1.25in,keepaspectratio]{{{0}}}'''

CONTINUE_ROW=''' &
'''

END_ROW='''\\\\
'''

FOOTER='''\\end{document}
'''

NEWPAGE='''\\pagebreak
\\newpage
'''

def read_input():
    with open("input.csv", "r") as fp:
        reader = csv.DictReader(fp)
        return sorted([dict(x) for x in reader if x["picture"]],
                        key = lambda x: (x["lastname"], x["firstname"]))

def generate_pdf(indir, outdir, rows, cols, title, logdir=None, *kwargs):
    def write_table(fp, input_data, indir, rows, cols):
        fp.write(TBLHEADER)
        fp.write("{" + "".join(["c" for x in range(0, cols)]) + "}")
        fp.write("{" + "".join(["bt" for x in range(0, rows)]) + "}")
        fp.write("\n")
        cnt = 0
        ended = False
        for row in range(0, rows):
            captions = []
            for col in range(0, cols):
                if ended:
                    entry = None
                else:
                    entry = input_data[cnt]

                cnt += 1
                print("{} {}".format(cnt, ended))

                if ended:
                    fp.write("  ")
                    captions.append("  ")
                else:
                    fp.write(PICENTRY.format(entry["picture"]))
                    captions.append("{} {}".format(entry["firstname"], entry["lastname"]))

                if col == cols-1:
                    fp.write(END_ROW)
                    fp.write(" & ".join(captions))
                    fp.write(END_ROW)
                else:
                    fp.write(CONTINUE_ROW)

                if cnt == len(input_data):
                    ended = True

        fp.write(TBLFOOTER)
        return

    os.chdir(indir)
    input_data = read_input()
    total_entries = len(input_data)
    entries_per_page = rows * cols
    total_pages = math.ceil(float(total_entries)/entries_per_page)

    with open("dir.tex", 'w') as fp:
        fp.write(HEADER)
        fp.write(COVERPAGE.format(title))
        for page in range(0, total_pages):
            write_table(fp, input_data[page*entries_per_page:(page+1)*entries_per_page],
                            indir, rows, cols)
            fp.write(NEWPAGE)
        fp.write(FOOTER)

    in_fname = "dir.tex"

    cmd = ["pdflatex", in_fname]

    if logdir:
        with open(os.path.join(logdir, "stdout"), "w") as p_stdout, open(os.path.join(logdir, "stderr"), "w") as p_stderr:
            subprocess.call(cmd, stdout=p_stdout, stderr=p_stderr)
    else:
        subprocess.call(cmd)
