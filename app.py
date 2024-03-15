from flask import Flask, render_template, request, jsonify
from laybinhluan import scrape_facebook_comments,scrape_shopee_comments,scrape_youtube_comments
import pickle
from sklearn.preprocessing import LabelEncoder
import re
from flask import send_file
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from tienxuli import preprocess_text,xoastopword
import os
import numpy as np


app = Flask(__name__)

# Đọc mô hình Logistic Regression từ file
with open('logistic_regression_model.pkl', 'rb') as file:
    log_reg_model = pickle.load(file)

# Đọc mô hình SVM từ file
with open('svm_model.pkl', 'rb') as file:
    svm_model = pickle.load(file)

# Đọc mô hình Naive Bayes từ file
with open('naive_bayes_model.pkl', 'rb') as file:
    nb_model = pickle.load(file)

# Đọc mô hình Naive Bayes +  Logistic Regression  từ file
with open('blender_model.pkl', 'rb') as file:
    blender_model = pickle.load(file)

with open('vectorizer.pkl', 'rb') as file:
    loaded_vectorizer = pickle.load(file)


# Định nghĩa hàm phân tích cảm xúc cho văn bản
def analyze_text(text, selected_model):
    # Tiền xử lý văn bản
    processed_text = preprocess_text(text)
    # Vector hóa văn bản
    new_text_vectorized = loaded_vectorizer.transform([processed_text])
    # Dự đoán sử dụng mô hình đã nạp
    if selected_model == 'logistic_regression':
        prediction = log_reg_model.predict(new_text_vectorized)
    elif selected_model == 'svm':
        prediction = svm_model.predict(new_text_vectorized)
    elif selected_model == 'naive_bayes':
        prediction = nb_model.predict(new_text_vectorized)
    elif selected_model == 'nb_svm':
        blender_features = np.column_stack((svm_model.predict(new_text_vectorized), nb_model.predict(new_text_vectorized)))
        prediction = blender_model.predict(blender_features)
    else:
        return {'error': 'Invalid model selected'}
    # Giải mã nhãn dự đoán
    label_encoder = LabelEncoder()
    label_encoder.fit(['0', '1', '2'])  
    predicted_label = label_encoder.inverse_transform(prediction)
    return {'sentiment': predicted_label[0]}

@app.route('/')
def index():
    return render_template('giaodien2chucnang.html')




@app.route('/scrape_comments', methods=['POST'])
def scrape_comments():
    data = request.get_json()
    post_url = data.get('postUrl')
    platform = data.get('platform')
    
    # Tạo tên file tạm thời hoặc đường dẫn
    output_file = "temp_comments.csv"

    if platform == 'facebook':
        scrape_facebook_comments(post_url, output_file)
    elif platform == 'youtube':
        scrape_youtube_comments(post_url, output_file)
    elif platform == 'shopee':
        scrape_shopee_comments(post_url, output_file)
    
    # Trả về file cho client
    return send_file(output_file, as_attachment=True)






@app.route('/analyze', methods=['POST'])
def analyze_sentiment():
    data = request.get_json()
    text = data.get('text', '')
    selected_model = data.get('model', 'logistic_regression')
    result = analyze_text(text, selected_model)
    return jsonify(result)


@app.route('/analyze_csv', methods=['POST'])

def analyze_csv():
    data = request.get_json()
    input_file_path = data.get('input_file_path', '')
    text_column = data.get('text_column', '')
    selected_model = data.get('model', 'logistic_regression')

    try:
        print(data)
        # Đọc dữ liệu từ file CSV
        df = pd.read_csv(input_file_path)
        
        # Áp dụng hàm phân tích cảm xúc cho mỗi dòng dữ liệu
        df['predicted_sentiment'] = df[text_column].apply(lambda x: analyze_text(x, selected_model)['sentiment'])
        
        # Lưu kết quả vào file CSV mới hoặc trả về dữ liệu dưới dạng JSON
        columns_to_keep = [text_column, 'predicted_sentiment']
        df = df[columns_to_keep]
        # Tính toán dữ liệu cho pie chart
        categorical_counts = df['predicted_sentiment'].value_counts()
        labels_mapping = {'2': 'Tích cực', '0': 'Tiêu cực', '1': 'Trung lập'}
        labels = categorical_counts.index.map(labels_mapping)
        sizes = categorical_counts.values
        # Vẽ pie chart
        # Tạo figure và axes
        fig = plt.figure(figsize=(12, 6))
        ax1 = fig.add_subplot(1, 2, 1)  # subplot cho pie chart
        ax2 = fig.add_subplot(1, 2, 2)  # subplot cho word cloud

        colors = {'Tích cực': 'green', 'Tiêu cực': 'red', 'Trung lập': 'gray'}
        # Vẽ pie chart
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140,  colors=[colors[label] for label in labels])
        ax1.set_title('Pie Chart')
        # Vẽ word cloud
        text = ' '.join((df[text_column]))
        wordcloud = WordCloud(width=400, height=200, background_color='white').generate(xoastopword(text))
        ax2.imshow(wordcloud, interpolation='bilinear')
        ax2.axis('off')
        ax2.set_title('Word Cloud')
        # Đường dẫn đến thư mục static
        static_folder = os.path.join(app.root_path, 'static')
        # Lưu hình ảnh vào thư mục static
        plt.savefig(os.path.join(static_folder, f"{selected_model}.png"))

        return jsonify({'status': 'success', 'data': df.to_dict(orient='records')})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
