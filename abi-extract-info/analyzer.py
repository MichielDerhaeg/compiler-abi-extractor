import abc
import tempfile

class Analyzer(abc.ABC):
    def __init__(self, Driver, Report, Target, name):
        self.Driver = Driver
        self.Report = Report
        self.Target = Target
        self.name = name
        self.source_files = ["src/helper.c"]
        self.assembly_files = ["src/arch/riscv.S", "src/arch/riscv2.s"]

    def generate(self, src):
        (handle, temp_source_file) = tempfile.mkstemp(
            suffix=".c", prefix=self.name, dir=None, text=True
        )
        with open(temp_source_file, "w") as file:
            file.write(src)
        res, stdout_file = self.Driver.run(
            self.source_files + [temp_source_file],
            self.assembly_files,
            self.name,
        )
        if res != 0:
            print("Skip: err")
            return None  # FIXME should be throw
        return stdout_file

    @abc.abstractmethod
    def analyze(self):
        pass

    def run(self):
        summary_content = self.analyze()
        summary_file = f"tmp/{self.name}.sum"
        with open(summary_file, "w") as file:
            file.write(summary_content)
        self.Report.append(summary_file)
