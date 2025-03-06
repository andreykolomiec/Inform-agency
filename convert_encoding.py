# Крок 1: Читання файлу з кодуванням utf-16
with open('dump.json', 'r', encoding='utf-16') as f:
    content = f.read()  # Зчитуємо весь вміст файлу

# Крок 2: Запис в новий файл з кодуванням utf-8
with open('dump_utf8.json', 'w', encoding='utf-8') as f:
    f.write(content)  # Записуємо вміст у новий файл з кодуванням utf-8

print("File was successfully transcoded!")
