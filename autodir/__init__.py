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
\\documentclass{article}
\\usepackage[margin=25pt]{geometry}
\\usepackage[demo]{graphicx}
\\usepackage{float}
\\begin{document}
'''

TBLHEADER='''\\begin{figure}[h!]
\\center
\\begin{tabular}'''

TBLFOOTER='''\\end{tabular}
\\end{figure}
'''

PICENTRY='''\\includegraphics[width = 1in]{{{0}}}'''

CONTINUE_ROW=''' &
'''

END_ROW='''\\\\
'''

FOOTER='''\\end{document}
'''

NEWPAGE='''\\pagebreak
\\newpage
'''

def read_input(indir):
    with open(os.path.join(indir, "input.csv"), "r") as fp:
        reader = csv.DictReader(fp)
        return [dict(x) for x in reader]

def generate_pdf(indir, outdir, rows, cols, logdir=None, *kwargs):
    def write_table(fp, input_data, indir, rows, cols):
        fp.write(TBLHEADER + "{" + "".join(["c" for x in range(0, rows)]) + "}\n")
        cnt = 0
        for row in range(0, rows):
            captions = []
            for col in range(0, cols):
                entry = input_data[cnt]
                cnt += 1
                ended = False
                if cnt == len(input_data):
                    ended = True
                print("{} {}".format(cnt, ended))

                fp.write(PICENTRY.format(
                    os.path.join(indir, entry["picture"])))
                captions.append("{} {}".format(entry["firstname"], entry["lastname"]))
                if col == cols-1 or ended:
                    fp.write(END_ROW)
                    fp.write(CONTINUE_ROW.join(captions))
                    if ended:
                        fp.write("\n")
                    elif row != rows - 1:
                        fp.write(END_ROW)
                    else:
                        # should not be reachable as
                        # input data should be consumed
                        fp.write("\n")
                else:
                    fp.write(CONTINUE_ROW)

                if ended:
                    break

            if ended:
                break
        fp.write(TBLFOOTER)
        return

    input_data = read_input(indir)
    total_entries = len(input_data)
    entries_per_page = rows * cols
    total_pages = math.ceil(float(total_entries)/entries_per_page)

    with open(os.path.join(outdir, "dir.tex"), 'w') as fp:
        fp.write(HEADER)
        for page in range(0, total_pages):
            write_table(fp, input_data[page*entries_per_page:(page+1)*entries_per_page],
                            indir, rows, cols)
            fp.write(NEWPAGE)
        fp.write(FOOTER)

    in_fname = os.path.join(outdir, "dir.tex")

    cmd = ["pdflatex", in_fname, "-output-directory", outdir]

    if logdir:
        with open(os.path.join(logdir, "stdout"), "w") as p_stdout, open(os.path.join(logdir, "stderr"), "w") as p_stderr:
            subprocess.call(cmd, stdout=p_stdout, stderr=p_stderr)
    else:
        subprocess.call(cmd)
