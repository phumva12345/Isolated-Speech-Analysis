import numpy as np
import heapq

class FeatureExtraction:
    def fzero(self, signal):
        new_signal = []
        max_cols = []
        rows = len(signal)
        cols = len(signal[0])
        for i in range(cols):
            max_index = 0
            max_signal = signal[0][i]
            for j in range(1, rows):
                if signal[j][i] > max_signal:
                    max_signal = signal[j][i]
                    max_index = j
            max_cols.append(max_index)
        for i in range(rows):
            new_s = []
            for j in range(cols):
                if max_cols[j] == i:
                    new_s.append(1)
                else:
                    new_s.append(np.NaN)
            new_signal.append(new_s)
        return new_signal

    def fone(self, signal):
        new_signal = []
        max_cols = []
        rows = len(signal)
        cols = len(signal[0])
        for i in range(cols):
            new_s = []
            for j in range(cols):
                new_s.append(signal[j][i])
            max_cols.append(heapq.nlargest(2, range(len(new_s)), key=new_s.__getitem__)[1])
        for i in range(rows):
            new_s = []
            for j in range(cols):
                if max_cols[j] == i:
                    new_s.append(1)
                else:
                    new_s.append(np.NaN)
            new_signal.append(new_s)
        return new_signal

    def formant_frequently(self, signal, n):
        new_signal = []
        max_cols = []
        rows = len(signal)
        cols = len(signal[0])
        for i in range(cols):
            new_s = []
            for j in range(cols):
                new_s.append(signal[j][i])
            max_cols.append(heapq.nlargest(6, range(len(new_s)), key=new_s.__getitem__)[n])
        for i in range(rows):
            new_s = []
            for j in range(cols):
                if max_cols[j] == i:
                    new_s.append(1)
                else:
                    new_s.append(np.NaN)
            new_signal.append(new_s)
        return new_signal
