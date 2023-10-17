from bs4 import BeautifulSoup


def replace_src_attributes(file_path):
    # Đọc nội dung của file HTML
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Sử dụng BeautifulSoup để phân tích HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Tìm tất cả các thẻ có thuộc tính src
    elements_with_src = soup.find_all(attrs={'src': True})

    for element in elements_with_src:
        src_value = element['src']

        # Kiểm tra xem thuộc tính src đã chứa {% static ... %} chưa
        if not src_value.startswith("{% static") and not src_value.endswith("%}"):
            new_src_value = "{% static '" + src_value + "' %}"
            element['src'] = new_src_value

    # Ghi lại file với sự thay đổi
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(str(soup))


file_path = '/Users/minhkhue/Documents/GitHub/Personal-projects/django-ecommerce-template/products/templates/products/products_grid.html'
replace_src_attributes(file_path)