import sys

usage = """
    python create_hmmdefs_from_proto.py hmm_proto phones_labels output_folder
    [vFloors_file]

    Where hmm_proto is a prototype file for the HMMs, phones_labels is a dict
    of the phones that are in the dataset and output_folder will contain all 
    the HMMs of the model (in hmmdefs one for each phone) and the macros file.
    Optionally, vFloors is the file with the variances (generated by HCompV).
"""

def create_hmmdefs(proto, labels, output_folder, vFloors=""):
    output_folder = output_folder.rstrip('/')
    labels_file = open(labels, 'r')
    hmmdefs_fname = output_folder + '/hmmdefs'
    hmmdefs_file = open(hmmdefs_fname, 'w')
    macros_fname = output_folder + '/macros'
    macros_file = open(macros_fname, 'w')
    header = False
    for line in open(proto):
        if "~o" in line:
            header = True
        elif "~" in line:
            header = False
        if header == True:
            macros_file.write(line)
    if vFloors != "":
        for line in open(vFloors):
            macros_file.write(line)
    macros_file.close()
    print ">>> Written", macros_fname, "file"
    header = False
    for line in labels_file:
        phone = line.rstrip('\n')
        started = False
        for line in open(proto):
            if header == False and "~o" in line:
                header = True
                started = True
                hmmdefs_file.write(line)
            elif "~h" in line:
                started = True
                hmmdefs_file.write(line.replace('proto', phone))
            elif started == True:
                hmmdefs_file.write(line)
    hmmdefs_file.close()
    print ">>> Written", hmmdefs_fname, "file"


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print >> sys.stderr, usage
        sys.exit(-1)
    if len(sys.argv) > 4:
        create_hmmdefs(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        create_hmmdefs(sys.argv[1], sys.argv[2], sys.argv[3])
