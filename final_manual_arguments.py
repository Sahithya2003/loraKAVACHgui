import argparse
import numpy as np
import uhd
import scipy.io as sio
import os

def parse_args():
    """Parse the command line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--args", default="", type=str)
    parser.add_argument("-o", "--output-file", type=str, required=True)
    parser.add_argument("-f", "--freq", type=float, required=True)
    parser.add_argument("-r", "--rate", default=1e6, type=float)
    parser.add_argument("-d", "--duration", default=5.0, type=float)
    parser.add_argument("-c", "--channels", default=0, nargs="+", type=int)
    parser.add_argument("-g", "--gain", type=int, default=10)
    parser.add_argument("-n", "--numpy", default=False, action="store_true",help="Save output file in NumPy format (default: No)")
    parser.add_argument("-m", "--mat-output", default=False, action="store_true",help="Save output file in MATLAB .mat format (default: No)")

    return parser.parse_args()
def clear_console():
    """Clear the console/terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')
   
def main():
    """RX samples and write to file"""
    args = parse_args()

    usrp = uhd.usrp.MultiUSRP(args.args)
    num_samps = int(np.ceil(args.duration * args.rate))

    if not isinstance(args.channels, list):
        args.channels = [args.channels]

    usrp.set_rx_antenna("RX2")  # Set antenna to RX2

    samps = usrp.recv_num_samps(num_samps, args.freq, args.rate, args.channels, args.gain)

    freq = usrp.get_rx_freq()
    print(f"The USRP is tuned to a frequency of {freq} Hz.")

    #bandwidth = usrp.get_rx_bandwidth()
    #print(f"The USRP is scanning a bandwidth of {bandwidth} Hz.")
    


    gain = usrp.get_rx_gain()
    print(f"Current gain: {gain} dB")

    if args.mat_output:
        sio.savemat(args.output_file, {'samps': samps})
    else:
        with open(args.output_file, 'wb') as out_file:
            if args.numpy:
                np.save(out_file, samps, allow_pickle=False, fix_imports=False)
            else:
                samps.tofile(out_file)

if __name__ == "__main__":
    clear_console()
    args = parse_args()
    usrp = uhd.usrp.MultiUSRP(args.args)
    main()

# Europe	      EU868 (863–870/873 MHz)
# North America	  US915 (902–928 MHz)
# Asia	          AS923 (915–928 MHz)
# Oceania	      AS923-1 (915–928 MHz)
# India	           IN865 (865–867 MHz)
# Worldwide  	   2.4 GHz 
# Europe, Asia, Oceania, Africa, India 433 MHz
