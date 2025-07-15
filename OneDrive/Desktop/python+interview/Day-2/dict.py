dict={"brand":"bmw",
      "year":2025,
      "model":"m4"}

print("my dict ", dict)
dict["price"]=20000000
for key , value in dict.items():
    print( key, ":" ,value )