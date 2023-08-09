import matplotlib.pyplot as plt
import scipy.io as sio

def plot_mat_file(filename):
    data = sio.loadmat(filename, squeeze_me=True)
    samps = data['samps']
    #samps_real = samps.real  # Get the real part of the complex data
    length = len(samps)
    plt.plot(range(length), samps)
    plt.xlabel('Sample Index')
    plt.ylabel('Amplitude')
    plt.title('Plot of ' + filename)
    plt.show()

# Example usage
filename = 'kavach.mat'
plot_mat_file(filename)
