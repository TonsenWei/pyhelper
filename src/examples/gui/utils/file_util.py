import os


class FileUtil:

    @staticmethod
    def get_files_path_list(dir_path, suffix):
        info_list = []
        for i, j, k in os.walk(dir_path):
            for file in k:
                if file.endswith(suffix):
                    info_list.append(os.path.join(i, file))
        print(info_list)
        return info_list


if __name__ == "__main__":
    FileUtil.get_files_path_list(r"D:\Projects\gitee\pylearning\files\wav_report", ".wav")
