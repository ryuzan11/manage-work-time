import logging
from service.utils import convert_list_to_comma_str


class Logger:
    def __init__(self, name = __name__):
        self.log_export = logging.getLogger(name)
        self.log_export.setLevel(logging.INFO)

    def debug(self, msg):
        self.log_export.debug(msg)

    def info(self, msg):
        self.log_export.info(msg)

    def warning(self, msg):
        self.log_export.warning(msg)

    def error(self, msg):
        self.log_export.error(msg)

    def exception(self, msg):
        self.log_export.exception(msg)


class LogExport:

    def __init__(self, file_name):
        self.log_file_name = file_name

    # 引数のlogに改行を追加して、ログ出力を行う
    def output_log(self, log):
        log_with_new_line = "{}\n".format(log)

        with open(self.log_file_name, "a", newline='\n') as f:
            f.write(log_with_new_line)

        return log_with_new_line

    # 引数のlogに改行を追加して、ログ出力を行う
    def output_log_list(self, log_list):
        log_list_with_new_line = ["{}\n".format(convert_list_to_comma_str(log)) for log in log_list]

        with open(self.log_file_name, "a", newline='\n') as f:
            f.writelines(log_list_with_new_line)

        return log_list_with_new_line

    # 引数のlogに改行を追加して、ログ出力を行う
    def output_error_log(self, log):
        error_log_with_new_line = "エラー: {}\n".format(log)

        with open(self.log_file_name, "a") as f:
            f.write(error_log_with_new_line)

        return error_log_with_new_line
