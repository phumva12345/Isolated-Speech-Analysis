import os
from deepspeech import *

path = 'D:/speech dataset/Indiana University Word Database/audio/'
spec_path = 'D:/speech dataset/Indiana University Word Database/spectrogram/'
mfcc_path = 'D:/speech dataset/Indiana University Word Database/mfccs/'
formant_path = 'D:/speech dataset/Indiana University Word Database/formant/'

def save_spec(processed_signal, sample_rate, filename):
    frequencies, times, spectrogram = signal.spectrogram(processed_signal, sample_rate)
    fig, ax = plt.subplots()
    fig.subplots_adjust(left=0,right=1,bottom=0,top=1)
    im = ax.pcolormesh(times, frequencies, np.log(spectrogram))
    ax.axis('tight')
    ax.axis('off')
    fig.savefig(spec_path + filename + '.png')
    plt.close(fig)

def save_mfcc(processed_signal, sample_rate, filename):
    mfcc_feat = mfcc(processed_signal, sample_rate)
    mfcc_data = np.swapaxes(mfcc_feat, 0 ,1)

    fig, ax = plt.subplots()
    fig.subplots_adjust(left=0,right=1,bottom=0,top=1)
    im = ax.imshow(mfcc_data, interpolation='nearest', origin='lower', aspect='auto')
    ax.axis('tight')
    ax.axis('off')
    fig.savefig(mfcc_path + filename + '.png')
    plt.close(fig)

def save_formant(processed_signal, sample_rate, filename):
    frequencies, times, spectrogram = signal.spectrogram(processed_signal, sample_rate)
    fig, ax = plt.subplots()
    fig.subplots_adjust(left=0,right=1,bottom=0,top=1)
    im = ax.pcolormesh(times, frequencies, np.log(spectrogram))
    ax.pcolormesh(times, frequencies, fzero(np.log(spectrogram)), cmap=plt.cm.Reds_r)
    ax.pcolormesh(times, frequencies, fone(np.log(spectrogram)), cmap=plt.cm.spring)
    ax.axis('tight')
    ax.axis('off')
    fig.savefig(formant_path + filename + '.png')
    plt.close(fig)

count = 0
for filename in os.listdir(path):
    count += 1
    file_name = filename.split('.')[0]
    print(count, file_name)
    sample_rate, processed_signal = PreProcessing().process(path + filename, trim = False)
    save_spec(processed_signal, sample_rate, file_name)
    save_mfcc(processed_signal, sample_rate, file_name)
    save_formant(processed_signal, sample_rate, file_name)
