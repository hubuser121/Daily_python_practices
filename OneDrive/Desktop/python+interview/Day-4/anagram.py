def is_anagram(str1,str2):
    return sorted(str1.lower().strip().replace(" ",""))==sorted(str2.lower().strip().replace(" ",""))
print(is_anagram("listen" , "silenT"))
print(is_anagram("karthik " ,"     thikakr"))