class ProcessedSignal:
    def __init__(self, signals, sample_rate):
        self.signals = signals
        self.sample_rate = sample_rate

    def getSignals(self):
        return self.signals

    def getSampleRate(self):
        return self.sample_rate
