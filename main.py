import csv
import os


files_directory = './data'


def filter_data_conditions(row) -> bool:
    if int(row['age']) >= 20 and int(row['age']) <= 59:
        if int(row['height']) >= 150 and int(row['height']) <= 190:
            if int(row['weight']) >= 50 and int(row['weight']) <= 90:
                if float(row['eyesight']) == 1.0:
                    if row['education'] == 'PhD' or row['education'] == 'Master':
                        if row['english_language'] == 'true':
                            return True
    return False


class Parser:
    def __init__(self,
                 filepath: str) -> None:
        self.raw_data = []
        self.clean_data = []
        self.prioritized = []
        self.candidates = []
        self.filepath = filepath
        self.files: list
        self.get_files()
        self.read_data()
        self.filter_data()
        self.sort_data()
        self.prioritized = sorted(self.prioritized,
                                  key=lambda candidate: [
                                             candidate['name'],
                                             candidate['surname']
                                  ])
        self.candidates = sorted(self.candidates,
                                 key=lambda candidate: [
                                            candidate['name'],
                                            candidate['surname'],
                                            int(candidate['age'])])
        self.prioritized = self.normalize_data(self.prioritized)
        self.candidates = self.normalize_data(self.candidates)
        self.write_data()

    def get_files(self) -> None:
        self.files = [file for file in os.listdir(self.filepath)
                      if file.endswith('.csv')]

    def read_data(self) -> None:
        for file in self.files:
            if not file == 'result.csv':
                filepath = os.path.join(self.filepath, file)
                with open(filepath) as f:
                    reader = csv.DictReader(f, delimiter='#')
                    self.raw_data += [row for row in reader]

    def filter_data(self) -> None:
        self.raw_data = [data_dict for data_dict in self.raw_data
                         if filter_data_conditions(data_dict)]

    def normalize_data(self, data: list[dict]) -> None:
        result = []
        for dict in data:
            result.append({
                'id': dict['id'],
                'name': dict['name'],
                'surname': dict['surname'],
                'height': dict['height'],
                'weight': dict['weight'],
                'education': dict['education'],
                'age': dict['age']
            })
        return result

    def sort_data(self) -> None:
        for person in self.raw_data:
            if int(person['age']) >= 27 and int(person['age']) <= 37:
                self.prioritized.append(person)
            else:
                self.candidates.append(person)

    def write_data(self) -> None:
        filepath = os.path.join(self.filepath, 'result.csv')
        fieldnames = ['id', 'name', 'surname',
                      'height', 'weight', 'education',
                      'age']
        with open(filepath, 'w+') as f:
            writer = csv.DictWriter(f, fieldnames,
                                    delimiter='#')
            data = self.prioritized + self.candidates
            for idx, candidate in enumerate(data, start=1):
                candidate['id'] = idx
            writer.writerows(data)


if not files_directory:
    files_directory = input('Введите путь к папке с данными: ')
p = Parser(files_directory)
