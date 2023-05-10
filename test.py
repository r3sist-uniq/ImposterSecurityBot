# import re
pattern = r'^j[-_ ]?o[-_ ]?h[-_ ]?n[-_ ]?c[-_ ]?o[-_ ]?o[-_ ]?g[-_ ]?a[-_ ]?n[-_ ]?$'
print(pattern)
# names = [
#     "john-coogan",
#     "jo-hncoogan",
#     "j_ohncoogan",
#     "johncoogan_",
#     "john coogan",
#     "johncoogan aman",
#     "best_johncoogan",
#     "john",
#     "john carmack"
# ]

# for name in names:
#     if re.match(pattern, name):
#         print(f"Matched: {name}")
#     else:
#         print(f"Not matched: {name}")
import re

def generate_regex_pattern(name):
    pattern = '^[-_ ]?' + ''.join(f'{c}[-_ ]?' for c in name.lower()) + '[-_ ]?$'
    return pattern

# Example usage
names = [
    "john-coogan",
    "jo-hncoogan",
    "j_ohncoogan",
    "johncoogan_",
    "john coogan",
    "johncoogan aman",
    "best_johncoogan",
    "john",
    "john carmack"
]

regex = generate_regex_pattern("aman_ok")
print(regex)
        