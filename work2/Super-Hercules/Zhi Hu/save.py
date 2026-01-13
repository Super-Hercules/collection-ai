import os
import csv

def save_to_csv(question, filename = "Zhihu.csv"):
    #保存到csv文件
    current_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(current_dir, filename)
    headers = ["序号", "标题", "内容"]
    with open(filepath, "w", encoding = "utf-8", newline = "") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(headers)
        question_counter = 1

        #写入问题行
        for item in question:
            question_row = [
                question_counter,
                item.get("title", ""),
                item.get("content", "")
            ]
            writer.writerow(question_row)

            for answer_item in item.get("answer"):
                answer_row = [
                    "",
                    answer_item.get("answer_index", ""),
                    answer_item.get("answer_content", "")
                ]
                writer.writerow(answer_row)

            question_counter += 1