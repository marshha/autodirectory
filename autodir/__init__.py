import os
import subprocess

#Example grid:

HEADER='''\\documentclass{article}
\\usepackage[demo]{graphicx}
\\usepackage{subfig}
\\begin{document}
\\begin{figure}
'''

TBLHEADER='''\\begin{tabular}'''

TBLFOOTER='''\\end{tabular}
'''

TBLENTRY='''\\subfloat[caption]{\\includegraphics[width = 1in]{something}}'''

CONTINUE_ROW=''' &
'''

END_ROW='''\\\\
'''

FOOTER='''\\caption{4 x 4}
\\end{figure}
\\end{document}
'''

def generate_pdf(indir, outdir, rows, cols, logdir=None, *kwargs):
    with open(os.path.join(outdir, "dir.tex"), 'w') as fp:
        fp.write(HEADER)
        fp.write(TBLHEADER + "{" + "".join(["c" for x in range(0, rows)]) + "}\n")
        for row in range(0, rows):
            for col in range(0, cols):
                fp.write(TBLENTRY)
                if col == cols-1:
                    if row != rows-1:
                        fp.write(END_ROW)
                    else:
                        fp.write("\n")
                else:
                    fp.write(CONTINUE_ROW)
        fp.write(TBLFOOTER)
        fp.write(FOOTER)

    in_fname = os.path.join(outdir, "dir.tex")

    cmd = ["pdflatex", in_fname, "-output-directory", outdir]

    if logdir:
        with open(os.path.join(logdir, "stdout"), "w") as p_stdout, open(os.path.join(logdir, "stderr"), "w") as p_stderr:
            subprocess.call(cmd, stdout=p_stdout, stderr=p_stderr)
    else:
        subprocess.call(cmd)
