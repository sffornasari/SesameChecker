import numpy
def geopsy_hv_reader(hvfile, logfile=None, lw=None):
    """Function to read the parameters from geopsy .hv and .log files.
    The .log file can be omitted if the windows length is passed directly.
    """
    if logfile==None and lw==None:
        print("ERROR: provide logfile or lw.")
        return
    with open(hvfile, 'r') as f:
        lines = f.read().splitlines()
    f = []
    hv = []
    sigmaA = []
    for line in lines:
        if "#" in line:
            if "Number of windows =" in line:
                nw = int(line.split('=')[1].strip())
            elif "f0 from windows" in line:
                fa, fd, fm = line.split()[-3:]
                sigmaf = float(fm)/float(fa)
        else:
            fi, avgi, lowi, highi = [float(x) for x in line.split()]
            f.append(fi)
            hv.append(avgi)
            sigmaA.append(highi/avgi)
            # sigmaA = np.sqrt(np.divide(high, low))
    if logfile != None:
        with open(logfile, 'r') as f:
            lines = f.read().splitlines()
        for line in lines:
            if "WINDOW MIN LENGTH (s)" in line:
                lw = float(line.split('=')[1].strip())
            else:
                continue
    else:
        lw = float(lw)
    return np.array(f), np.array(hv), np.array(sigmaA), sigmaf, lw, nw