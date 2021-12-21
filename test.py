#!/usr/bin/python3


s = "jab. jab."
parts = [p.strip() for p in s.split(".") if p != ""]
for p in parts:
    print(p)
