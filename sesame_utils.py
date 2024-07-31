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
                fm, fl, fh = line.split()[-3:]
                sig = float(fm)/float(fl)
                m = np.log(fm)
                s = np.log(sig)
                # Compute the standard deviation of a log-normal distribution
                varf = np.exp(2*m+s**2)*(np.exp(s**2)-1)
                sigmaf = np.sqrt(varf)
        else:
            fi, avgi, lowi, highi = [float(x) for x in line.split()]
            f.append(fi)
            hv.append(avgi)
            sigmaA.append(highi/avgi)
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
