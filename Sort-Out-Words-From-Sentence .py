file = "This is a very *long String, %with many uninteresting word, that should be! cut out of the result."
punctuations = "!()-[]{};:\,<>./?@#$%^&*_~"
uninteresting_words = ["the", "a", "to", "if", "is", "it", "of", "and", "or", "an", "as", "i", "me", "my", \
"we", "our", "ours", "you", "your", "yours", "he", "she", "him", "his", "her", "hers", "its", "they", "them", \
    "their", "what", "which", "who", "whom", "this", "that", "am", "are", "was", "were", "be", "been", "being", \
    "have", "has", "had", "do", "does", "did", "but", "at", "by", "with", "from", "here", "when", "where", "how", \
    "all", "any", "both", "each", "few", "more", "some", "such", "no", "nor", "too", "very", "can", "will", "just"]

counts_of_frequency = {}
words = file.split()

for word in words:
    if word.lower() in uninteresting_words:
        continue
    for char in word:
        if char in punctuations:
            new_word = word.strip(char)
            counts_of_frequency[new_word] = counts_of_frequency.get(new_word, 0) + 1
            continue
counts_of_frequency[word] = counts_of_frequency.get(word, 0) + 1        

print(counts_of_frequency)

    
#counts_of_frequency = {}
#for word in file:
#     if word in :
#            continue
#    if word in punctuations and uninteresting_words:
#           continue
#    counts_of_frequency[word] = counts_of_frequency.get(word, 0) + 1

#print(counts_of_frequency)
