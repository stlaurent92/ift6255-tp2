import os

import matchzoo as mz
import pandas as pd


class NeuralSearchEngine:
    def __init__(self):

        self.data = None

        self.train_pack = None
        self.valid_pack = None

    def read_documents(self):
        list_of_doc_no = []
        list_of_content = []

        for root, dirs, files in os.walk("data/docs"):
            for dir in dirs:
                for document in os.listdir("./data/docs/" + dir):
                    list_of_doc_no, list_of_content = self.read_document_file("./data/docs/" + dir + "/" + document,
                                                                              list_of_doc_no, list_of_content)

        documents_in_files = {
            'doc_numbers': list_of_doc_no,
            'doc_content': list_of_content
        }

        df = pd.DataFrame(documents_in_files, columns=['doc_numbers', 'doc_content'])

        self.save_df_to_pickle(df, "documents")

    def read_document_file(self, file_path, list_of_doc_no, list_of_content):
        with open(file_path) as fp:
            is_in_text_section = False
            doc_no = None
            content = ""

            for line in fp:
                line = line.split("\n")[0]
                if line.startswith("<DOCNO>"):
                    doc_no = line.split("<DOCNO>")[1].split("</DOCNO>")[0].strip()

                elif line.startswith("</TEXT>"):
                    is_in_text_section = False
                    list_of_doc_no.append(doc_no)
                    list_of_content.append(content)

                    doc_no = None
                    content = ""

                elif is_in_text_section:
                    content += line

                elif line.startswith("<TEXT>"):
                    is_in_text_section = True

            return list_of_doc_no, list_of_content

    def save_df_to_csv(self, df, file):
        dirpath = os.getcwd()
        df.to_csv(dirpath + "\data\\" + file + ".csv", index=False, header=True)

    def save_df_to_pickle(self, df, file):
        dirpath = os.getcwd()
        df.to_pickle(dirpath + "\data\\" + file + ".pkl")

    def read_documents_from_pickle(self):
        self.data = pd.read_pickle(".\data\documents.pkl")

    def read_topics(self):
        list_of_topic_numbers = []
        list_of_topic_titles = []

        list_of_topic_numbers, list_of_topic_titles = self.read_topic_file("data/topics/topics.1-50.txt",
                                                                           list_of_topic_numbers,
                                                                           list_of_topic_titles)

        list_of_topic_numbers, list_of_topic_titles = self.read_topic_file("data/topics/topics.51-100.txt",
                                                                           list_of_topic_numbers,
                                                                           list_of_topic_titles)

        list_of_topic_numbers, list_of_topic_titles = self.read_topic_file("data/topics/topics.101-150.txt",
                                                                           list_of_topic_numbers,
                                                                           list_of_topic_titles)

        topics = {
            'topic_numbers': list_of_topic_numbers,
            'topic_title': list_of_topic_titles
        }

        df = pd.DataFrame(topics, columns=['topic_numbers', 'topic_title'])

        self.save_df_to_pickle(df, "topics")

    def read_topic_file(self, file_path, list_of_topic_numbers, list_of_topic_titles):
        with open(file_path) as fp:
            for line in fp:
                if line.startswith("<num>"):
                    list_of_topic_numbers.append(int(line.split(":")[1].strip()))
                elif line.startswith("<title>"):
                    list_of_topic_titles.append(line.split("Topic:")[1].strip())

            return list_of_topic_numbers, list_of_topic_titles

    def read_qrels(self):
        list_of_topic_numbers = []
        list_of_document_numbers = []
        list_of_labels = []

        list_of_topic_numbers, list_of_document_numbers, list_of_labels = self.read_qrels_file(
            "data/qrels/qrels.1-50.AP8890.txt",
            list_of_topic_numbers,
            list_of_document_numbers,
            list_of_labels)

        list_of_topic_numbers, list_of_document_numbers, list_of_labels = self.read_qrels_file(
            "data/qrels/qrels.51-100.AP8890.txt",
            list_of_topic_numbers,
            list_of_document_numbers,
            list_of_labels)

        list_of_topic_numbers, list_of_document_numbers, list_of_labels = self.read_qrels_file(
            "data/qrels/qrels.101-150.AP8890.txt",
            list_of_topic_numbers,
            list_of_document_numbers,
            list_of_labels)

        qrels = {
            'topic_numbers': list_of_topic_numbers,
            'documents_numbers': list_of_document_numbers,
            'labels': list_of_labels
        }

        df = pd.DataFrame(qrels, columns=['topic_numbers', 'documents_numbers', 'labels'])
        self.save_df_to_pickle(df, "qrels")

    def read_qrels_file(self, file_path, list_of_topic_numbers, list_of_document_numbers, list_of_labels):
        with open(file_path) as fp:
            for line in fp:
                array = line.split(" ")
                list_of_topic_numbers.append(int(array[0]))
                list_of_document_numbers.append(array[2])
                list_of_labels.append(array[3].split("\n")[0])

        return list_of_topic_numbers, list_of_document_numbers, list_of_labels

    def train_model(self):
        train_pack = mz.datasets.wiki_qa.load_data('train', task='ranking')
        valid_pack = mz.datasets.wiki_qa.load_data('dev', task='ranking')
        print(type(valid_pack))


        # preprocessor = mz.preprocessors.DSSMPreprocessor()
        # train_processed = preprocessor.fit_transform(train_pack)
        # valid_processed = preprocessor.transform(valid_pack)
        #
        # ranking_task = mz.tasks.Ranking(loss=mz.losses.RankCrossEntropyLoss(num_neg=4))
        # ranking_task.metrics = [
        #     mz.metrics.NormalizedDiscountedCumulativeGain(k=3),
        #     mz.metrics.MeanAveragePrecision()
        # ]
        #
        # model = mz.models.DSSM()
        # model.params['input_shapes'] = preprocessor.context['input_shapes']
        # model.params['task'] = ranking_task
        # model.guess_and_fill_missing_params()
        # model.build()
        # model.compile()
        #
        # train_generator = mz.PairDataGenerator(train_processed, num_dup=1, num_neg=4, batch_size=64, shuffle=True)
        # valid_x, valid_y = valid_processed.unpack()
        # evaluate = mz.callbacks.EvaluateAllMetrics(model, x=valid_x, y=valid_y, batch_size=len(valid_x))
        # history = model.fit_generator(train_generator, epochs=20, callbacks=[evaluate], workers=5,
        #                               use_multiprocessing=False)
        #
        # model.save('my-model')
        # loaded_model = mz.load_model('my-model')


if __name__ == '__main__':
    nse = NeuralSearchEngine()
    nse.train_model()
