class Logger:

    def __init__(self, file_name):
        self.log_file_name = file_name

    # 引数のlogに改行を追加して、ログ出力を行う
    def output_log(self, log):
        log_with_new_line = "{}\n".format(log)

        with open(self.log_file_name, "a") as f:
            f.write(log_with_new_line)

        return log_with_new_line

    # 引数のlogに改行を追加して、ログ出力を行う
    def output_error_log(self, log):
        error_log_with_new_line = "エラー: {}\n".format(log)

        with open(self.log_file_name, "a") as f:
            f.write(error_log_with_new_line)

        return error_log_with_new_line
