from PreProcessing import *
from scipy.spatial import distance as dist
import cv2

PATH = 'D:/Downloads/speech/Isolated Words/1/'

def plotHist(hist, name):
    plt.figure(name)
    x = [i+1 for i in range(len(hist))]
    plt.bar(x, height=hist)
    plt.xticks(x, x)
    plt.xlabel('Period')

class Assessment:
    def __init__(self):
        self.scipy_methods = {
            "euclidean": dist.euclidean,
            "manhattan": dist.cityblock,
            "chebysev": dist.chebyshev,
            "hellinger": cv2.HISTCMP_BHATTACHARYYA,
            "correlation": cv2.HISTCMP_CORREL
            }
        self.methods = {
            "ZCR": self.ZCR,
            "TimeDuration": self.TimeDuration}
        self.ths = [float("{0:.04f}".format(i*0.001)) for i in range(6, 16, 2)]

    def segment(self, signal):
        signals = []
        count = -1
        isInSpeech = False
        for i in range(len(signal)):
            if signal[i] != 0 and not isInSpeech:
                signals.append([signal[i]])
                isInSpeech = True
                count += 1
            elif signal[i] == 0:
                isInSpeech = False

            if isInSpeech:
                signals[count].append(signal[i])
        return signals

    def ZCR(self, file_name, threshold):
        _, signal = PreProcessing().process(file_name, combine=False, threshold=threshold)
        signals = self.segment(signal)

        hist = []
        for segment in signals:
            total = 0
            for i in range(1, len(segment)):
                total += (segment[i] - segment[i - 1]) ** 2
            hist.append(total / len(segment))
        return hist

    def TimeDuration(self, file_name, threshold):
        sample_rate, signal = PreProcessing().process(file_name, combine=False, threshold=threshold)
        signals = self.segment(signal)

        hist = []
        for segment in signals:
            hist.append(len(segment) / sample_rate)
        return hist

    def assess(self, template_file_name, file_name, method, scipy_method):
        best_result = 1
        best_template_th = self.ths[0]
        best_th = self.ths[0]

        for i in range (len(self.ths)):
            template_hist = np.float32(np.array(self.methods[method](template_file_name, self.ths[i])))
            for j in range (len(self.ths)):
                hist = np.float32(np.array(self.methods[method](file_name, self.ths[j])))
                if len(template_hist) != len(hist):
                    continue
                if scipy_method == 'hellinger' or scipy_method == 'correlation':
                    result = cv2.compareHist(template_hist, hist, self.scipy_methods[scipy_method])
                else:
                    result = self.scipy_methods[scipy_method](template_hist, hist)
                result = abs(result)
                if result < best_result:
                    best_result = result
                    best_template_th = self.ths[i]
                    best_th = self.ths[j]

        if scipy_method == 'hellinger':
            return 1 - best_result, best_template_th, best_th
        elif scipy_method == 'correlation':
            return best_result, best_template_th, best_th
        return max(0, 1 - (best_result * 100)), best_template_th, best_th

def getWordsFromDataSet():
    import os

    ths = [float("{0:.04f}".format(i*0.001)) for i in range(8, 16, 1)]
    scipy_methods = ["euclidean", "manhattan", "chebysev"]
    methods = ["ZCR"]
    test_word = 'candy'
    template = '1F'
    words = []

    for filename in os.listdir(PATH):
        template_f = filename.split('_')[1]
        if template_f == template:
            temp = filename.split('.')[0]
            word = temp.split('_')[2]
            words.append(word)
    return words

if __name__ == "__main__":
    words = getWordsFromDataSet()
    total_acc_eu = 0
    total_acc_man = 0
    total_acc_che = 0
    count_eu = 0
    count_man = 0
    count_che = 0
    count_word = 0
    count_zero = 0
    count = 0
    # scipy_methods = ["euclidean", "manhattan", "chebysev"]
    scipy_methods = ["chebysev"]
    methods = ["ZCR"]
    # test_set = ['isw_1F_','isw_2M_','isw_1M_']
    test_set = ['isw_2M_']

    for test_word in words:
        count_word += 1
        print(count_word, '--- %s ---'%test_word)
        # test_word = 'candy'
        # template = PATH + 'isw_2F_' + test_word + '.wav'
        template = PATH + 'isw_1M_' + test_word + '.wav'

        for method in methods:
            for scipy_method in scipy_methods:
                print("Feature:", method, ", Method:", scipy_method, end = "\n\n")
                for t in test_set:
                    acc, template_th, th = Assessment().assess(template, PATH+'%s%s.wav'%(t, test_word), method=method, scipy_method=scipy_method)
                    print('Test file: %s%s.wav'%(t, test_word))
                    # print("Accuracy:", '{0:.2f}'.format(acc))
                    new_acc = '{0:.2f}'.format(acc)
                    print("Accuracy: %s, Template th: %s , Test th: %s" % (new_acc, template_th, th))
                    if scipy_method == 'euclidean':
                        total_acc_eu += float(new_acc)
                        if float(new_acc) != 0:
                            count_eu += 1
                    elif scipy_method == 'manhattan':
                        total_acc_man += float(new_acc)
                        if float(new_acc) != 0:
                            count_man += 1
                    elif scipy_method == 'chebysev':
                        count += 1
                        total_acc_che += float(new_acc)
                        if float(new_acc) != 0:
                            count_che += 1
                print()

        # print("Curr Euclidean Total Acc:", '{0:.2f}'.format(total_acc_eu / count_eu))
        # print("Curr Manhattan Total Acc:", '{0:.2f}'.format(total_acc_man / count_man))
        if count_che != 0:
            print("Curr Chebysev Total Acc:", '{0:.2f}'.format(total_acc_che / count_che))
            # print("Euclidean: total: %s, non-zero: %s, zero: %s"%(count, count_eu, count - count_eu))
            # print("Manhattan: total: %s, non-zero: %s, zero: %s"%(count, count_man, count - count_man))
            print("Chebysev: total: %s, non-zero: %s, zero: %s"%(count, count_che, count - count_che))
            print()

    # test = "robot-2.wav"
    # template_hist = Assessment().TimeDuration(template, 0.005)
    # hist = Assessment().TimeDuration(test, 0.005)

    # plotHist(template_hist, "Template")
    # plotHist(hist, "Test")

    # result = Assessment().assess(template, test, 'TimeDuration', 'euclidean')
    # print(result)

#     # plt.show()

# acc, template_th, th = Assessment().assess(PATH+'isw_1F_acorn.wav', PATH+'isw_1F_hazel.wav', method='ZCR', scipy_method='chebysev')
# print("Accuracy: %s, Template th: %s , Test th: %s" % (acc, template_th, th))
