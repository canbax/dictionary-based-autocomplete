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

class TurkishTrie:
  """ letter alternatives should be generated from statistics of typos 
  things to concern: 
  1. ünlü düşmesi like (oğul-u > oğlu)
  2. ünlü daralması  “a” veya “e” sesi daralarak “ı, i, u, ü” seslerinden birine dönüşür: başla-yor > başlıyor
  3. Ünsüz Yumuşaması “p, ç, t, k” sert ünsüzleri ile biten sözcükler, ünlü ile başlayan bir ek aldığında yumuşayarak “b, c, d, g, ğ” ye dönüşür:
  """

  def __init__(self, letter_alternatives=None):
    self.head = Node()
    if letter_alternatives == None:
      self.letter_alternatives = { 'a':set({}), 'b':set({'p'}), 'c':set({'ç'}), 'ç':set({'c'}), 'd':set({'t'}), 'e':set({}),
      'f':set({}), 'g':set({'ğ', 'k'}), 'ğ':set({'g', 'k'}), 'h':set({}), 'ı':set({'i','a','e'}), 'i':set({'ı','a','e'}), 'j':set({'c'}), 'k':set({'c'}), 
      'l':set({}), 'm':set({}), 'n':set({}), 'o':set({'ö'}), 'ö':set({'o'}), 'p':set({}), 'r':set({}), 's':set({'ş'}), 'ş':set({'s'}), 't':set({}), 
      'u':set({'ü','a','e'}), 'ü':set({'u','a','e'}), 'v':set({}), 'y':set({}), 'z':set({}), 'x':set({'ks'}), 'q':set({'ku', 'k'}) }
    else:
      self.letter_alternatives = letter_alternatives
  
  def is_vowel(self, letter):
    return letter in 'aeıiuüoö'
  
  def __getitem__(self, key):
    return self.head.children[key]

  def add(self, word):
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
    curr_node.data = word
  
  def has_word(self, word):
    if word == None:
      raise ValueError('word should not be None')
    if word == '':
      return False
    
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
  
  # standard bfs goes through alternatives of letter
  def bfs(self, word, word_idx, curr_node, results, path):
    
    if curr_node == None or word_idx == len(word):
      results.add(path)
      return

    curr_char = word[word_idx]
    alternatives = (self.letter_alternatives[curr_char]).union(set({curr_char}))
    
    has_alternative = False
    for alternative in alternatives:
      if alternative in curr_node.children:
        has_alternative = True
        idx2 = word_idx + 1
        path += alternative
        self.bfs(word, idx2, curr_node[alternative], results, path)
    
    if not has_alternative:
      results.add(path)

  def get_data(self, word):
    """ This returns the 'data' of the node identified by the given word """
    if not self.has_word(word):
      raise ValueError('{} not found in trie'.format(word))
        
    # Race to the bottom, get data
    curr_node = self.head
    for letter in word:
      curr_node = curr_node[letter]
    
    return curr_node.data

trie = TurkishTrie()
trie.add('kitap')
trie.add('kitaplık')
trie.add('sakız')
trie.add('gel')
result_set = set({})
trie.bfs('sakiz', 0, trie.head, result_set, '')
print (result_set)

print (trie.has_word('gelmek'))
print (trie.has_word('gel'))

