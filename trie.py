class Node:
  def __init__(self, label=None, data=None):
    self.label = label
    self.data = data
    self.children = dict()
  
  def add_child(self, key, data=None):
    if not isinstance(key, Node):
      self.children[key] = Node(key, data)
    else:
      self.children[key.label] = key

  def __getitem__(self, key):
    return self.children[key]

# constructing Trie by reading words from right to left might be useful to find some words
class Trie:
  """ letter alternatives should be generated from statistics of typos 
  things to concern: 
  1. ünlü düşmesi like (oğul-u > oğlu)
  2. ünlü daralması  “a” veya “e” sesi daralarak “ı, i, u, ü” seslerinden birine dönüşür: başla-yor > başlıyor
  3. Ünsüz Yumuşaması “p, ç, t, k” sert ünsüzleri ile biten sözcükler, ünlü ile başlayan bir ek aldığında yumuşayarak “b, c, d, g, ğ” ye dönüşür:
  4. şapkalı harfler: "î, â, û" 
  """

  def __init__(self, letter_alternatives=None, alphabet=None, dict_file_name=None):
    self.head = Node()
    if letter_alternatives == None:
      self.letter_alternatives = { 'a':set({'â'}), 'b':set({'p'}), 'c':set({'ç'}), 'ç':set({'c'}), 'd':set({'t'}), 'e':set({}),
      'f':set({}), 'g':set({'ğ', 'k'}), 'ğ':set({'g', 'k'}), 'h':set({}), 'ı':set({'i','a','e','î'}), 'i':set({'ı','a','e','î'}), 'j':set({'c'}), 'k':set({'c'}), 
      'l':set({}), 'm':set({}), 'n':set({}), 'o':set({'ö'}), 'ö':set({'o'}), 'p':set({}), 'r':set({}), 's':set({'ş'}), 'ş':set({'s'}), 't':set({}), 
      'u':set({'ü','a','e','û'}), 'ü':set({'u','a','e','û'}), 'v':set({}), 'y':set({}), 'z':set({}), 'x':set({'ks'}), 'q':set({'ku', 'k'}) }
    else:
      self.letter_alternatives = letter_alternatives
    if alphabet:
      self.alphabet = alphabet
    else:
      self.alphabet = 'abcçdefgğhıijklmnoöprsştuüvyz'

    if dict_file_name != None:
      self.build_trie(dict_file_name)
      
  def is_vowel(self, letter):
    return letter in 'aeıiuüoö'
  
  def __getitem__(self, key):
    return self.head.children[key]

  def add(self, word, word_idx):
    curr_node = self.head

    i = 0
    while i < len(word):
      if word[i] in curr_node.children:
        curr_node = curr_node.children[word[i]]
        i += 1
      else:
        # add this word to trie
        while i < len(word):
          curr_node.add_child(word[i])
          curr_node = curr_node.children[word[i]]
          i += 1
        break
    
    # Let's store the full word at the end node so we don't need to
    # travel back up the tree to reconstruct the word
    curr_node.data = word_idx
  
  def has_word(self, word):
    if word == None:
      raise ValueError('word should not be None')
    if word == '':
      return False
    word = word.lower()
    curr_node = self.head

    for letter in word:
      if letter in curr_node.children:
        curr_node = curr_node.children[letter]
      else:
        return False
    
    return curr_node.data != None

  def get_closest(self, word):
    if word == None:
      raise ValueError('word should not be None')
    if word == '':
      return False
    
    curr_path = ''
    for letter in word:
      if letter in curr_node.children:
        curr_path += letter
        curr_node = curr_node.children[letter]
      else:
        curr_node = curr_node
  
  def get_data(self, word):
    """ This returns the 'data' of the node identified by the given word """
    if not self.has_word(word):
      raise ValueError('{} not found in trie'.format(word))
        
    # Race to the bottom, get data
    curr_node = self.head
    for letter in word:
      curr_node = curr_node[letter]
    
    return curr_node.data

  # standard bfs goes through alternatives of letter
  # word must be lower case
  def bfs(self, word, char_idx, curr_node, results, path):
    if curr_node == None or char_idx == len(word):
      results.add(path)
      return

    curr_char = word[char_idx]
    alternatives = (self.letter_alternatives[curr_char]).union(set({curr_char}))
    
    has_alternative = False
    for alternative in alternatives:
      curr_path = path
      if alternative in curr_node.children:
        has_alternative = True
        idx2 = char_idx + 1
        curr_path += alternative
        self.bfs(word, idx2, curr_node[alternative], results, curr_path)
    
    # assume there is an extra letter in the word
    self.bfs(word, char_idx + 1, curr_node, results, path)
    
    # what happens if there is a missing letter in the word ? 
    # has_missing_letter = False
    # for letter in self.alphabet:
    #   curr_path = path
    #   if letter in curr_node.children:
    #     has_missing_letter = True
    #     curr_path += letter
    #     self.bfs(word, char_idx, curr_node[letter], results, curr_path)

    if not has_alternative:
      results.add(path)
  
  def edit_dist(self, s1, s2):
    l1 = len(s1) + 1
    l2 = len(s2) + 1
    table = [[i if j==0 else j if i==0 else 0 for i in range(l1)] for j in range(l2)]
    for i in range(1, l1):
      for j in range(1, l2):
        if s1[i - 1] == s2[j - 1]:
          table[j][i] = table[j - 1][i - 1]
        else:
          table[j][i] = 1 + min(table[j][i - 1], table[j - 1][i], table[j - 1][i - 1])
    return table[l2 - 1][l1 - 1]

  def lemmatize(self, pattern, dist_func=None):
    result_set = set({})
    self.bfs(pattern, 0, self.head, result_set, '')
    if dist_func == None:
      dist_func = self.edit_dist
    
    min_dist = 2147000000
    min_dist_elem = ''
    for result in result_set:
      dist = dist_func(pattern, result)
      if dist < min_dist:
        min_dist = dist
        min_dist_elem = result
    return min_dist_elem

  def build_dictionary_from_file(self, file_name):
    d = dict()
    cnt = 0
    with open(file_name, 'r', encoding='utf-8') as f:
      lines = f.readlines()
      for line in lines:
        d[cnt] = line.strip()
        cnt = cnt + 1
    return d

  def build_trie_from_dictionary(self, dic):
    for word_idx in dic:
      self.add(dic[word_idx], word_idx)

  def build_trie(self, dict_file_name):
    d = self.build_dictionary_from_file(dict_file_name)
    self.build_trie_from_dictionary(d)

trie = Trie(None, None, 'tr_words.txt')
print (trie.lemmatize("mesaaj"))

