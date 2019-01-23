import re
import time

# sources used to generate word list
# zargan: Bilgin, O. (2016). Biçimbilimsel Bakımdan Karmaşık Türkçe Kelimelerin İşlenmesinde Frekans Etkileri (yayınlanmamış yüksek lisans tezi). Boğaziçi Üniversitesi, İstanbul. Erişim: http://st2.zargan.com/public/resources/turkish/frequency_effects_in_turkish.pdf
# aklimagelmisken.xyz: https://www.aklimagelmisken.xyz/turkce-yazim-imla-kilavuzu-tdk-txt-dosyasi-indir/
# emrahcom: https://github.com/emrahcom/turkce_kelimeler
# excelgurusu: http://www.excelgurusu.com/download.php?d=TDK-MLA-KILAVUZU.zip
# maidis: https://github.com/maidis/mythes-tr
# cannuhlar: https://github.com/CanNuhlar/Turkce-Kelime-Listesi

file_names = ['dictionary sources/aklimagelmisken.xyz/Türkçe Yazım Kılavuzu.txt','dictionary sources/emrahcom/imla_kilavuzu.txt',
'dictionary sources/zargan/word_forms_stems_and_frequencies_full.txt', 'dictionary sources/excelgurusu/tdk-imla.txt', 
'dictionary sources/cannuhlar/turkce_kelime_listesi.txt',]

def get_words_from_line(line):
  return set(re.findall( r'\w+', line, re.U))

def get_first_word_from_line(line):
  m = re.findall( r'\w+', line, re.U)
  if len(m) > 0:
    return m[0]
  return None

def get_second_word_from_line(line):
  m = re.findall( r'\w+', line, re.U)
  if len(m) > 1:
    return m[1]
  return None

def parse_source(get_word_from_line_fn, file_name):
  all_words = set({})

  with open(file_name, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
      word = get_word_from_line_fn(line)
      if word != None and not word.isnumeric():
        word = word.lower()
        all_words.add(word)
  print('found ', len(all_words), ' unique words')
  
  return all_words

def write_set_of_words2file(set_of_words):
  words = sorted(set_of_words)
  with open('words.txt', 'w', encoding='utf-8') as f:
    for word in words:
        f.write("%s\n" % word)

start = time.time()
word_set0 = parse_source(get_first_word_from_line, file_names[0])
word_set1 = parse_source(get_first_word_from_line, file_names[1])
word_set2 = parse_source(get_second_word_from_line, file_names[2])
word_set3 = parse_source(get_first_word_from_line, file_names[3])
word_set4 = parse_source(get_first_word_from_line, file_names[4])

all_sets = word_set1.union(word_set0).union(word_set2).union(word_set3).union(word_set4)
print('found ', len(all_sets), ' unique words')
# print(all_sets)

write_set_of_words2file(all_sets)

end = time.time()
print('Executed in ', end - start, ' secs')