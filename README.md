# Mini ebay-like auction

---
UPDATE:
-----
The code is now re-written so it works with new oTree (>2.5) and new Django Channels (2.x)/


Introduction
=================

How does this thing work:

1. We create a standard oTree app (`ebay` folder)
2. We add its name to the `settings.py` as an oTree extension:

```python
EXTENSION_APPS = ['ebay']
```

3. In `ebay` folder we create another sub-folder named `otree_extensions` and we create two python files there:
    1. `consumers.py`
    2. `routing.py`
    
 


A small piece of code based on channels to demonstrate how to create
simple auctions in oTree
---
Filipp Chapkovski, Higher School of Economics, Moscow

