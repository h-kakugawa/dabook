# A format converter from DIMACS graph file to Graphviz Dot (and more)
#
# Example:
#   $ python3 dim2dot g_test01.dat

from dimacs import DIMACS
import argparse
import sys
import os
import re
import subprocess

param_resolution = 300
param_penwidth = 1.0
param_layout = 'dot'

def dimacs_to_dot(file_dimacs, file_dot, enable_overwrite):
    if os.path.isfile(file_dot) and not enable_overwrite:
        sys.exit("ERROR: OUTPUT FILE EXISTS: " + file_dot)
    d = DIMACS(file_dimacs)
    with open(file_dot, 'w') as f:
        gtype = 'graph'
        etype = '--'
        f.write(gtype + ' {\n')
        f.write('  graph [\n')
        f.write('    charset = "UTF-8",\n')
        f.write('    dpi = {},\n'.format(param_resolution))
        f.write('    labeljust = "c",\n')
        f.write('  ];\n')
        f.write('  node [\n')
        f.write('    fontsize = 10,\n')
        f.write('    fontname = "Noto Serif",\n')
        f.write('    fixedsize = true,\n')
        f.write('    penwidth = {},\n'.format(param_penwidth))
        f.write('    shape = circle,\n')
        f.write('    height = 0.3,\n')
        f.write('    width = 0.3\n')
        f.write('  ];\n')
        f.write('  edge [\n')
        f.write('    fontsize = 9,\n')
        f.write('    fontname = "Noto Serif",\n')
        f.write('    penwidth = {}\n'.format(param_penwidth))
        f.write('  ];\n')
        for pid in range(d.get_n()):
            label = 'P' + str(pid)
            rank = 'max' if pid == 0 else 'min'
            node_attr = \
                'tooltop="{}", '.format(label) + \
                'label="{}" '.format(label) + \
                ''
            f.write('  {} [ {}];\n'.format(pid, node_attr))
        if d.is_weighted():
            for e in d.get_wedges():
                w = e[2]
                wi = int(w)
                sw = str(w)
                if abs(wi - w) < 0.001:
                    sw = str(int(w))
                edge_attr = \
                    'label = "{}", '.format(sw) + \
                    'labelfloat = true '
                f.write('  {} {} {} [ {}];\n'.format(e[0], etype, e[1],
                                                     edge_attr))
        else:
            for e in d.get_edges():
                f.write('  {} {} {};\n'.format(e[0], etype, e[1]))
        f.write('}\n')

def dot_to_svg(file_dot, file_svg, layout):
    run_dot('svg', file_dot, file_svg, layout)

def dot_to_png(file_dot, file_png, layout):
    run_dot('png', file_dot, file_png, layout)

def dot_to_pdf(file_dot, file_pdf, layout):
    run_dot('pdf', file_dot, file_pdf, layout)

def dot_to_eps(file_dot, file_eps, layout):
    run_dot('eps', file_dot, file_eps, layout)

def run_dot(out_format, file_dot, file_out, layout):
    try:
        cmd = "dot" \
            + " -T" + out_format \
            + " -K" + layout \
            + " -o" + file_out \
            + " " + file_dot 
        ret = subprocess.run(cmd, shell = True)
    except subprocess.CalledProcessError as e:
        print(e)
        sys.exit(1)

# ------------------------------------------
if __name__ == '__main__':
    desc = 'A format converter from DIMACS graph file to Graphviz Dot ' \
        + '(and more, PDF, PNG, etc. for example)'
    p = argparse.ArgumentParser(description = desc)
    p.add_argument('FILE',
                   help="Input file name (DIMACS graph file)",
                   type=str)
    p.add_argument('-O',
                   help="Enable overwriting the output file (Default: {})".\
                   format('Disable'),
                   action='store_true',
                   default=False)
    p.add_argument('-r',
                   help="Device resolution in DPI (Default: {})".\
                   format(param_resolution),
                   type=int,
                   default=param_resolution)
    p.add_argument('-l',
                   help="Drawing layout scheme (Default: {})".\
                   format(param_layout),
                   choices=['dot', 'neato', 'fdp', 'sfdp', 'circo', 'twopi'],
                   default=param_layout)
    args = p.parse_args()
    param_file_dimacs = args.FILE
    param_enable_overwrite = args.O
    param_resolution = args.r
    param_layout = args.l
    r, e = os.path.splitext(param_file_dimacs)
    file_dot = r + ".dot"
    dimacs_to_dot(param_file_dimacs, file_dot, param_enable_overwrite)
    dot_to_svg(file_dot, r + ".svg", param_layout)
    dot_to_png(file_dot, r + ".png", param_layout)
    dot_to_pdf(file_dot, r + ".pdf", param_layout)
    dot_to_eps(file_dot, r + ".eps", param_layout)
