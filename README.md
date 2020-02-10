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
    
4. `routing` defines what path the javascript on the page should 'knock to' to reach our python code (which is mostly 
located in `consumers.py`)
5. `consumers` define our logic: it contains one class called `EbayConsumer`

The logic there is straightforward - as soon as someone connects, we get his/her group id, and player id and find these
two objects on our database.

Then we add new connections to a special `group` that allows them to communicate in real time (in `connect` method).

`receive` method of `EbayConsumer` is executed every time we get a new message from the user. If it contains 
`bid_up` command then we send the information that current bid is increased to the entire group.

In other words we just call a `new_bid` method below, that:

* updates a price for the group.
* updates an information about the winner
* Resets the counter till when the auction is over.
* Sends this whole package to all group members.







A small piece of code based on channels to demonstrate how to create
simple auctions in oTree
---
Filipp Chapkovski, Higher School of Economics, Moscow

