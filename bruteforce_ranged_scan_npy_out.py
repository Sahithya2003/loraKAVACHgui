import argparse
import torch
import uhd
import scipy.io as sio
import os
import numpy as np
 

def parse_args():
    """Parse the command line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--args", default="", type=str)
    parser.add_argument("-o", "--output-dir", type=str, required=True)
    parser.add_argument("-f", "--start-freq", type=float, required=True)
    parser.add_argument("-e", "--end-freq", type=float, required=True)
    parser.add_argument("-r", "--rate", default=1e6, type=float)
    parser.add_argument("-d", "--duration", default=5.0, type=float)
    parser.add_argument("-c", "--channels", default=0, nargs="+", type=int)
    parser.add_argument("-g", "--gain", type=int, default=10)
    parser.add_argument("-n", "--numpy", default=False, action="store_true", 
                        help="Save output file in NumPy format (default: No)")
    parser.add_argument("-m", "--mat-output", default=False, action="store_true", 
                        help="Save output file in MATLAB .mat format (default: No)")
    return parser.parse_args()
 

def clear_console():
    """Clear the console/terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')
 

def main():
    """RX samples and write to file"""
    args = parse_args()
    usrp = uhd.usrp.MultiUSRP(args.args)
    num_samps = int(torch.ceil(torch.tensor(args.duration*args.rate)))
    
    if not isinstance(args.channels, list):
        args.channels = [args.channels]

    usrp.set_rx_antenna("RX2")  # Set antenna to RX2
    
    freq = args.start_freq
    while freq <= args.end_freq:
        samps = usrp.recv_num_samps(num_samps, freq, args.rate, args.channels, args.gain)
        freq_str = f"{int(freq / 1e6)}MHz"
        output_file = os.path.join(args.output_dir, f"{freq_str}.mat")
        
        if args.mat_output:
            sio.savemat(output_file, {'samps': samps})
        else:
            with open(output_file, 'wb') as out_file:
                if args.numpy:
                    np.save(out_file, samps, allow_pickle=False, fix_imports=False)
                else:
                    samps.tofile(out_file)

        freq += args.rate 
        print(f"Scanned frequency {freq_str} and saved to {output_file}")


if __name__ == "__main__":
    clear_console()
    main()