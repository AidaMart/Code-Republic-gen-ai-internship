#!/usr/bin/env python
# coding: utf-8

# In[52]:


import weakref
import ctypes

def get_count(id):
    return ctypes.c_long.from_address(id).value

class Person:
    pass

ob1 = Person()
ob2 = weakref.ref(ob1)

print(ob2())
get_count(id(ob1))


# In[11]:


# Metaprogramming 

# Decorators & Descriptors
from functools import wraps

def decorator(function):
    
    @wraps(function)
    def wrapper(*args, **kwargs):
        return function(*args, **kwargs)
    
    return wrapper

@decorator
def foo():
    '''Why use foo '''
    print('hello')

@decorator
def foo2(arg):
    '''Why use foo2'''
    print(arg)

foo()
foo2(123)

print(foo.__name__)
foo2.__name__


# In[12]:


class Squared(int):
    def __new__(cls, x):
        return super().__new__(cls, x ** 2)
    

obj = Squared(5)
obj


# In[49]:


# Descriptors

# two types 
# 1. Non-data descriptors, __get__(self, instance, owner=None) -> obj.x 
# 2. Data Descriptors __get__, __set__(self, instance, value)
# __delete__(self, instance, owner)
# __set_name__(self, owner, property_name) -> Python 3.6

import weakref

import ctypes
import sys
class Integer:

    def __init__(self, value):
        self.data = weakref.WeakKeyDictionary()

    def __get__(self, instance, owner=None):
        print(id(instance))
        # print(f'__get__ is called : self={self}, instance={instance}, owner={owner}')
        if instance is None:
            return self
        return self.data.get(instance, None)
    
    def __set__(self, instance, value):
        # print(f'__set__ : self={self}, instance={instance}, value={value}')
        if not isinstance(value, int):
            raise ValueError('The value must be an integer')
        self.data[instance] = value
    
class MyInteger:
    attribute = Integer(12)

obj = MyInteger()
obj.attribute
print(id(obj))
obj1 = MyInteger()
obj.attribute = 35

# print(id(obj.attribute), id(obj1.attribute))
# print(obj.attribute, obj1.attribute)

obj_id = id(obj)
obj.attribute
print(ctypes.c_long.from_address(obj_id).value)




# In[77]:


class Descriptor:
  def __set_name__(self, owner, property):
    print(f'__set_name__, owner={owner}, property={property}')
    self.property = property

  def __set__(self, instance, value):
    # check
    instance.__dict__[self.property] = value

  def __get__(self, instance, owener):
    # check 
    print(self.property)
    return instance.__dict__.get(self.property, None)




class Mlass:
  x = Descriptor()
  x = Descriptor()

obj = Mlass()
obj.x = 12
obj.x
obj.__dict__

obj2 = Mlass()
obj2.x = 24

print(obj.x)
print(obj2.x)



# In[86]:


# __slots__

class A: 
    __slots__ = ('_x', '_y')
    def __init__(self, x, y):
        self._x = x 
        self._y = y

    @property
    def x(self):
      return self._x
  


obj = A(1, 3)

obj.x
obj.x = 35


# In[94]:


namespace = {}
exec('''
def add(x, y): return x + y
def mul(x, y): return x * y
''', globals(),namespace)

namespace['add'](1, 2)
namespace['mul'](5, 2)

globals()


# In[ ]:




